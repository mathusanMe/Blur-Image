import numpy as np
from PIL import Image


def load_image(image_path, grayscale=False):
    """Charge une image et la convertit en niveaux de gris si demandé."""
    image = Image.open(image_path)
    if grayscale:
        image = image.convert("L")
    else:
        image = image.convert("RGB")
    return np.array(image)


def save_image(image_array, output_path):
    """Sauvegarde une image à partir d'un tableau NumPy."""
    image = Image.fromarray(image_array)
    image.save(output_path)


def show_image(image_array):
    """Affiche une image à partir d'un tableau NumPy."""
    image = Image.fromarray(image_array)
    image.show()
