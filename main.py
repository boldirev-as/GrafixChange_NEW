import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QFileDialog, QInputDialog, QErrorMessage
from grafix import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.errorwidget = QErrorMessage(self)
        self.centralwidget.setLayout(self.verticalLayout_3)
        self.connect_widgets()
        self.style_sheet()
        self.filename = ''
        self.objectsnames = ['valuegforeditor', 'reverse',
                             'filters', 'edits']
        self.open()

    def style_sheet(self):
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.imageplace.setStyleSheet("color: rgb(255, 255, 255)")
        self.imageplace.setAlignment(Qt.AlignCenter)
        self.filters.setAlignment(Qt.AlignCenter)
        self.edits.setAlignment(Qt.AlignCenter)
        self.reverse.setAlignment(Qt.AlignCenter)

    def connect_widgets(self):
        self.openphotoact.changed.connect(self.open)
        self.closephotoact.changed.connect(self.close)
        self.renamephotoact.changed.connect(self.rename)
        self.savephotoact.changed.connect(self.save)

    def hide_all(self):
        for objectname in self.objectsnames:
            exec(f'self.{objectname}.hide()')

    def show_all(self):
        for objectname in self.objectsnames:
            exec(f'self.{objectname}.show()')

    def save(self):
        self.pixmap.save(self.filename)

    def rename(self):
        endsfiles = ['.png', '.jpg', '.bmp']
        name, ok_pressed = QInputDialog.getText(self, "Ввод нового имени файла",
                                                "Введите новое имя файла")
        while ok_pressed and not any([name.endswith(endfile) for endfile in endsfiles]):
            name, ok_pressed = QInputDialog.getText(self, "Ввод нового имени файла",
                                                    "Введите новое имя файла(вместе с его расширением)")
        if ok_pressed:
            self.filename = name

    def close(self):
        self.imageplace.setText('Выберите картинку Ctrl+O')
        self.hide_all()

    def open(self):
        new_filename = QFileDialog.getOpenFileName(
                self, 'Выбрать картинку', '',
                'Картинка (*.png);;Картинка (*.jpg);;Картинка (*.bmp)')[0]
        if new_filename != '':
            self.show_all()
            self.filename = new_filename
            pixmap = QPixmap(self.filename)
            self.imageplace.setPixmap(pixmap)

    def except_hook(self, cls, exception, traceback):
        self.errorwidget.showMessage(str(exception))
        sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.showMaximized()
    sys.excepthook = ex.except_hook
    sys.exit(app.exec())
