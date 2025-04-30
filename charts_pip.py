#!/usr/bin/env python3
"""
Graficas de polidipsia inducida por programa (PIP)
=================================================
Autor: Marcos Peña Sánchez‑Covisa  
Licencia: MIT

Descripción
-----------
Genera dos figuras en escala de grises que resumen los resultados esperados del
estudio sobre la influencia del ambiente social y sensorial en la PIP:

* **Figura 1** – Curvas de adquisición (media ± SEM) de lametones a lo largo de
  20 sesiones para los cuatro grupos experimentales.
* **Figura 2** – Boxplots (con puntos individuales) de lametones promediados en
  el bloque final de sesiones (16‑20).

El script puede usarse como plantilla: basta con sustituir la función
``load_or_simulate_data`` por la carga de un archivo CSV real con idéntica
estructura (filas = sujetos, columnas = sesiones).

Uso
----
```bash
python graficas_pip.py --outdir figures
```
Los ficheros ``figura1.png`` y ``figura2.png`` se guardarán en la carpeta
indicada (por defecto ``./``).

Dependencias
------------
* numpy ≥ 1.20
* matplotlib ≥ 3.5

``pip install numpy matplotlib``
"""

import argparse
import os
from typing import Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Parámetros fijos del estudio --------------------------------------------------
# -----------------------------------------------------------------------------
N_SUBJECTS = 8
SESSIONS = np.arange(1, 21)
GROUPS: Dict[str, Dict[str, float]] = {
    "AIS":  {"plateau": 2200, "k": 0.30},
    "A+ES": {"plateau": 1800, "k": 0.25},
    "G+ES": {"plateau": 1200, "k": 0.20},
    "G–ES": {"plateau":  800, "k": 0.15},
}

# -----------------------------------------------------------------------------
# Simulación o carga de datos ---------------------------------------------------
# -----------------------------------------------------------------------------

def load_or_simulate_data(seed: int = 42) -> Dict[str, np.ndarray]:
    """Devuelve un diccionario {grupo: matriz sujetos×sesiones}.

    Reemplace esta función para cargar datos experimentales reales desde un CSV
    con la forma `(n_subjects, 20)` por grupo.
    """
    rng = np.random.default_rng(seed)
    data = {}
    for name, params in GROUPS.items():
        plateau, k = params["plateau"], params["k"]
        subject_matrix = []
        for _ in range(N_SUBJECTS):
            means = plateau * (1 - np.exp(-k * SESSIONS))
            noise = rng.normal(0, plateau * 0.05, size=SESSIONS.size)
            subject_matrix.append(np.clip(means + noise, 0, None))
        data[name] = np.vstack(subject_matrix)
    return data

# -----------------------------------------------------------------------------
# Gráficas ---------------------------------------------------------------------
# -----------------------------------------------------------------------------

LINE_STYLES = {"AIS": "-", "A+ES": "--", "G+ES": ":", "G–ES": "-."}
MARKERS = {"AIS": "o", "A+ES": "s", "G+ES": "^", "G–ES": "d"}


def plot_timecourse(data: Dict[str, np.ndarray], out_path: str) -> None:
    """Genera la figura de curvas de adquisición (Figura 1)."""
    fig, ax = plt.subplots(figsize=(8, 5))
    for name, matrix in data.items():
        means = matrix.mean(axis=0)
        sems = matrix.std(axis=0, ddof=1) / np.sqrt(matrix.shape[0])
        ax.plot(
            SESSIONS,
            means,
            linestyle=LINE_STYLES[name],
            marker=MARKERS[name],
            color="black",
            label=name,
        )
        ax.fill_between(
            SESSIONS,
            means - sems,
            means + sems,
            color="black",
            alpha=0.1,
        )

    ax.set_xlabel("sesión")
    ax.set_ylabel("lametones")
    ax.set_title("evolución temporal de la polidipsia inducida por programa")
    ax.legend(title="condición")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def plot_boxplot(data: Dict[str, np.ndarray], out_path: str) -> None:
    """Genera la figura de boxplots del bloque final (Figura 2)."""
    groups_order = ["AIS", "A+ES", "G+ES", "G–ES"]
    final_block = [data[g][:, 15:20].mean(axis=1) for g in groups_order]

    fig, ax = plt.subplots(figsize=(6, 5))
    box = ax.boxplot(final_block, labels=groups_order, patch_artist=True)

    # B/N: contornos negros, fondo blanco
    for element in ["boxes", "whiskers", "caps", "medians"]:
        for b in box[element]:
            b.set(color="black")
    for patch in box["boxes"]:
        patch.set(facecolor="white")

    # Puntos individuales
    for i, vals in enumerate(final_block, start=1):
        ax.scatter(
            np.full_like(vals, i, dtype=float) + np.random.uniform(-0.1, 0.1, size=vals.size),
            vals,
            color="black",
            alpha=0.7,
            s=15,
            zorder=2,
        )

    ax.set_xlabel("condición de alojamiento")
    ax.set_ylabel("lametones")
    ax.set_title("lametones en bloque final (sesiones 16‑20)")
    ax.grid(axis="y")
    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)

# -----------------------------------------------------------------------------
# Programa principal -----------------------------------------------------------
# -----------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Genera las figuras de PIP")
    parser.add_argument(
        "--outdir", "-o", default=".", help="directorio donde guardar las figuras"
    )
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    data = load_or_simulate_data()

    plot_timecourse(data, os.path.join(args.outdir, "figura1.png"))
    plot_boxplot(data, os.path.join(args.outdir, "figura2.png"))
    print("Figuras guardadas en", os.path.abspath(args.outdir))


if __name__ == "__main__":
    main()
