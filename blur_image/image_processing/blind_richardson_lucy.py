import numpy as np
from scipy.signal import fftconvolve


class BlindRichardsonLucy:
    def __init__(self, image, initial_psf, iterations=10, psf_iterations=5):
        """
        Initialize the BlindRichardsonLucy deconvolution class with the target image,
        an initial point spread function (PSF), and the number of iterations for both
        the image deconvolution and PSF estimation.

        :param image: Input image as a numpy array.
        :param initial_psf: Initial guess for the point spread function.
        :param iterations: Number of iterations for the deconvolution process.
        :param psf_iterations: Number of iterations for refining the PSF.
        """
        self.image = image.astype(np.float64)
        self.psf = initial_psf
        self.iterations = iterations
        self.psf_iterations = psf_iterations
        self.psf_mirror = np.flipud(np.fliplr(self.psf))  # Precompute the mirrored PSF

    def apply(self):
        """
        Deblurs the image using the Richardson-Lucy deconvolution algorithm. This method supports both grayscale
        and color images by processing each channel separately if necessary.

        :return: The deblurred image, with the same dimensions as the input image.
        :rtype: numpy.ndarray
        """
        if self.image.ndim == 3:
            channels = [self._apply_to_channel(self.image[:, :, i]) for i in range(3)]
            deblurred_image = np.stack(channels, axis=-1)
        else:
            deblurred_image = self._apply_to_channel(self.image)
        return deblurred_image.astype(np.uint8)

    def _apply_to_channel(self, channel):
        """
        Apply the deconvolution process to a single color channel and updates the PSF estimate.

        :param channel: Single color channel of the image as a numpy array.
        :return: Deconvolved channel as a numpy array.
        """
        original_mean = np.mean(channel)
        original_std = np.std(channel)

        estimate = np.copy(channel)

        for _ in range(self.iterations):
            convolved_estimate = self._convolve2d(estimate, self.psf)
            relative_blur = channel / (convolved_estimate + 1e-12)
            error_estimate = self._convolve2d(relative_blur, self.psf_mirror)
            estimate *= error_estimate

            # Incremental lighting and contrast correction
            estimate_mean = np.mean(estimate)
            estimate_std = np.std(estimate)

            if estimate_mean > 0 and estimate_std > 0:
                mean_correction_factor = original_mean / estimate_mean
                std_correction_factor = original_std / estimate_std
                estimate = (estimate * mean_correction_factor) * std_correction_factor
                # Ensure the correction does not push values beyond the valid range
                estimate = np.clip(estimate, 0, 255)  # Assuming 8-bit image

        # Update the PSF estimate
        self._update_psf(channel, estimate)

        return estimate

    def _update_psf(self, original, estimate):
        """
        Update the PSF based on the latest image estimate and the original image.

        :param original: Original image channel.
        :param estimate: Latest deconvolved image estimate.
        """
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
        """
        Perform a 2D convolution of an image with a kernel, simulating the behavior of scipy.signal.convolve2d.
        Way faster than richardson_lucy._convolve2d because it uses FFT-based convolution.

        :param image: Input image as a numpy array.
        :param kernel: Convolution kernel as a numpy array.
        :return: Convolved image as a numpy array.
        """
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
        """
        Crop the center of an image to a specified size.

        :param img: Input image as a numpy array.
        :param cropsize: Tuple specifying the desired crop size.
        """
        y, x = img.shape
        cropx, cropy = cropsize
        startx = x // 2 - (cropx // 2)
        starty = y // 2 - (cropy // 2)
        return img[starty : starty + cropy, startx : startx + cropx]
