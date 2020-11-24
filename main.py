import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QFileDialog, QInputDialog, QErrorMessage
from grafix import Ui_MainWindow
from PhotoMainClass import Photo


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.selected_filter = None
        self.setupUi(self)
        self.count_main_change = 0
        self.errorwidget = QErrorMessage(self)
        self.centralwidget.setLayout(self.verticalLayout_3)
        self.filters_name = ['negative', 'gray', 'warm', 'cold', 'real', 'change_chanels']
        self.objectsnames = []
        self.undofiles = []
        self.FILENAME = 'data_change/NEW.png'
        self.this_photo = None
        self.hide_objects = {self.verticalLayout: [self.new_2, self.brillance,
                                                   self.contrast, self.hightlight,
                                                   self.exposure],
                             self.verticalLayout_4: [self.mirror, self.rotate_90],
                             self.verticalLayout_2: [self.label_1, self.label_2,
                                                     self.label_3, self.label_4,
                                                     self.label_5, self.label_6]}
        [obj.hide() for obj in self.hide_objects[self.verticalLayout_4]]
        [obj.hide() for obj in self.hide_objects[self.verticalLayout_2]]
        self.connect_widgets()
        self.style_sheet()
        self.open()

    def style_sheet(self):
        [obj.clicked.connect(self.more_good_file) for obj in self.hide_objects[self.verticalLayout]]
        [obj.setAlignment(Qt.AlignCenter) for obj in self.hide_objects[self.verticalLayout_2]]
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.imageplace.setStyleSheet("color: rgb(255, 255, 255)")
        #self.openphotoact.setFont(QFont("color: rgb(255, 255, 255)"))
        self.imageplace.setAlignment(Qt.AlignCenter)
        self.filters.setAlignment(Qt.AlignCenter)
        self.edits.setAlignment(Qt.AlignCenter)
        self.reverse.setAlignment(Qt.AlignCenter)

    def connect_widgets(self):
        self.openphotoact.changed.connect(self.open)
        self.closephotoact.changed.connect(self.close)
        self.renamephotoact.changed.connect(self.rename)
        self.savephotoact.changed.connect(self.save)
        self.reverse.clicked.connect(self.reverse_image)
        self.edits.clicked.connect(self.edit_image)
        self.filters.clicked.connect(self.filter_photo)
        self.valuegforeditor.valueChanged.connect(self.re_edit_photo)

    def filter_photo(self):
        [obj.hide() for obj in self.hide_objects[self.verticalLayout_4]]
        [obj.hide() for obj in self.hide_objects[self.verticalLayout]]
        [obj.show() for obj in self.hide_objects[self.verticalLayout_2]]

    def update_photo_filter(self):
        for i, name_filter in enumerate(self.filters_name):
            name_file = f'cash_image/min_{name_filter}'
            pixmap = QPixmap(name_file)
            exec(f'self.label_{i + 1}.setPixmap(pixmap)')
            exec(f'self.label_{i + 1}.clicked.connect(self.photo_selected)')
            print(name_file, 'up to date')

    def photo_selected(self):
        name_filter = self.filters_name[int(self.sender().objectName()[-1]) - 1]
        name_file = f'cash_image/{name_filter}'
        print(name_file, 'photo_selected')
        self.update_main_photo(name_file)

    def edit_image(self):
        [obj.hide() for obj in self.hide_objects[self.verticalLayout_4]]
        [obj.hide() for obj in self.hide_objects[self.verticalLayout_2]]
        [obj.show() for obj in self.hide_objects[self.verticalLayout]]

    def reverse_image(self):
        [obj.hide() for obj in self.hide_objects[self.verticalLayout]]
        [obj.hide() for obj in self.hide_objects[self.verticalLayout_2]]
        [obj.show() for obj in self.hide_objects[self.verticalLayout_4]]

    def save(self):
        print(self.FILENAME, self.undofiles[-1])
        QPixmap(self.FILENAME).save(self.undofiles[-1])

    def rename(self):
        endsfiles = ['.png', '.jpg', '.bmp']
        name, ok_pressed = QInputDialog.getText(self, "Ввод нового имени файла",
                                                "Введите новое имя файла")
        while ok_pressed and not any([name.endswith(endfile) for endfile in endsfiles]):
            name, ok_pressed = QInputDialog.getText(self, "Ввод нового имени файла",
                                                    "Введите новое имя файла(вместе с его расширением)")
        if ok_pressed:
            QPixmap(self.undofiles[-1]).save('data_change/' + name)
            self.undofiles[-1] = self.undofiles[-1][:self.undofiles[-1].rfind('/') + 1] + name

    def open(self):
        new_filename = QFileDialog.getOpenFileName(
                self, 'Выбрать картинку', '',
                'Картинка (*.png);;Картинка (*.jpg);;Картинка (*.bmp);;Картинка (*.jpeg)')[0]
        if new_filename != '':
            file_name_for_main = new_filename[new_filename.rfind('/') + 1:]
            self.undofiles.append(new_filename)
            QPixmap(new_filename).save('data_change/' + file_name_for_main)
            self.update_main_photo(new_filename, True)
            self.count_main_change += 1

    def update_main_photo(self, new_filename, update=False):
        pixmap = QPixmap(new_filename)
        pixmap.save(self.FILENAME)
        self.imageplace.setPixmap(pixmap)
        self.this_photo = Photo(self.FILENAME) if update else self.this_photo
        self.update_photo_filter() if update else None

    def more_good_file(self):
        self.selected_filter = self.sender().objectName()

    def re_edit_photo(self):
        koeff = self.valuegforeditor.value()
        print(self.selected_filter, 're edit')
        if self.selected_filter == 'new_2':
            self.this_photo.change_gaussian(koeff)
        self.update_main_photo('data_change/NEW.png', True)

    def except_hook(self, cls, exception, traceback):
        self.errorwidget.showMessage(str(exception))
        sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.showMaximized()
    sys.excepthook = ex.except_hook
    sys.exit(app.exec())
