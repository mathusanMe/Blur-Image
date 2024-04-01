import numpy as np
from image_processing.convolve2d import convolve2d


class RichardsonLucy:
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
        estimate = np.copy(channel)
        psf_mirror = np.flipud(np.fliplr(self.psf))  # Mirrored PSF for the convolution

        for _ in range(self.iterations):
            convolved_estimate = convolve2d(
                estimate, self.psf, mode="same", boundary="wrap"
            )
            relative_blur = channel / (convolved_estimate + 1e-12)
            error_estimate = convolve2d(
                relative_blur, psf_mirror, mode="same", boundary="wrap"
            )
            estimate = estimate * error_estimate

        return estimate
