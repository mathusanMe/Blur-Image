import numpy as np


class Kernel:
    def __init__(self, name, kernel):
        """
        Create a new Kernel object with a given name and kernel matrix.

        :param name: The name of the kernel.
        :type name: str
        :param kernel: The kernel matrix.
        :type kernel: ndarray
        """
        self.name = name.lower()
        self.kernel = kernel


### KERNEL FUNCTIONS ###


def kernel_average(size=3):
    """
    Creates an averaging kernel: a matrix where all elements have equal value, contributing equally to the output.
    It smooths the image by averaging the pixels under the kernel area.

    :param size: The size of the kernel. Must be an odd number.
    :type size: int
    :return: An instance of the Kernel class representing the averaging kernel.
    :rtype: Kernel
    :raises ValueError: If the kernel size is not an odd number.
    """
    if size % 2 == 0:
        raise ValueError("Kernel size must be an odd number.")

    kernel_matrix = np.ones((size, size)) / (size * size)
    return Kernel(f"average_{size}x{size}", kernel_matrix)


def kernel_gaussian(size=3, sigma=1.0):
    """
    Creates a Gaussian kernel: a matrix where the central elements have higher values with a decrease towards the edges,
    following a Gaussian distribution. It reduces noise and details in the image.

    :param size: The size of the kernel. Must be an odd number.
    :type size: int
    :param sigma: The standard deviation of the Gaussian distribution.
    :type sigma: float
    :return: An instance of the Kernel class representing the Gaussian kernel.
    :rtype: Kernel
    :raises ValueError: If the kernel size is not an odd number.
    """
    if size % 2 == 0:
        raise ValueError("Kernel size must be an odd number.")

    ax = np.linspace(-(size - 1) / 2.0, (size - 1) / 2.0, size)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sigma))
    kernel_matrix = np.outer(gauss, gauss)
    kernel_matrix /= np.sum(kernel_matrix)
    return Kernel(f"gaussian_{size}x{size}_sigma{sigma}", kernel_matrix)


def apply_kernel(image_array, kernel, border_handling="fill", fill_value=0):
    """
    Applies a specific kernel to an image.

    This function applies a convolution operation between the given image and kernel,
    allowing for different methods of handling the image borders.

    :param image_array: A NumPy array representing the image. It can be either grayscale or color (3 channels).
    :type image_array: numpy.ndarray
    :param kernel: The kernel to apply as part of the convolution process.
    :type kernel: numpy.ndarray
    :param border_handling: Method for handling the borders of the image. Options include "fill", "wrap", or "symm" for filling with a specific value, wrapping around, or using symmetric padding, respectively.
    :type border_handling: str
    :param fill_value: The value to use when filling the borders if border_handling is set to "fill". Default is 0.
    :type fill_value: int or float
    :return: The filtered image as a NumPy array.
    :rtype: numpy.ndarray

    The method implements convolution by creating a padded version of the input image according to the specified border handling method and then applying the kernel to every pixel (or block of pixels in case of color images) in the original image.
    """
    kernel_height, kernel_width = kernel.shape
    image_height, image_width = image_array.shape[:2]

    # Calculate the required dimensions for padding
    pad_height_top = kernel_height // 2
    pad_height_bottom = kernel_height - pad_height_top - 1
    pad_width_left = kernel_width // 2
    pad_width_right = kernel_width - pad_width_left - 1

    # Create an enlarged image filled with zeros (or with the appropriate value for other border handling modes)
    padded_height = image_height + pad_height_top + pad_height_bottom
    padded_width = image_width + pad_width_left + pad_width_right

    if image_array.ndim == 3:  # For color images
        padded_image = np.zeros((padded_height, padded_width, image_array.shape[2]))
    else:  # For grayscale images
        padded_image = np.zeros((padded_height, padded_width))

    # Copy the original image into the center of the enlarged image
    padded_image[pad_height_top:-pad_height_bottom, pad_width_left:-pad_width_right] = (
        image_array
    )

    # Handle borders according to the specified method
    if border_handling == "fill":
        # Fill the borders with a specific value
        padded_image[:pad_height_top, :] = fill_value
        padded_image[-pad_height_bottom:, :] = fill_value
        padded_image[:, :pad_width_left] = fill_value
        padded_image[:, -pad_width_right:] = fill_value
    elif border_handling == "wrap":
        # Wrap the borders around
        padded_image[:pad_height_top, :] = padded_image[-pad_height_top - 1 : -1, :]
        padded_image[-pad_height_bottom:, :] = padded_image[
            1 : pad_height_bottom + 1, :
        ]
        padded_image[:, :pad_width_left] = padded_image[:, -pad_width_left - 1 : -1]
        padded_image[:, -pad_width_right:] = padded_image[:, 1 : pad_width_right + 1]
    elif border_handling == "symm":
        # Symmetrically pad the horizontal edges
        padded_image[:pad_height_top, pad_width_left:-pad_width_right] = np.flipud(
            image_array[:pad_height_top, :]
        )
        padded_image[-pad_height_bottom:, pad_width_left:-pad_width_right] = np.flipud(
            image_array[-pad_height_bottom:, :]
        )

        # Symmetrically pad the vertical edges
        padded_image[kernel_height // 2 : -pad_height_bottom, :pad_width_left] = (
            np.fliplr(image_array[:, :pad_width_left])
        )
        padded_image[kernel_height // 2 : -pad_height_bottom, -pad_width_right:] = (
            np.fliplr(image_array[:, -pad_width_right:])
        )

        # Corners
        # Top left
        padded_image[:pad_height_top, :pad_width_left] = np.flipud(
            np.fliplr(image_array[:pad_height_top, :pad_width_left])
        )
        # Top right
        padded_image[:pad_height_top, -pad_width_right:] = np.flipud(
            np.fliplr(image_array[:pad_height_top, -pad_width_right:])
        )
        # Bottom left
        padded_image[-pad_height_bottom:, :pad_width_left] = np.flipud(
            np.fliplr(image_array[-pad_height_bottom:, :pad_width_left])
        )
        # Bottom right
        padded_image[-pad_height_bottom:, -pad_width_right:] = np.flipud(
            np.fliplr(image_array[-pad_height_bottom:, -pad_width_right:])
        )

    # Perform convolution
    result = np.zeros_like(image_array)
    for i in range(image_height):
        for j in range(image_width):
            if image_array.ndim == 3:  # For each color channel
                for k in range(image_array.shape[2]):
                    result[i, j, k] = np.sum(
                        padded_image[i : i + kernel_height, j : j + kernel_width, k]
                        * kernel
                    )
            else:  # Grayscale image
                result[i, j] = np.sum(
                    padded_image[i : i + kernel_height, j : j + kernel_width] * kernel
                )

    return result
