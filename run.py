#!/usr/bin/env python3
"""MAMA-SYNTH 2026 - BreizhCT: virtual peak-enhancement breast DCE-MRI from a pre-contrast slice.

Grand Challenge I/O:
    input   /input/images/pre-contrast-dce-mri-slice-breast/<uuid>.mha
    output  /output/images/synthetic-contrast-dce-mri-slice-breast/output.mha

Both are 2D z-score normalised float32 slices (official MAMA-SYNTH preprocessing). The prediction is the mean of
a five-fold U-Net++ ensemble applied to the slice and its three flips (Prediction.yml).
"""

import subprocess
from pathlib import Path

import SimpleITK as sitk
import torch

INPUT_FOLDER = Path("/input/images/pre-contrast-dce-mri-slice-breast")
OUTPUT_FOLDER = Path("/output/images/synthetic-contrast-dce-mri-slice-breast")
MODELS = [f"CV_{i}.pt" for i in range(5)]


def main() -> None:
    inputs = sorted(INPUT_FOLDER.glob("*.mha"))
    if not inputs:
        raise FileNotFoundError(f"No .mha input in {INPUT_FOLDER}")
    case = Path("Dataset/P001")
    case.mkdir(parents=True, exist_ok=True)
    sitk.WriteImage(sitk.ReadImage(str(inputs[0])), str(case / "IMAGE.mha"))

    device = ["--gpu", "0"] if torch.cuda.is_available() else ["--cpu", "1"]
    subprocess.run(["konfai", "PREDICTION", "-y", *device, "--config", "Prediction.yml", "--models", *MODELS], check=True)

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    sitk.WriteImage(sitk.ReadImage("Predictions/Out/Output/P001/sMR.mha"), str(OUTPUT_FOLDER / "output.mha"))


if __name__ == "__main__":
    main()
