# TFG‑PIP‑graphs

Python scripts and example data for generating the figures included in the
Bachelor Thesis (TFG) *“Environmental and social modulation of
schedule‑induced polydipsia in rats”*.

## Contents

| Path | Description |
|------|-------------|
| `graficas_pip.py` | Main script that simulates the expected dataset and produces two publication‑ready figures in grayscale (PNG + PDF). |
| `data/` | Example CSV files with the simulated behavioural measures (one file per subject). |
| `env.txt` | Plain‑text list of Python dependencies and versions used to reproduce the figures. |

## Requirements

* Python ≥ 3.9
* `numpy`, `matplotlib` (tested with NumPy 1.26 and Matplotlib 3.9)

Create a virtual environment and install the dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r env.txt
```

## Usage

Generate the figures in a chosen directory (defaults to `./figures`):

```bash
python charts_pip.py --output-dir figures
```

The script produces two files:

* `figura1.png`  ➜ *evolution temporal de la polidipsia inducida por programa*
* `figura2.png` ➜ *lametones en bloque final (sesiones 16‑20)*

All figures are rendered in black and white to conform to journal style.

## Reproducibility

The random seed is fixed (`np.random.seed(42)`) so the simulated dataset and
figures are deterministic. Replace the contents of `data/` with your own CSV
files to visualise empirical results.

## Citation

If you use this code or an adapted version in your own work, please cite the
repository:

> Peña S‑C, M. (2025). *TFG‑PIP‑graphs* (Version 1.0) [Git repository]. GitHub.  
> https://github.com/username/TFG-PIP-graphs

A DOI will be minted for the final release via Zenodo.

## License

MIT — see `LICENSE` for details.
