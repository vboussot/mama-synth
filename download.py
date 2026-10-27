"""Download the five fold checkpoints from Hugging Face into the current directory."""

import shutil

from huggingface_hub import hf_hub_download

for i in range(5):
    shutil.copy(hf_hub_download(repo_id="VBoussot/mama-synth", filename=f"CV_{i}.pt"), f"CV_{i}.pt")
