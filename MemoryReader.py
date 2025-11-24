import contextlib
from enum import IntEnum

import pymem
import pymem.process


class Stats(IntEnum):
    Strength = 0
    Defense = 1
    Magic = 2
    Agility = 3


class MemoryReader:
    def __init__(self, mainGUIRefresh):
        self.mainGUIRefresh = mainGUIRefresh
        self.pm = pymem.Pymem('castle.exe')

        module = pymem.process.module_from_name(self.pm.process_handle, 'castle.exe')
        base_address = module.lpBaseOfDll

        # Pointer chain offsets
        offsets = [0x0038E198, 0x34, 0x24, 0xA8]

        # Resolve pointer chain (resolves to green knights strength stat)
        addr = base_address + offsets[0]
        for offset in offsets[1:]:
            addr = self.pm.read_int(addr) + offset

        self.greenKnightAddress = addr - 0x08
        self.characterAddress = self.greenKnightAddress
        self.selectedCharacter = 1

        self.levelOffset = 1
        self.xpOffset = 2
        self.goldOffset = 19
        self.strengthOffset = 8
        self.weaponOffset = 6
        self.petOffset = 7
        self.normalLevelUnlocksOffset = 12
        self.insaneModeUnlockedOffset = 23
        self.insaneLevelUnlocksOffset = 24

    def setCharacter(self, id):
        # each character is 48 bytes of data
        self.selectedCharacter = id
        self.characterAddress = self.greenKnightAddress + 48 * (id - 1)

    def isUnlocked(self):
        data = self.pm.read_bytes(self.characterAddress, 1)
        return int.from_bytes(data, byteorder='big')

    def characterLockToggle(self):
        if self.isUnlocked():
            self.pm.write_bytes(self.characterAddress, b'\x00', 1)
        else:
            self.pm.write_bytes(self.characterAddress, b'\x80', 1)
        self.mainGUIRefresh()

    def getLevel(self):
        # levels are 0 based so level 99 is 98 in memory
        data = self.pm.read_bytes(self.characterAddress + self.levelOffset, 1)
        return int.from_bytes(data, byteorder='big') + 1

    def setLevel(self, level):
        # levels are 0 based so - 1 is needed
        level = level - 1
        self.pm.write_bytes(
            self.characterAddress + self.levelOffset,
            level.to_bytes(1, byteorder='big'),
            1,
        )

    def setXP(self, xp):
        self.pm.write_bytes(
            self.characterAddress + self.xpOffset,
            xp.to_bytes(4, byteorder='big', signed=True),
            4,
        )

    def getXP(self):
        data = self.pm.read_bytes(self.characterAddress + self.xpOffset, 4)
        return int.from_bytes(data, byteorder='big')

    def setGold(self, xp):
        self.pm.write_bytes(
            self.characterAddress + self.goldOffset,
            xp.to_bytes(4, byteorder='big', signed=True),
            4,
        )

    def getGold(self):
        data = self.pm.read_bytes(self.characterAddress + self.goldOffset, 4)
        return int.from_bytes(data, byteorder='big')

    def getStat(self, attribute):
        data = self.pm.read_bytes(
            self.characterAddress + self.strengthOffset + attribute, 1,
        )
        return int.from_bytes(data, byteorder='big')

    def setStat(self, value, attribute):
        self.pm.write_bytes(
            self.characterAddress + self.strengthOffset + attribute,
            value.to_bytes(1, byteorder='big'),
            1,
        )

    def getWeapon(self):
        data = self.pm.read_bytes(self.characterAddress + self.weaponOffset, 1)
        return int.from_bytes(data, byteorder='big')

    def setWeapon(self, index):
        self.pm.write_bytes(
            self.characterAddress + self.weaponOffset,
            index.to_bytes(1, byteorder='big'),
            1,
        )

    def getPet(self):
        data = self.pm.read_bytes(self.characterAddress + self.petOffset, 1)
        return int.from_bytes(data, byteorder='big')

    def setPet(self, index):
        self.pm.write_bytes(
            self.characterAddress + self.petOffset,
            index.to_bytes(1, byteorder='big'),
            1,
        )

    def getLevelBitsHelper(self, addressOffset):
        count = 0
        for i in range(3):
            data = self.pm.read_bytes(self.characterAddress + addressOffset + i, 1)
            byte_val = int.from_bytes(data, byteorder='big')
            count += bin(byte_val).count('1')
        return count

    def writeLevelBitsHelper(self, checkpointIndex, addressOffset):
        total_bits = checkpointIndex
        full_bytes = total_bits // 8  # Number of bytes fully set (0xFF)
        leftover_bits = total_bits % 8  # Bits to set in the last byte

        for i in range(3):
            if i < full_bytes:
                byte_val = 0xFF
            elif i == full_bytes:
                if leftover_bits == 0:
                    byte_val = 0x00
                else:
                    byte_val = (1 << leftover_bits) - 1
            else:
                byte_val = 0x00

            self.pm.write_bytes(
                self.characterAddress + addressOffset + i,
                byte_val.to_bytes(1, byteorder='big'),
                1,
            )

    def getNormalLevelUnlocks(self):
        return self.getLevelBitsHelper(self.normalLevelUnlocksOffset)

    def setNormalLevelUnlocks(self, checkpointIndex):
        return self.writeLevelBitsHelper(checkpointIndex, self.normalLevelUnlocksOffset)

    def isInsaneModeUnlocked(self):
        data = self.pm.read_bytes(
            self.characterAddress + self.insaneModeUnlockedOffset, 1,
        )
        return int.from_bytes(data, byteorder='big')

    def insaneModeLockToggle(self):
        if self.isInsaneModeUnlocked():
            self.pm.write_bytes(
                self.characterAddress + self.insaneModeUnlockedOffset, b'\x00', 1,
            )
        else:
            self.pm.write_bytes(
                self.characterAddress + self.insaneModeUnlockedOffset, b'\x01', 1,
            )

    def getInsaneLevelUnlocks(self):
        return self.getLevelBitsHelper(self.insaneLevelUnlocksOffset)

    def setInsaneLevelUnlocks(self, checkpointIndex):
        return self.writeLevelBitsHelper(checkpointIndex, self.insaneLevelUnlocksOffset)

    def __del__(self):
        if getattr(self, 'pm', None):
            self.pm.close_process()
