import os
import numpy as np
from PIL import Image as PILImage

class Image:
    def __init__(self, f):
        self.width = f.columns
        self.height = f.rows
        self.matrix = f

    def save_image(self, path, file_name):
        image = PILImage.new('RGB', (self.width, self.height))
        pixels = image.getdata()

        new_pixels = []
        for x in range(self.width):
            for y in range(self.height):
                alpha = abs(self.matrix[x, y])
                new_pixels.append(tuple(int(c * 255) for c in colorsys.hsv_to_rgb(0, 0, alpha)))

        image.putdata(new_pixels)
        file_path = os.path.join(path, file_name)
        image.save(file_path, "PNG")
        return os.path.abspath(file_path)