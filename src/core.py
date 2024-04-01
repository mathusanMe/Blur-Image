import os
from utils import load_image, save_image

from kernels import Kernel, kernel_average, kernel_gaussian
from image_processing.convolve2d import apply_kernel
from image_processing.richardson_lucy import RichardsonLucy


def process_images(
    input_folder, output_folder, kernel_inst: Kernel, action, iterations=10
):
    """
    Process images by blurring or unblurring based on the given action.

    :param input_folder: The folder containing the images to process.
    :type input_folder: str
    :param output_folder: The folder where processed images will be saved.
    :type output_folder: str
    :param kernel_inst: The kernel instance to use for blurring or unblurring.
    :type kernel_inst: Kernel
    :param action: The action to perform - either "blur" or "unblur".
    :type action: str
    :raises ValueError: If an invalid action is specified.
    """
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
            image_path = os.path.join(input_folder, filename)
            image = load_image(image_path)

            if action == "blur":
                # Apply blurring
                processed_image = apply_kernel(
                    image, kernel_inst.kernel, border_handling="wrap"
                )
            elif action == "unblur":
                # Apply unblurring (deconvolution)
                rl = RichardsonLucy(image, kernel_inst.kernel, iterations)
                processed_image = rl.apply()
            else:
                raise ValueError(
                    "Invalid action specified. Choose either 'blur' or 'unblur'."
                )

            # Split the filename and extension
            splitted_filename = os.path.splitext(filename)
            filename_only, extension = (
                "".join(splitted_filename[:-1]),
                splitted_filename[-1],
            )

            # Save the processed image
            save_image(
                processed_image,
                os.path.join(
                    output_folder,
                    f"{filename_only}_{(kernel_inst.name).lower()}_{action}{extension}",
                ),
            )


if __name__ == "__main__":

    input_folder = "resources"
    output_folder_blurred = "processed/blurred"
    output_folder_unblurred = "processed/unblurred"

    # Define the kernel to use for blurring and unblurring
    kernels = [
        kernel_gaussian(size=5, sigma=1.0),
        # kernel_gaussian(size=5, sigma=2.0),
        # kernel_average(size=3),
        # kernel_average(size=5),
    ]

    # Apply a blur to the images in the input folder and save them
    for kernel in kernels:
        process_images(input_folder, output_folder_blurred, kernel, "blur")

    # Apply an unblur to the blurred images and save them
    for kernel in kernels:
        process_images(
            output_folder_blurred,
            output_folder_unblurred,
            kernel,
            "unblur",
            iterations=10,
        )
