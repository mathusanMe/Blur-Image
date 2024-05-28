import os
import time
from utils import (
    load_image,
    save_image,
    calculate_psnr,
    print_blue,
    print_green,
    print_red,
    print_yellow,
    print_purple,
)
from image_processing.kernels import (
    kernel_average,
    kernel_gaussian,
)
from image_processing.fast_blind_richardson_lucy import FastBlindRichardsonLucy


class BlindImageProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def process_image(self, image_path, kernel_obj, iterations, psf_iterations):
        image = load_image(image_path)
        filename = os.path.splitext(os.path.basename(image_path))[0]
        image_output_folder = os.path.join(self.output_folder, filename)

        # Update the folder name to include the kernel information
        kernel_folder_name = str(kernel_obj)
        kernel_output_folder = os.path.join(image_output_folder, kernel_folder_name)

        if not os.path.exists(kernel_output_folder):
            os.makedirs(kernel_output_folder)

        print_purple(
            f"Unblurring image: {filename}, {iterations} iterations, {psf_iterations} PSF iterations"
        )
        start_time = time.time()
        blrl = FastBlindRichardsonLucy(image, kernel_obj.kernel, iterations, psf_iterations)
        unblurred_image = blrl.apply()

        # Calculate PSNR.
        psnr_value = calculate_psnr(image, unblurred_image)
        print_yellow(f"PSNR: {psnr_value:.2f} dB")

        duration = time.time() - start_time

        # Update the file name to include kernel, iteration, and PSF iteration information
        unblurred_image_filename = (
            f"{filename}_unblurred_{iterations}-iter_{psf_iterations}-psf-iter.png"
        )
        unblurred_image_path = os.path.join(
            kernel_output_folder, unblurred_image_filename
        )
        save_image(unblurred_image, unblurred_image_path)

        # Print the duration in a formatted way
        print_green(f"Completed in: {duration:.2f} seconds")
        print("")

    def process_folder(self, initial_psf_list, iterations_list, psf_iterations):
        for filename in os.listdir(self.input_folder):
            if filename.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
                print_blue(
                    f"############### Processing image: {filename} ###############"
                )
                image_path = os.path.join(self.input_folder, filename)

                for initial_psf in initial_psf_list:
                    for iterations in iterations_list:
                        self.process_image(
                            image_path, initial_psf, iterations, psf_iterations
                        )


if __name__ == "__main__":
    input_folder = "images/blind_originals"
    output_folder = "images/blind_processed"

    # The initial PSF is a guess and should be defined accordingly.
    # It could be a simple average kernel or a Gaussian, etc.
    initial_psf_list = [
        kernel_average(3),
        kernel_average(5),
        kernel_average(11),
        kernel_gaussian(5, 1.0),
        kernel_gaussian(5, 2.0),
    ]

    iterations_list = [
        15,
        30,
        60,
        120,
    ]  # Number of iterations for Blind Richardson-Lucy deconvolution
    psf_iterations = 5  # Number of PSF iterations during each main iteration

    processor = BlindImageProcessor(input_folder, output_folder)
    processor.process_folder(initial_psf_list, iterations_list, psf_iterations)
