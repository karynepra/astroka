# astroka

astro-fits-tools/
├── analysis/                   # Módulo com funções de análise
│   ├── __init__.py
│   └── analyze_headers.py
|
├── headers/                    # Headers extraídos (.fits_header.txt)
│   └── example.fits_header.txt
│
├── examples/                   # Scripts de exemplo
│   └── main.py
│
├── README.md                   # Documentação principal
├── requirements.txt            # Bibliotecas usadas no projeto
└── .gitignore                  # Ignora arquivos temporários

# AstroPy Tools — From Basics to Advanced

This repository is part of my PhD journey in Astronomy, where I organize Python tools for reading and analyzing astronomical data. The goal is to build a personal toolkit — from basic tasks like reading FITS headers to more advanced spectral analysis.

## 📁 Current Modules

### `headers/`
Tools to:
- Scan directories for `.fits` files
- Extract FITS headers
- Select and structure specific header keywords

## 🛠️ Requirements

- Python 3.8+
- astropy
- pathlib

Install with:

```bash
pip install astropy
