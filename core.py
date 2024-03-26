import os
from filters import apply_kernel, kernel_gaussian
from utils import load_image, save_image


def blur_images(input_folder, output_folder_blurred, kernel_size=5):
    """Applique un flou gaussien à toutes les images d'un dossier."""
    if not os.path.exists(output_folder_blurred):
        os.makedirs(output_folder_blurred)

    for filename in os.listdir(input_folder):
        if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            image_path = os.path.join(input_folder, filename)
            image = load_image(image_path)
            kernel = kernel_gaussian(size=kernel_size)
            blurred_image = apply_kernel(image, kernel, border_handling="wrap")
            save_image(blurred_image, os.path.join(output_folder_blurred, filename))


if __name__ == "__main__":

    input_folder = "images/original"
    output_folder_blurred = "images/processed/blurred"
    output_folder_unblurred = "images/processed/unblurred"

    # Applique un flou aux images du dossier d'entrée et les sauvegarde
    blur_images(input_folder, output_folder_blurred)
