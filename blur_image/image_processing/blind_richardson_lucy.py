import numpy as np
from scipy.signal import fftconvolve
import math


class BlindRichardsonLucy:
    def __init__(self, image, initial_psf, iterations=10, psf_iterations=5):
        self.image = image.astype(np.float64)
        self.psf = initial_psf
        self.iterations = iterations
        self.psf_iterations = psf_iterations
        self.psf_mirror = np.flipud(np.fliplr(self.psf))  # Precompute the mirrored PSF

    def apply(self):
        if self.image.ndim == 3:
            channels = [self._apply_to_channel(self.image[:, :, i]) for i in range(3)]
            deblurred_image = np.stack(channels, axis=-1)
        else:
            deblurred_image = self._apply_to_channel(self.image)
        return deblurred_image.astype(np.uint8)

    def _apply_to_channel(self, channel):
        estimate = np.copy(channel)
        for _ in range(self.iterations):
            convolved_estimate = self._convolve2d(estimate, self.psf)
            relative_blur = channel / (convolved_estimate + 1e-12)
            error_estimate = self._convolve2d(relative_blur, self.psf_mirror)
            estimate *= error_estimate
        self._update_psf(channel, estimate)
        return estimate

    def _update_psf(self, original, estimate):
        flipped_estimate = np.flipud(
            np.fliplr(estimate)
        )  # Precompute the flipped estimate once per iteration
        for _ in range(self.psf_iterations):
            estimated_convolution = self._convolve2d(estimate, self.psf)
            error_ratio = original / (estimated_convolution + 1e-12)
            full_psf_update = self._convolve2d(error_ratio, flipped_estimate)

            # Crop to match the PSF size
            psf_update = self._crop_center(full_psf_update, self.psf.shape)
            self.psf *= psf_update
            self.psf /= np.sum(self.psf)  # Normalize PSF to maintain energy

    def _convolve2d(self, image, kernel):
        # Compute padding widths
        pad_height = kernel.shape[0] // 2
        pad_width = kernel.shape[1] // 2

        # Manually wrap the boundary by padding
        padded_image = np.pad(
            image, ((pad_height, pad_height), (pad_width, pad_width)), mode="wrap"
        )

        # Perform FFT-based convolution on the padded image
        result = fftconvolve(padded_image, kernel, mode="same")

        # Crop the result back to the original image size
        result_cropped = result[pad_height:-pad_height, pad_width:-pad_width]

        return result_cropped

    def _crop_center(self, img, cropsize):
        y, x = img.shape
        cropx, cropy = cropsize
        startx = x // 2 - (cropx // 2)
        starty = y // 2 - (cropy // 2)
        return img[starty : starty + cropy, startx : startx + cropx]

    def calculate_psnr(self, original, reconstructed):
        """
        Calculate the PSNR between the original and reconstructed images.

        :param original: Original image data as a numpy array.
        :param reconstructed: Reconstructed (deblurred) image data as a numpy array.
        :return: PSNR value in decibels (dB).
        """
        mse = np.mean((original - reconstructed) ** 2)
        if mse == 0:  # MSE is zero means no noise is present in the signal.
            # Therefore PSNR is 100.
            return 100
        max_pixel = 255.0
        psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
        return psnr
