[![Grand Challenge](https://img.shields.io/badge/Grand%20Challenge-MAMA--SYNTH_2026-blue)](https://mamasynth.grand-challenge.org/) [![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-mama--synth-orange)](https://huggingface.co/VBoussot/mama-synth)

# MAMA-SYNTH 2026 – Virtual contrast enhancement of breast DCE-MRI

This repository provides everything needed to build the Docker image and reproduce our solution (team **BreizhCT**,
algorithm *SAM Synth*) to the **MAMA-SYNTH 2026** challenge: synthesizing the peak-enhancement phase of breast
DCE-MRI from a 2D pre-contrast T1-weighted slice.

Our approach is based on a **2D U-Net++** with a ResNet-34 encoder, implemented with
[KonfAI](https://github.com/vboussot/KonfAI), our modular deep learning framework.
Training combines a pixel-wise **MAE** loss with a **perceptual loss** derived from **SAM 2.1** features, on the
1,506 cases of [MAMA-MIA](https://doi.org/10.7303/syn60868042) with a patient-level five-fold split.

Final predictions use **test-time augmentation** (the slice and its three flips) and **5-fold ensembling**, i.e. the
mean of 20 predictions.

🏅 **12th of 30 entries** on the hidden test set (300 cases from Radboud University Medical Centre and Instituto
Alexander Fleming)
(Related leaderboard: [MAMA-SYNTH test phase](https://mamasynth.grand-challenge.org/evaluation/test-phase/leaderboard/))

| Rank | MSE ↓ | LPIPS ↓ | SSIM tumour ↑ | FRD ↓ | AUROC contrast ↑ | AUROC tumour-ROI ↑ | Dice ↑ | HD95 ↓ |
|------|-------|---------|---------------|-------|------------------|--------------------|--------|--------|
| 12 | 0.84 (9) | 0.13 (21) | 0.50 (2) | 24.71 (20) | 0.81 (7) | 0.90 (25) | 0.38 (18) | 213.1 (23) |

Per-metric positions are in parentheses.

---

## 🚀 Inference instructions

### 1. Install KonfAI

```bash
pip install -r requirements.txt
```

---

### 2. Download pretrained weights

Download the five models from Hugging Face:

👉 https://huggingface.co/VBoussot/mama-synth

```bash
python download.py
```

You should obtain `CV_0.pt` ... `CV_4.pt` in the working directory.

---

### 3. Dataset structure

The input is a 2D pre-contrast slice produced by the official MAMA-SYNTH preprocessing
([mama-research/mama-synth](https://github.com/mama-research/mama-synth)), i.e. z-score normalised with the
dataset-level statistics. Your dataset should be structured as follows:

```
./Dataset/
├── <case_1>/
│   └── IMAGE.mha
├── <case_2>/
│   └── IMAGE.mha
└── ...
```

---

### 4. Run inference

Copy the KonfAI files next to your working directory — the prediction config references `UNetpp.py` through the
`UNetpp:` classpath:

```bash
cp KonfAI/UNetpp.py KonfAI/Prediction.yml .
```

```bash
konfai PREDICTION -y --gpu 0 \
  --config Prediction.yml \
  --models CV_0.pt CV_1.pt CV_2.pt CV_3.pt CV_4.pt
```

Predictions are written to `./Predictions/Out/Output/<case>/sMR.mha`, in the same z-score space as the input.

---

## 🐳 Docker (Grand Challenge)

```bash
./build.sh       # builds the image mama_synth_algorithm (weights downloaded at build time)
./test_gpu.sh    # runs it on test/ with the Grand Challenge restrictions, output in output/
docker save mama_synth_algorithm | gzip -c > mama_synth_algorithm.tar.gz   # file to upload on Grand Challenge
```

The container reads `/input/images/pre-contrast-dce-mri-slice-breast/*.mha` and writes
`/output/images/synthetic-contrast-dce-mri-slice-breast/output.mha` (`run.py`). The slice in `test/` is a
placeholder that only checks the I/O.

---

## 📄 License

The code is released under the Apache-2.0 license. The models are trained on MAMA-MIA (CC BY-NC 4.0).
