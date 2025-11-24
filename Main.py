import os
import sys

from CharacterStatWindow import CharacterStatWindow
from CustomWidgets import ClickableLabel
from MemoryReader import MemoryReader
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QImage, QPainter, QPalette, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QStyle,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.memoryReader = MemoryReader(self.refreshImageGrid)

        self.useNewCharacterSprites = True
        self.setWindowTitle('Castle Crashers Save Editor')
        self.setGeometry(200, 200, 615, 600)

        self.menu_bar = self.menuBar()
        self.menu_bar.clear()

        option_menu = self.menu_bar.addMenu('Options')
        changeStyleButton = QAction('Change Sprite Style', self)
        changeStyleButton.triggered.connect(self.changeStyle)
        option_menu.addAction(changeStyleButton)
        helpButton = QAction('Instructions', self)
        helpButton.triggered.connect(self.openInstructions)
        option_menu.addAction(helpButton)

        self.characterLabels = []
        self.image_width = 0
        self.refreshImageGrid()

    def refreshImageGrid(self):
        # Create widget that will contain all the images
        self.container = QWidget()
        self.grid = QGridLayout()
        self.container.setLayout(self.grid)

        for label in self.characterLabels:
            self.grid.removeWidget(label)

        self.characterLabels = []

        # folder_path = ".\\CharacterSprites\\"
        folder_path = self.resource_path('./CharacterSprites/')

        if self.useNewCharacterSprites:
            self.image_width = QPixmap(f'{folder_path}{101}.png').width() + 5
        else:
            # with the old sprites some are wider than others
            self.image_width = QPixmap(f'{folder_path}{7}.png').width() + 10

        self.images_per_row = int(self.width() / self.image_width)
        iImageOffset = 0
        if self.useNewCharacterSprites:
            iImageOffset = 100

        oldSelectedCharacter = self.memoryReader.selectedCharacter
        for i in range(42):
            # skip paint junior and custom characters
            if i > 30 and not self.useNewCharacterSprites:
                continue

            label = ClickableLabel()

            pixmap = None

            if i < 28:
                image_path = f'{folder_path}{i + 1 + iImageOffset}.png'
                pixmap = QPixmap(image_path)

                self.memoryReader.setCharacter(i + 1)
                if not self.memoryReader.isUnlocked():
                    gray_image = pixmap.toImage().convertToFormat(
                        QImage.Format.Format_Grayscale8,
                    )
                    pixmap = QPixmap.fromImage(gray_image)
            else:
                self.memoryReader.setCharacter(i + 1)
                if not self.memoryReader.isUnlocked():
                    # dont add to list if DLC not enabled
                    continue

                if i < 32:
                    # pink, purple, hatty, painter
                    image_path = f'{folder_path}{i + 1 + iImageOffset}.png'
                    pixmap = QPixmap(image_path)
                else:
                    # painter DLC custom characters
                    image_path = f'{self.resource_path("./CharacterSprites/custom/")}{i - 32 + 1}.png'
                    pixmap = QPixmap(image_path)

            label.clicked.connect(
                lambda checked=False, idx=(i + 1): self.characterImageClicked(idx),
            )

            label.setPixmap(pixmap)

            row = i // self.images_per_row
            col = i % self.images_per_row

            self.grid.addWidget(label, row, col)
            self.characterLabels.append(label)

        self.memoryReader.setCharacter(oldSelectedCharacter)

        scroll = QScrollArea()
        scroll.setWidget(self.container)
        self.setCentralWidget(scroll)

    def changeStyle(self):
        if self.useNewCharacterSprites == True:
            self.useNewCharacterSprites = False
        else:
            self.useNewCharacterSprites = True

        self.refreshImageGrid()

    def openInstructions(self):
        msg = QMessageBox()
        msg.setWindowTitle('Instructions')
        msg.setText(
            'To use the save editor first open castle crashers to the title screen. Then start the save editor. To edit a character, click on their image while still in the title screen. To save all changes to disk, start the game with any character and exit to map.',
        )
        # Create a transparent 1x1 icon
        iconPix = QPixmap(1, 1)
        iconPix.fill(Qt.GlobalColor.transparent)
        empty_icon = QIcon(iconPix)
        msg.setWindowIcon(empty_icon)
        msg.exec_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if int(self.width() / self.image_width) != self.images_per_row:
            self.refreshImageGrid()

    # needed for pyinstaller to find image files
    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller's temp folder when running bundled
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath('.')

        return os.path.join(base_path, relative_path)

    def characterImageClicked(self, index):
        self.statWindow = CharacterStatWindow(index, self, self.memoryReader)


app = QApplication(sys.argv)

win = MainWindow()
win.show()

icon = app.style().standardIcon(QStyle.SP_DialogSaveButton)
win.setWindowIcon(icon)

sys.exit(app.exec_())
