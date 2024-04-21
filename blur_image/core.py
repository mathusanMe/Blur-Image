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
from image_processing.kernels import kernel_average, kernel_gaussian, apply_kernel
from image_processing.richardson_lucy import RichardsonLucy


class ImageProcessor:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def process_image(self, image_path, kernel_obj, iterations_list):
        image = load_image(image_path)
        filename = os.path.basename(image_path)
        image_output_folder = os.path.join(
            self.output_folder, os.path.splitext(filename)[0]
        )

        kernel_folder_name = str(kernel_obj)
        kernel_output_folder = os.path.join(image_output_folder, kernel_folder_name)

        if not os.path.exists(kernel_output_folder):
            os.makedirs(kernel_output_folder)

        # Blurring
        print_red(f"Blurring image with {kernel_obj}")
        blurred_image = apply_kernel(image, kernel_obj.kernel, border_handling="wrap")
        blurred_image_path = os.path.join(kernel_output_folder, "blurred.png")
        save_image(blurred_image, blurred_image_path)

        # Unblurring with specified iterations
        for iterations in iterations_list:
            start_time = time.time()
            print_purple(f"Unblurring image with {kernel_obj} and {iterations} iterations")
            rl = RichardsonLucy(image, kernel_obj.kernel, iterations)
            unblurred_image = rl.apply()

            # Calculate PSNR.
            psnr_value = calculate_psnr(image, unblurred_image)
            print_yellow(f"PSNR: {psnr_value:.2f} dB")

            duration = time.time() - start_time
            unblurred_image_path = os.path.join(
                kernel_output_folder, f"unblurred_{iterations}-iter.png"
            )
            save_image(unblurred_image, unblurred_image_path)

            print_green(f"Completed in: {duration:.2f} seconds")
            print("--------------------------------------------------")

    def process_folder(self, kernels, iterations_list):
        for filename in os.listdir(self.input_folder):
            if filename.endswith((".png", ".jpg", ".jpeg", ".webp", ".gif")):
                print_blue(f"############### Processing image: {filename} ###############")
                image_path = os.path.join(self.input_folder, filename)
                image_output_folder = os.path.join(
                    self.output_folder, os.path.splitext(filename)[0]
                )

                if not os.path.exists(image_output_folder):
                    os.makedirs(image_output_folder)

                for kernel in kernels:
                    self.process_image(image_path, kernel, iterations_list)


if __name__ == "__main__":
    input_folder = "originals"
    output_folder = "processed"

    kernels = [
        kernel_average(3),
        kernel_average(5),
        kernel_average(11),
        kernel_gaussian(3, 1.0),
        kernel_gaussian(5, 1.0),
        kernel_gaussian(3, 2.0),
        kernel_gaussian(5, 2.0),
    ]

    iterations_list = [5, 10, 15]

    processor = ImageProcessor(input_folder, output_folder)
    processor.process_folder(kernels, iterations_list)
