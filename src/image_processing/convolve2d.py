import numpy as np
from kernels import Kernel


def apply_kernel(image_array, kernel, border_handling="fill", fill_value=0):
    """
    Applique un noyau spécifique à une image.

    Args:
        image_array: tableau NumPy représentant l'image
        kernel: noyau à appliquer
        border_handling: méthode de gestion des bords (fill, wrap, symm)
    Returns:
        image filtrée
    """
    kernel_height, kernel_width = kernel.shape
    image_height, image_width = image_array.shape[:2]

    # Calculer les dimensions nécessaires pour le padding
    pad_height_top = kernel_height // 2
    pad_height_bottom = kernel_height - pad_height_top - 1
    pad_width_left = kernel_width // 2
    pad_width_right = kernel_width - pad_width_left - 1

    # Créer une image agrandie avec des zéros (ou avec la valeur appropriée pour d'autres modes de gestion des bords)
    padded_height = image_height + pad_height_top + pad_height_bottom
    padded_width = image_width + pad_width_left + pad_width_right

    if image_array.ndim == 3:  # Images en couleur
        padded_image = np.zeros((padded_height, padded_width, image_array.shape[2]))
    else:  # Images en niveaux de gris
        padded_image = np.zeros((padded_height, padded_width))

    # Copier l'image originale dans le centre de l'image agrandie
    padded_image[pad_height_top:-pad_height_bottom, pad_width_left:-pad_width_right] = (
        image_array
    )

    # Gestion des bordures
    if border_handling == "fill":
        # Remplir les bords avec une valeur spécifique
        padded_image[:pad_height_top, :] = fill_value
        padded_image[-pad_height_bottom:, :] = fill_value
        padded_image[:, :pad_width_left] = fill_value
        padded_image[:, -pad_width_right:] = fill_value
    elif border_handling == "wrap":
        # Enrouler les bords
        padded_image[:pad_height_top, :] = padded_image[-pad_height_top:, :]
        padded_image[-pad_height_bottom:, :] = padded_image[
            1 : pad_height_bottom + 1, :
        ]
        padded_image[:, :pad_width_left] = padded_image[:, -pad_width_left - 1 : -1]
        padded_image[:, -pad_width_right:] = padded_image[:, 1 : pad_width_right + 1]
    elif border_handling == "symm":
        # Symétrie horizontale
        padded_image[kernel_height // 2 : -pad_height_bottom, :pad_width_left] = (
            np.fliplr(image_array[:, :pad_width_left])
        )
        padded_image[kernel_height // 2 : -pad_height_bottom, -pad_width_right:] = (
            np.fliplr(image_array[:, -pad_width_right:])
        )

        # Symétrie verticale
        padded_image[:pad_height_top, pad_width_left:-pad_width_right] = np.flipud(
            image_array[:pad_height_top, :]
        )
        padded_image[-pad_height_bottom:, pad_width_left:-pad_width_right] = np.flipud(
            image_array[-pad_height_bottom:, :]
        )

        # Coins
        # Supérieur gauche
        padded_image[:pad_height_top, :pad_width_left] = np.flipud(
            np.fliplr(image_array[:pad_height_top, :pad_width_left])
        )
        # Supérieur droit
        padded_image[:pad_height_top, -pad_width_right:] = np.flipud(
            np.fliplr(image_array[:pad_height_top, -pad_width_right:])
        )
        # Inférieur gauche
        padded_image[-pad_height_bottom:, :pad_width_left] = np.flipud(
            np.fliplr(image_array[-pad_height_bottom:, :pad_width_left])
        )
        # Inférieur droit
        padded_image[-pad_height_bottom:, -pad_width_right:] = np.flipud(
            np.fliplr(image_array[-pad_height_bottom:, -pad_width_right:])
        )

    # Convolution
    result = np.zeros_like(image_array)
    for i in range(image_height):
        for j in range(image_width):
            for k in range(image_array.shape[2]):  # Pour chaque canal de couleur
                result[i, j, k] = np.sum(
                    padded_image[i : i + kernel_height, j : j + kernel_width, k]
                    * kernel
                )

    return result


def convolve2d(image, kernel, mode="same", boundary="wrap"):
    """
    Manually apply a convolution kernel to an image, ensuring it mimics the behavior of scipy.signal.convolve2d,
    including handling of boundary conditions and flipping the kernel for convolution.

    Parameters:
    - image: A 2D numpy array representing the grayscale image.
    - kernel: A 2D numpy array representing the convolution kernel.

    Returns:
    - output: A 2D numpy array representing the convolved image.
    """

    kernel = np.flipud(np.fliplr(kernel))  # Flip the kernel
    output = np.zeros_like(image)  # Prepare the output array

    # Determine padding width
    if mode == "same":
        pad_height = kernel.shape[0] // 2
        pad_width = kernel.shape[1] // 2
        padded_image = np.pad(
            image, ((pad_height, pad_height), (pad_width, pad_width)), mode=boundary
        )
    else:
        # For simplicity, other modes are not implemented
        raise ValueError(
            "Unsupported mode. Only 'same' is supported with 'wrap' boundary condition."
        )

    # Convolve the padded image with the kernel
    for x in range(image.shape[1]):  # Loop over every pixel of the image
        for y in range(image.shape[0]):
            # Extract the current region of interest
            region = padded_image[y : y + kernel.shape[0], x : x + kernel.shape[1]]
            output[y, x] = np.sum(region * kernel)

    return output
