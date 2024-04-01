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
