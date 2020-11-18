from PIL import Image
import numpy as np


class Photo:
    def __init__(self, name_file):
        image = np.ndarray(Image.open('images/image0 (4).jpeg'))

        mask = image < 87
        image[mask] = 255
