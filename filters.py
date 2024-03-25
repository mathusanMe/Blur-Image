import numpy as np
from scipy.signal import convolve2d


def kernel_average(size=3):
    """Crée un noyau moyenneur."""
    return np.ones((size, size)) / (size * size)


def kernel_gaussian(size=3, sigma=1.0):
    """Crée un noyau gaussien."""
    ax = np.linspace(-(size - 1) / 2.0, (size - 1) / 2.0, size)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sigma))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel)


def kernel_laplacian():
    """Crée un noyau laplacien."""
    return np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])


def apply_kernel(image_array, kernel, border_handling="fill"):
    """
    Applique un noyau spécifique à une image.

    Args:
        image_array: tableau NumPy représentant l'image
        kernel: noyau à appliquer
        border_handling: méthode de gestion des bords (fill, wrap, symm)
    Returns:
        image filtrée
    """
    if image_array.ndim == 3:  # Images en couleur
        # Appliquer le filtre sur chaque canal
        result = np.zeros_like(image_array)
        for i in range(3):  # Traitement canal par canal
            result[:, :, i] = convolve2d(
                image_array[:, :, i], kernel, mode="same", boundary=border_handling
            )
    else:  # Images en niveaux de gris
        result = convolve2d(image_array, kernel, mode="same", boundary=border_handling)
    return result
