from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel, QLineEdit, QSlider, QWidget


# widget container that combines a QLabel and an input box left to right
class LabelAndInput(QWidget):
    def __init__(
        self, labelText, lineEditStartingText, valMin, valMax, onTextEdit, outerLayout
    ):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.label = QLabel(labelText)
        self.lineEdit = QLineEdit()
        self.lineEdit.setText(lineEditStartingText)
        self.lineEdit.setValidator(QIntValidator(valMin, valMax))
        self.lineEdit.textEdited.connect(onTextEdit)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lineEdit)
        outerLayout.addWidget(self)


class StatLabelAndSlider(QWidget):
    def __init__(
        self,
        labelText,
        sliderStartingVal,
        valMin,
        valMax,
        onSliderMove,
        outerLayout,
        stat,
    ):
        super().__init__()

        self.labelText = labelText
        self.layout = QHBoxLayout(self)
        self.label = QLabel(labelText + str(sliderStartingVal))
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(valMin)
        self.slider.setMaximum(valMax)
        self.slider.setValue(int(sliderStartingVal))
        self.slider.sliderMoved.connect(lambda val: onSliderMove(val, stat))
        self.slider.sliderMoved.connect(self.updateLabelText)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
        outerLayout.addWidget(self)

    def updateLabelText(self, num):
        self.label.setText(self.labelText + str(num))


class DropDown(QWidget):
    def __init__(self, itemList, outerLayout, startingIndex, onComboChange):
        super().__init__()

        combo = QComboBox()
        for item in itemList:
            combo.addItem(item)
        combo.setMaxVisibleItems(15)
        outerLayout.addWidget(combo)
        combo.setCurrentIndex(startingIndex)
        combo.currentIndexChanged.connect(onComboChange)


class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # custom signal

    def mousePressEvent(self, event):
        self.clicked.emit()  # emit signal when label is clicked
