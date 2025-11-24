from CustomWidgets import DropDown, LabelAndInput, StatLabelAndSlider
from MemoryReader import MemoryReader, Stats
from PyQt5.QtWidgets import QCheckBox, QDockWidget, QVBoxLayout, QWidget


class CharacterStatWindow(QDockWidget):
    def __init__(self, i, mainwindow, memReader: MemoryReader):
        super().__init__()
        self.i = i
        self.mainwindow = mainwindow

        self.setWindowTitle(f"{get_character_name(i)}")
        self.setFloating(True)
        self.setFixedWidth(350)

        self.memoryReader = memReader
        self.memoryReader.setCharacter(i)

        container = QWidget()
        layout = QVBoxLayout(container)

        # can't change 4 original knights or DLC knights
        if i > 4 and i < 29:
            characterUnlockCheckbox = QCheckBox("Unlocked")
            if self.memoryReader.isUnlocked():
                characterUnlockCheckbox.setChecked(True)
            characterUnlockCheckbox.toggled.connect(self.memoryReader.characterLockToggle)
            layout.addWidget(characterUnlockCheckbox)

        intMin = -2147483648
        intMax = 2147483647
        LabelAndInput("Level ", str(self.memoryReader.getLevel()), 1, 99, self.level_text_edited, layout)
        LabelAndInput("XP ", str(self.memoryReader.getXP()), intMin, intMax, self.xp_text_edited, layout)
        LabelAndInput("Gold ", str(self.memoryReader.getGold()), intMin, intMax, self.gold_text_edited, layout)

        StatLabelAndSlider("Strength ", str(self.memoryReader.getStat(Stats.Strength)), 1, 25, self.statEdited, layout, Stats.Strength)
        StatLabelAndSlider("Magic ", str(self.memoryReader.getStat(Stats.Magic)), 1, 25, self.statEdited, layout, Stats.Magic)
        StatLabelAndSlider("Defense ", str(self.memoryReader.getStat(Stats.Defense)), 1, 25, self.statEdited, layout, Stats.Defense)
        StatLabelAndSlider("Agility ", str(self.memoryReader.getStat(Stats.Agility)), 1, 25, self.statEdited, layout, Stats.Agility)

        weapons = ["Skinny Sword", "Skinny Sword", "Skinny Sword", "Thin Sword", "Thick Sword", "Pumpkin Peeler", "Gladiator Sword", "Butcher Knife", "Half Sword", "Carrot", "Thief Sword", "Gold Sword", "Dual Prong Sword", "Zigzag", "Playdo Pasta Maker", "Falchion", "Pointy Sword", "Chewed Up Sword", "Fencer's Foil", "Barbarian Axe", "Pitchfork", "Curved Sword", "Key Sword", "Apple Peeler", "Rubber Handle Sword", "Mace", "Club", "Ugly Mace", "Refined Mace", "Fish", "Wrapped Sword", "Skeletor Mace", "Clunky Mace", "Snakey Mace", "Rat Beating Bat", "Black Morning Star", "King's Mace", "Meat Tenderizer", "Leaf", "Sheathed Sword", "Practice Foil", "Twig", "Leafy Twig", "Light Saber", "Staff", "Wooden Spoon", "Bone Leg", "Alien Gun", "Fishing Spear", "Lance", "Sai", "Unicorn Horn", "Ribeye", "Kielbasa", "Lobster", "Umbrella", "Broad Ax", "Evil Sword", "Ice Sword", "Candlestick", "Panic Mallet", "Fishing Rod", "Wrench", "NG Lollipop", "Gold Skull Mace", "NG Gold Sword", "Chainsaw", "Broad Spear", "Glowstick", "Chicken Stick", "Demon Sword", "Broccoli Sword", "Man Catcher", "Wooden Mace", "Ninja Claw", "Buffalo Mace", "Electric Eel", "Scissors", "Dinner Fork", "Cattle Prod", "Lightning Bolt", "2x4", "Wooden Sword", "Cardboard Tube", "Emerald Sword", "Hammer", "Pencil", "Invisible Sword", "Invisible Sword", "Invisible Sword", "Invisible Sword", "Invisible Sword", "Invisible Sword", "Invisible Map", "Invisible Horn", "Invisible Arrow", "Invisible Shovel", "Map", "Horn", "Arrow", "Shovel"]
        DropDown(weapons, layout, int(self.memoryReader.getWeapon()), self.weaponEdited)
        pets = ["none", "Cardinal", "Owlet", "Rammy", "Frogglet", "Monkeyface", "BiPolar Bear", "Bitey Bat", "Yeti", "Troll", "Snailburt", "Giraffey", "Zebra", "Meowburt", "Pazzo", "Burly Bear", "Hawkster", "Snoot", "Piggy", "Spiny", "Scratchpaw", "Seahorse", "Chicken", "Install Ball", "Mr. Buddy", "Sherbert", "Pelter", "Dragonhead", "Beholder", "Golden Whale"]
        DropDown(pets, layout, int(self.memoryReader.getPet()), self.petEdited)
        normalLevels = ["normal mode checkpoint 0", "Castle Keep", "Barbarian Boss", "Thieves' Forest", "Catfish", "Pipistrello's Cave", "Parade", "Cyclops' Fortress", "Lava World", "Industrial Castle", "Pirate Ship", "Desert Chase", "Sand Castle Roof", "Corn Boss", "Medusa's Lair", "Full Moon", "Ice Castle", "Final Battle"]
        DropDown(normalLevels, layout, int(self.memoryReader.getNormalLevelUnlocks()), self.normalUnlocksEdited)

        insaneCheckbox = QCheckBox("is insane mode unlocked")
        if self.memoryReader.isInsaneModeUnlocked():
            insaneCheckbox.setChecked(True)
        insaneCheckbox.toggled.connect(self.memoryReader.insaneModeLockToggle)
        layout.addWidget(insaneCheckbox)

        insaneLevels = ["insane mode checkpoint 0", "Castle Keep", "Barbarian Boss", "Thieves' Forest", "Catfish", "Pipistrello's Cave", "Parade", "Cyclops' Fortress", "Lava World", "Industrial Castle", "Pirate Ship", "Desert Chase", "Sand Castle Roof", "Corn Boss", "Medusa's Lair", "Full Moon", "Ice Castle", "Final Battle"]
        DropDown(insaneLevels, layout, int(self.memoryReader.getInsaneLevelUnlocks()), self.insaneUnlocksEdited)

        self.setWidget(container)
        self.show()

    def level_text_edited(self, text):
        if text != '' and int(text) != 0:
            self.memoryReader.setLevel(int(text))

    def xp_text_edited(self, text):
        if text != '' and text != '-':
            self.memoryReader.setXP(int(text))

    def gold_text_edited(self, text):
        if text != '' and text != '-':
            self.memoryReader.setGold(int(text))

    def statEdited(self, value, attribute):
        self.memoryReader.setStat(value, attribute)

    def weaponEdited(self,index):
        self.memoryReader.setWeapon(index)

    def petEdited(self,index):
        self.memoryReader.setPet(index)

    def normalUnlocksEdited(self,index):
        self.memoryReader.setNormalLevelUnlocks(index)

    def insaneUnlocksEdited(self,index):
        self.memoryReader.setInsaneLevelUnlocks(index)

def get_character_name(id):
    names = ["Green Knight", "Red Knight", "Blue Knight", "Orange Knight", "Gray Knight", "Barbarian", "Thief", "Fencer", "Beekeeper", "Industralist", "Alien Hominid", "The King", "The Brute", "Snakey", "Saracen", "Royal Guard", "Stoveface", "Peasant", "Bear", "Necromancer", "Conehead", "Civilian", "Open-face Gray Knight", "Fire Demon", "Skeleton", "Iceskimo", "Ninja", "Cultist", "Pink Knight", "Purple Knight Blacksmith", "Hatty", "Paint Junior", "Custom 1", "Custom 2", "Custom 3", "Custom 4", "Custom 5", "Custom 6", "Custom 7", "Custom 8", "Custom 9", "Custom 10"]
    return names[id - 1] if 1 <= id <= len(names) else "Unknown Character"
