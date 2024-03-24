import os
import numpy as np
from PIL import Image
from filters import apply_kernel, apply_kernel_unoptimized, kernel_gaussian, kernel_laplacian
from utils import load_image, save_image


def blur_images(input_folder, output_folder_blurred, kernel_size=5, optimized=True):
    """Applique un flou gaussien à toutes les images d'un dossier."""
    if not os.path.exists(output_folder_blurred):
        os.makedirs(output_folder_blurred)

    for filename in os.listdir(input_folder):
        if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            image_path = os.path.join(input_folder, filename)
            image = load_image(image_path)
            kernel = kernel_gaussian(size=kernel_size)
            if optimized:
                blurred_image = apply_kernel(image, kernel)
            else:
                blurred_image = apply_kernel_unoptimized(image, kernel)
            save_image(blurred_image, os.path.join(output_folder_blurred, filename))


def unblur_images(input_folder_blurred, output_folder_unblurred, optimized=True):
    """Tente d'appliquer un 'défloutage' aux images en utilisant un noyau laplacien."""
    if not os.path.exists(output_folder_unblurred):
        os.makedirs(output_folder_unblurred)

    for filename in os.listdir(input_folder_blurred):
        if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            image_path = os.path.join(input_folder_blurred, filename)
            image = load_image(image_path)
            kernel = kernel_laplacian()
            if optimized:
                unblurred_image = apply_kernel(image, kernel, border_handling="symm")
            else:
                unblurred_image = apply_kernel_unoptimized(image, kernel, border_handling="symm")
            save_image(unblurred_image, os.path.join(output_folder_unblurred, filename))


if __name__ == "__main__":

    # Version Optimisée
    # -----------------
    input_folder = "images/optimized/original"
    output_folder_blurred = "images/optimized/blurred"
    output_folder_unblurred = "images/optimized/unblurred"

    # Applique un flou aux images du dossier d'entrée et les sauvegarde
    blur_images(input_folder, output_folder_blurred, optimized=True)
    # Tente de 'déflouter' les images floutées en utilisant le noyau laplacien
    unblur_images(output_folder_blurred, output_folder_unblurred, optimized=True)

    # Version Non Optimisée
    # ---------------------
    input_folder = "images/unoptimized/original"
    output_folder_blurred = "images/unoptimized/blurred"
    output_folder_unblurred = "images/unoptimized/unblurred"

    # Applique un flou aux images du dossier d'entrée et les sauvegarde
    blur_images(input_folder, output_folder_blurred, optimized=False)
    # Tente de 'déflouter' les images floutées en utilisant le noyau laplacien
    unblur_images(output_folder_blurred, output_folder_unblurred, optimized=False)

