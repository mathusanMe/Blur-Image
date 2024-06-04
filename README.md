# Blur-Image

## Overview

**Blur-Image** is a compact image processing toolkit developed in Python, designed to improve image sharpness through advanced blurring techniques. Based on the Richardson-Lucy deconvolution algorithm, this toolkit allows users to apply different blur kernels and iterative enhancements to improve image quality.

## Features

- **Blurring and sharpening**: Implement Richardson-Lucy deconvolution for image blurring, as well as standard blurring techniques using different kernels.
- **Batch image processing**: Process entire directories of images for bulk blurring and sharpening.
- **Quality measurements**: Calculate and report the Peak Signal-to-Noise Ratio (PSNR) to measure the quality of processed images.
- **Visual logging**: Color-coded console for easy monitoring of processing steps.

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/mathusanm6/Blur-Image.git
cd Blur-Image
```

### Prerequisites

Ensure you have Python installed along with the following packages:

- numpy
- scipy
- pillow (PIL)

You can install the required packages via pip:

```bash
pip install numpy scipy pillow
```

## Usage

After tuning the parameters in the `core.py` and `blind_core.py` files, you can run the toolkit using the following command:

```bash
python ./run.sh
```

## Richardson-Lucy Deconvolution

Below are some examples of images processed by the Blur-Image toolkit, showing the original images, the blurred versions, and the deblurred outputs after applying various kernels and iteration counts.

#### Process

Blurring are done using the following kernels:

- Average 3x3
- Average 5x5
- Average 11x11
- Gaussian 3x3, sigma: 1.0
- Gaussian 3x3, sigma: 2.0
- Gaussian 5x5, sigma: 1.0
- Gaussian 5x5, sigma: 2.0

Sharpening are done knowing the kernel used for blurring and the number of iterations using the Richardson-Lucy deconvolution algorithm as follows:

## Richardson-Lucy Deconvolution Algorithm

**Input:** Blurred image `I`, PSF `P`, number of iterations `n_it`  
**Output:** Restored image `J`

```python
# Initialize
J0 = I

# Iterative deconvolution
for n in range(1, n_it + 1):
    # Convolve Jn with P to obtain a blurred estimation I_estimated
    I_estimated = convolve(Jn, P)

    # Calculate the relative blur ratio
    Ratio = I / (I_estimated + epsilon)

    # Convolve this ratio with the mirror of the PSF
    Correction = convolve(Ratio, P_mirror)

    # Update the estimation
    Jn = Jn * Correction

# Return the final restored image
return Jn_it
```

#### Original Image

<div align="center" style="display: flex; justify-content: center; align-items: center;">
  <p style="margin-right: 20px; display: flex; flex-direction: column; align-items: center;">
    <img src="images/originals/flower.jpg" alt="grayscale flower" width="200">
    <br>
    <p style="margin-top: auto;">(1) Grayscale Flower</p>
  </p>
  <p style="margin-left: 20px; display: flex; flex-direction: column; align-items: center;">
    <img src="images/originals/tiger.jpeg" alt="tiger" width="200">
    <br>
    <p style="margin-top: auto;">(2) Tiger</p>
  </p>
</div>

#### Processed Images

##### (1) Grayscale Flower

<table style="width: 100%; border-collapse: collapse;">
    <tr>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Average 3x3</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Average 5x5</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Average 11x11</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Gaussian 3x3, sigma: 1.0</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Gaussian 3x3, sigma: 2.0</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Gaussian 5x5, sigma: 1.0</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Gaussian 5x5, sigma: 2.0</p>
        </td>
    </tr>
    <tr>
        <td colspan="7" align="center" style="text-align: center;"><strong>Blurred Images</strong></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_3x3/blurred.png" alt="blurred flower" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_5x5/blurred.png" alt="blurred flower" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_11x11/blurred.png" alt="blurred flower" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_3x3_sigma1.0/blurred.png" alt="blurred flower" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_3x3_sigma2.0/blurred.png" alt="blurred flower" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_5x5_sigma1.0/blurred.png" alt="blurred flower" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_5x5_sigma2.0/blurred.png" alt="blurred flower" width="200">
            <br>
        </td>
    </tr>
    <tr>
        <td colspan="7" align="center" style="text-align: center;"><strong>Unblurred Images</strong></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_3x3/unblurred_5-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_5x5/unblurred_5-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_11x11/unblurred_5-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_3x3_sigma1.0/unblurred_5-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_3x3_sigma2.0/unblurred_5-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_5x5_sigma1.0/unblurred_5-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_5x5_sigma2.0/unblurred_5-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
    </tr>
    <tr>
        <td colspan="7" style="text-align: center;"></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_3x3/unblurred_10-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_5x5/unblurred_10-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_11x11/unblurred_10-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_3x3_sigma1.0/unblurred_10-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_3x3_sigma2.0/unblurred_10-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_5x5_sigma1.0/unblurred_10-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_5x5_sigma2.0/unblurred_10-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
    </tr>
    <tr>
        <td colspan="7" style="text-align: center;"></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_3x3/unblurred_15-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_5x5/unblurred_15-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/average_11x11/unblurred_15-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_3x3_sigma1.0/unblurred_15-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_3x3_sigma2.0/unblurred_15-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_5x5_sigma1.0/unblurred_15-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/flower/gaussian_5x5_sigma2.0/unblurred_15-iter.png" alt="unblurred flower" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
    </tr>
</table>

##### (2) Tiger

<table style="width: 100%; border-collapse: collapse;">
    <tr>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Average 3x3</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Average 5x5</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Average 11x11</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Gaussian 3x3, sigma: 1.0</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Gaussian 3x3, sigma: 2.0</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Gaussian 5x5, sigma: 1.0</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Gaussian 5x5, sigma: 2.0</p>
        </td>
    </tr>
    <tr>
        <td colspan="7" align="center" style="text-align: center;"><strong>Blurred Images</strong></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_3x3/blurred.png" alt="blurred tiger" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_5x5/blurred.png" alt="blurred tiger" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_11x11/blurred.png" alt="blurred tiger" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_3x3_sigma1.0/blurred.png" alt="blurred tiger" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_3x3_sigma2.0/blurred.png" alt="blurred tiger" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_5x5_sigma1.0/blurred.png" alt="blurred tiger" width="200">
            <br>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_5x5_sigma2.0/blurred.png" alt="blurred tiger" width="200">
            <br>
        </td>
    </tr>
    <tr>
        <td colspan="7" align="center" style="text-align: center;"><strong>Unblurred Images</strong></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_3x3/unblurred_5-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_5x5/unblurred_5-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_11x11/unblurred_5-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_3x3_sigma1.0/unblurred_5-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_3x3_sigma2.0/unblurred_5-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_5x5_sigma1.0/unblurred_5-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_5x5_sigma2.0/unblurred_5-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">5 Iterations</p>
        </td>
    </tr>
    <tr>
        <td colspan="7" style="text-align: center;"></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_3x3/unblurred_10-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_5x5/unblurred_10-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_11x11/unblurred_10-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_3x3_sigma1.0/unblurred_10-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_3x3_sigma2.0/unblurred_10-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_5x5_sigma1.0/unblurred_10-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_5x5_sigma2.0/unblurred_10-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">10 Iterations</p>
        </td>
    </tr>
    <tr>
        <td colspan="7" style="text-align: center;"></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_3x3/unblurred_15-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_5x5/unblurred_15-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/average_11x11/unblurred_15-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_3x3_sigma1.0/unblurred_15-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_3x3_sigma2.0/unblurred_15-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_5x5_sigma1.0/unblurred_15-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/processed/tiger/gaussian_5x5_sigma2.0/unblurred_15-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations</p>
        </td>
    </tr>
</table>

## Blind Richardson-Lucy Deconvolution

### Process

Sharpening are done not knowing the kernel used for blurring and the number of iterations using the Blind Richardson-Lucy deconvolution algorithm as follows:

## Blind Richardson-Lucy Deconvolution Algorithm

**Input:** Blurred image `I`, initial PSF `P`, number of iterations for image `n_it`, number of iterations for PSF `psf_it`  
**Output:** Restored image `J`, refined PSF `P`

```python
# Initialize
J0 = I

# Iterative deconvolution
for n in range(1, n_it + 1):
    # Convolve Jn with P to obtain a blurred estimation I_estimated
    I_estimated = convolve(Jn, P)

    # Calculate the relative blur ratio
    Ratio = I / (I_estimated + epsilon)

    # Convolve this ratio with the mirror of the PSF
    Correction = convolve(Ratio, P_mirror)

    # Update the estimation
    Jn = Jn * Correction

    # PSF refinement
    for m in range(1, psf_it + 1):
        # Convolve Jn+1 with P to obtain a new blurred estimation I_estimated
        I_estimated = convolve(Jn, P)

        # Calculate the error ratio
        E = I / (I_estimated + epsilon)

        # Convolve this ratio with the mirror of the restored image Jn+1
        PSF_Update = convolve(E, Jn_mirror)

        # Update the PSF
        P = P * PSF_Update

        # Normalize the PSF
        P = P / sum(P)

# Return the final restored image and refined PSF
return Jn_it, P
```

### Original Image

<div align="center" style="display: flex; justify-content: center; align-items: center;">
  <p style="margin-right: 20px; display: flex; flex-direction: column; align-items: center;">
    <img src="images/blind_originals/tiger.png" alt="blurred tiger" width="200">
    <br>
    <p align="center" style="margin-top: auto;">(A) Blurred tiger (Unknown Kernel)</p>
  </p>
</div>

### Processed Images

#### (A) Blurred Tiger (Unknown Kernel)

<table style="width: 100%; border-collapse: collapse;">
    <tr>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Average 3x3</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Average 5x5</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Average 11x11</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Gaussian 5x5, sigma: 1.0</p>
        </td>
        <td style="text-align: center;">
            <p align="center" style="font-weight: bold;">Gaussian 5x5, sigma: 2.0</p>
        </td>
    </tr>
    <tr>
        <td colspan="7" style="text-align: center;"></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_5x5/tiger_unblurred_15-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_5x5/tiger_unblurred_15-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_11x11/tiger_unblurred_15-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/gaussian_5x5_sigma1.0/tiger_unblurred_15-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/gaussian_5x5_sigma2.0/tiger_unblurred_15-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">15 Iterations, 25 PSF Iterations</p>
        </td>
    </tr>
    <tr>
        <td colspan="7" style="text-align: center;"></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_5x5/tiger_unblurred_30-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">30 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_5x5/tiger_unblurred_30-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">30 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_11x11/tiger_unblurred_30-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">30 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/gaussian_5x5_sigma1.0/tiger_unblurred_30-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">30 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/gaussian_5x5_sigma2.0/tiger_unblurred_30-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">30 Iterations, 25 PSF Iterations</p>
        </td>
    </tr>
    <tr>
        <td colspan="7" style="text-align: center;"></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_5x5/tiger_unblurred_60-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">60 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_5x5/tiger_unblurred_60-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">60 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_11x11/tiger_unblurred_60-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">60 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/gaussian_5x5_sigma1.0/tiger_unblurred_60-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">60 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/gaussian_5x5_sigma2.0/tiger_unblurred_60-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">60 Iterations, 25 PSF Iterations</p>
        </td>
    </tr>
    <tr>
        <td colspan="7" style="text-align: center;"></td>
    </tr>
    <tr>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_5x5/tiger_unblurred_120-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">120 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_5x5/tiger_unblurred_120-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">120 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/average_11x11/tiger_unblurred_120-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">120 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/gaussian_5x5_sigma1.0/tiger_unblurred_120-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">120 Iterations, 25 PSF Iterations</p>
        </td>
        <td style="text-align: center;">
            <img src="images/blind_processed/tiger/gaussian_5x5_sigma2.0/tiger_unblurred_120-iter_25-psf-iter.png" alt="unblurred tiger" width="200">
            <br>
            <p align="center">120 Iterations, 25 PSF Iterations</p>
        </td>
    </tr>
</table>

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.
