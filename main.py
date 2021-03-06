import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QFileDialog, QInputDialog, QErrorMessage
from grafix import Ui_MainWindow
from PhotoMainClass import Photo


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.first = False
        self.koeffs_arr = {'new_2': [0, 0, 10],
                           'hightlight': [0, 3, 5],
                           'brillance': [100, 3, 100]}
        self.selected_filter = None
        self.setupUi(self)
        self.count_main_change = 0
        self.errorwidget = QErrorMessage(self)
        self.centralwidget.setLayout(self.verticalLayout_3)
        self.filters_name = ['negative', 'gray', 'warm', 'cold', 'real', 'change_chanels']
        self.objectsnames = []
        self.undofiles = []
        self.FILENAME = 'data_change/NEW.png'
        self.this_photo = Photo()
        self.hide_objects = {self.verticalLayout: [self.new_2, self.brillance,
                                                   self.hightlight],
                             self.verticalLayout_4: [self.mirror, self.rotate_90],
                             self.verticalLayout_2: [self.label_1, self.label_2,
                                                     self.label_3, self.label_4,
                                                     self.label_5, self.label_6]}
        [obj.hide() for obj in self.hide_objects[self.verticalLayout_4]]
        [obj.hide() for obj in self.hide_objects[self.verticalLayout_2]]
        self.connect_widgets()
        self.style_sheet()
        self.filter_photo()
        self.open()

    def style_sheet(self):
        [obj.clicked.connect(self.more_good_file) for obj in self.hide_objects[self.verticalLayout]]
        [obj.setAlignment(Qt.AlignCenter) for obj in self.hide_objects[self.verticalLayout_2]]
        self.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.imageplace.setStyleSheet("color: rgb(255, 255, 255)")
        self.menubar.setStyleSheet("color: rgb(255, 255, 255)")
        for objs in self.hide_objects.items():
            for obj in objs[1]:
                obj.setAlignment(Qt.AlignCenter)

    def connect_widgets(self):
        self.openphotoact.changed.connect(self.open)
        self.closephotoact.changed.connect(self.close)
        self.renamephotoact.changed.connect(self.rename)
        self.savephotoact.changed.connect(self.save)
        self.reverse.clicked.connect(self.reverse_image)
        self.edits.clicked.connect(self.edit_image)
        self.filters.clicked.connect(self.filter_photo)
        self.valuegforeditor.valueChanged.connect(self.re_edit_photo)
        self.rotate_90.clicked.connect(self.flip_90)
        self.mirror.clicked.connect(self.flip_to_bottom)

    def flip_90(self):
        self.this_photo.flip_90()
        self.update_main_photo('data_change/NEW.png', True)

    def flip_to_bottom(self):
        self.this_photo.flip_to_bottom()
        self.update_main_photo('data_change/NEW.png', True)

    def filter_photo(self):
        [obj.hide() for obj in self.hide_objects[self.verticalLayout_4]]
        [obj.hide() for obj in self.hide_objects[self.verticalLayout]]
        [obj.show() for obj in self.hide_objects[self.verticalLayout_2]]

    def update_photo_filter(self):
        for i, name_filter in enumerate(self.filters_name):
            name_file = f'cash_image/min_{name_filter}'
            exec(f'self.label_{i + 1}.setPixmap(QPixmap(name_file))')
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
        endsfiles = ['.png', '.jpg', '.bmp', '.jpeg']
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
                'Картинка (*.png;*.jpg;*.bmp;*.jpeg)')[0]
        if new_filename != '':
            file_name_for_main = new_filename[new_filename.rfind('/') + 1:]
            self.undofiles.append(new_filename)
            QPixmap(new_filename).save('data_change/' + file_name_for_main)
            self.update_main_photo(new_filename, True)
            self.count_main_change += 1

    def update_main_photo(self, new_filename, update=False):
        pixmap = QPixmap(new_filename)
        pixmap.save(self.FILENAME)
        x, y = pixmap.size().width(), pixmap.size().height()
        procent = min((100 * 800) / x, (100 * 800) / y) / 100
        self.imageplace.setPixmap(pixmap.scaled(int(procent * x), int(procent * y)))
        self.this_photo = Photo(self.FILENAME) if update else self.this_photo
        self.update_photo_filter() if update else None

    def more_good_file(self):
        self.selected_filter = self.sender().objectName()
        print(self.koeffs_arr[self.selected_filter])
        self.valuegforeditor.setMinimum(self.koeffs_arr[self.selected_filter][1])
        self.valuegforeditor.setMaximum(self.koeffs_arr[self.selected_filter][2])
        self.valuegforeditor.setValue(self.koeffs_arr[self.selected_filter][0])
        self.first = False

    def re_edit_photo(self):
        if self.selected_filter is not None and self.first:
            koeff = self.valuegforeditor.value()
            print(koeff)
            print(self.selected_filter, 're edit')
            if self.selected_filter == 'new_2':
                self.this_photo.change_gaussian(koeff)
            elif self.selected_filter == 'hightlight':
                self.this_photo.gray_photo_with_koeff(koeff)
            elif self.selected_filter == 'brillance':
                self.this_photo.quantize(koeff)
            self.update_main_photo('data_change/NEW.png', True)
        elif not self.first:
            self.first = True

    def except_hook(self, cls, exception, traceback):
        self.errorwidget.showMessage(str(exception))
        sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.showMaximized()
    sys.excepthook = ex.except_hook
    sys.exit(app.exec())
