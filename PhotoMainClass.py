from PIL import Image, ImageFilter
import numpy as np


def save_image(filter_name, image):
    print(f'cash_image/{filter_name}.png', 'photo')
    image.save(f'cash_image/{filter_name}.png')
    image = image.resize((130, 130))
    image.save(f'cash_image/min_{filter_name}.png')


class Photo:
    def __init__(self, name_file):
        print(name_file, 'photo')
        self.image_pil = Image.open(name_file)
        self.image_array = np.array(self.image_pil)
        self.save_all_in_cash()

    def save_all_in_cash(self):
        self.negative_photo()
        save_image('real', self.image_pil)
        self.warm_photo()
        self.gray_photo()
        self.cold_photo()
        self.change_chanels()

    def change_chanels(self):
        picture = self.image_array[:]
        mask_0 = picture[:, :, 0] < 200
        mask_1 = picture[:, :, 1] < 200
        mask_2 = picture[:, :, 2] < 200
        mask_00 = picture[:, :, 0] >= 200
        mask_11 = picture[:, :, 1] >= 200
        mask_22 = picture[:, :, 2] >= 200
        picture[mask_0] += 50
        picture[mask_1] += 50
        picture[mask_2] += 50
        picture[mask_00] = 255
        picture[mask_11] = 255
        picture[mask_22] = 255
        image = Image.fromarray(picture)
        save_image('change_chanels', image)

    def negative_photo(self):
        picture = self.image_array[:]
        picture[:, :, 0] = 255 - picture[:, :, 0]
        picture[:, :, 1] = 255 - picture[:, :, 1]
        picture[:, :, 2] = 255 - picture[:, :, 2]
        image = Image.fromarray(picture)
        save_image('negative', image)

    def gray_photo(self):
        picture = self.image_array[:]
        summa = picture[:, :, 0] + picture[:, :, 1] + picture[:, :, 2]
        picture[:, :, 0] = summa // 3
        picture[:, :, 1] = summa // 3
        picture[:, :, 2] = summa // 3
        image = Image.fromarray(picture)
        save_image('gray', image)

    def warm_photo(self):
        picture = self.image_array[:]
        picture[:, :, 0] = 255
        picture[:, :, 2] = 200
        image = Image.fromarray(picture)
        save_image('warm', image)

    def cold_photo(self):
        picture = self.image_array[:]
        picture[:, :, 2] = 255
        image = Image.fromarray(picture)
        save_image('cold', image)

    def change_gaussian(self, radius):
        im2 = self.image_pil.filter(ImageFilter.GaussianBlur(radius=radius))
        im2.save('data_change/NEW.png')
