import numpy as np
from scipy.signal import convolve2d


class FastRichardsonLucy:
    def __init__(self, image, psf, iterations=10):
        """
        Initializes the Richardson-Lucy deconvolution process with the given image, point spread function (PSF),
        and number of iterations.

        :param image: The blurry and noisy image to be deblurred. Can be a 2D (grayscale) or 3D (color) numpy array.
        :type image: numpy.ndarray
        :param psf: The Point Spread Function of the blur, as a 2D numpy array.
        :type psf: numpy.ndarray
        :param iterations: The number of iterations to run the deconvolution algorithm, defaults to 10.
        :type iterations: int
        """
        self.image = image
        self.psf = psf
        self.iterations = iterations
        self.psf_mirror = np.flipud(np.fliplr(self.psf))  # Precompute the mirrored PSF

    def apply(self):
        """
        Deblurs the image using the Richardson-Lucy deconvolution algorithm. This method supports both grayscale
        and color images by processing each channel separately if necessary.

        :return: The deblurred image, with the same dimensions as the input image.
        :rtype: numpy.ndarray
        """
        # Determine if the image is grayscale or color
        if self.image.ndim == 3:
            # Process each channel separately
            channels = []
            for i in range(3):  # Assuming the image is in RGB format
                channel = self._apply_to_channel(self.image[:, :, i])
                channels.append(channel)
            # Stack the processed channels back together
            deblurred_image = np.stack(channels, axis=-1)
        else:
            # Process a grayscale image
            deblurred_image = self._apply_to_channel(self.image)

        return deblurred_image

    def _apply_to_channel(self, channel):
        """
        Applies the Richardson-Lucy deconvolution algorithm to a single channel of the image.

        This private method is utilized by the `apply` method to process each color channel separately for color images,
        or directly on the image if it is grayscale.

        :param channel: A single channel of the blurry and noisy image, as a 2D numpy array.
        :type channel: numpy.ndarray
        :return: The deblurred channel.
        :rtype: numpy.ndarray
        """

        # Calculate the mean and standard deviation of the original channel for
        # lighting and contrast correction
        original_mean = np.mean(channel)
        original_std = np.std(channel)

        estimate = np.copy(channel)

        for _ in range(self.iterations):
            convolved_estimate = self._convolve2d(estimate, self.psf)
            relative_blur = channel / (convolved_estimate + 1e-12)
            error_estimate = self._convolve2d(relative_blur, self.psf_mirror)
            estimate = estimate * error_estimate

            # Incremental lighting and contrast correction
            estimate_mean = np.mean(estimate)
            estimate_std = np.std(estimate)

            if estimate_mean > 0 and estimate_std > 0:
                mean_correction_factor = original_mean / estimate_mean
                std_correction_factor = original_std / estimate_std
                estimate = (estimate * mean_correction_factor) * std_correction_factor
                # Ensure the correction does not push values beyond the valid range
                estimate = np.clip(estimate, 0, 255)  # Assuming 8-bit image

        return estimate

    def _convolve2d(self, image, kernel):
        """
            Applies a convolution kernel to an image using scipy.signal.convolve2d. This includes
            managing boundary conditions.

            :param image: A two-dimensional numpy array that represents the grayscale image to which the convolution will be applied.
            :type image: numpy.ndarray
            :param kernel: A two-dimensional numpy array that represents the convolution kernel to be applied to the image.
            :type kernel: numpy.ndarray
            :return: A two-dimensional numpy array representing the image after convolution.
            :rtype: numpy.ndarray
        """
        # Flip the kernel horizontally and vertically
        kernel = np.flipud(np.fliplr(kernel))
        
        # Perform convolution using scipy.signal.convolve2d
        output = convolve2d(image, kernel, mode='same', boundary='wrap')
        
        return output