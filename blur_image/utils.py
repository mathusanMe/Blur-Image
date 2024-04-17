import numpy as np
from PIL import Image


def load_image(image_path, grayscale=False):
    """
    Loads an image from a specified path and optionally converts it to grayscale.

    :param image_path: The path to the image to be loaded.
    :type image_path: str
    :param grayscale: Flag indicating whether to convert the image to grayscale. Default is False.
    :type grayscale: bool
    :return: The loaded image as a NumPy array. If `grayscale` is True, the image will be 2D, otherwise 3D.
    :rtype: numpy.ndarray
    """
    image = Image.open(image_path)
    if grayscale:
        image = image.convert("L")
    else:
        image = image.convert("RGB")
    return np.array(image)


def save_image(image_array, file_path):
    """
    Saves a NumPy array as an image to the specified path. The function handles normalization and ensures that the image data
    is in the correct dtype and shape for saving.

    :param image_array: The image data as a NumPy array.
    :type image_array: numpy.ndarray
    :param file_path: The path where the image will be saved.
    :type file_path: str
    :raises ValueError: If the image shape or channels are unsupported.
    """
    # Ensure the image data is in the right dtype and scale
    if image_array.dtype != np.uint8:
        # Normalize and scale if not already uint8
        image_array = (
            255
            * (
                (image_array - image_array.min())
                / (image_array.max() - image_array.min())
            )
        ).astype(np.uint8)

    # Ensure the shape is correct (for this example, assuming RGB)
    if image_array.ndim == 3 and image_array.shape[2] == 1:
        # If the image is actually grayscale but shaped (height, width, 1), we convert it to (height, width)
        image_array = image_array.reshape(image_array.shape[:2])
    elif image_array.ndim == 2 or (image_array.ndim == 3 and image_array.shape[2] == 3):
        # If the shape is correct, do nothing special. This includes grayscale (height, width) and RGB (height, width, 3).
        pass
    else:
        # If the array shape does not meet the expected conditions, raise an error or handle accordingly.
        raise ValueError("Unsupported image shape or channels.")

    # Create and save the image
    image = Image.fromarray(image_array)
    image.save(file_path)


def show_image(image_array):
    """
    Displays an image from a NumPy array.

    :param image_array: The image data to be displayed, as a NumPy array.
    :type image_array: numpy.ndarray
    """
    image = Image.fromarray(image_array)
    image.show()


def print_red(string):
    # Red color
    print("\033[1;31m" + string + "\033[0m")


def print_green(string):
    # Bright green color
    print("\033[1;32m" + string + "\033[0m")


def print_yellow(string):
    # Yellow color
    print("\033[1;33m" + string + "\033[0m")


def print_blue(string):
    # Blue color
    print("\033[1;34m" + string + "\033[0m")
