# PDF Standardizer

A Python tool that standardizes all pages in a PDF to the same size while maintaining quality and aspect ratio.

## Features

- Maintains aspect ratio of original pages
- Centers content on the standardized page
- Preserves image quality
- Configurable output page size
- Defaults to A4 size (595x842 points)

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python pdf_standardizer.py input.pdf output.pdf
```

Custom page size (in points):
```bash
python pdf_standardizer.py input.pdf output.pdf --width 612 --height 792  # Letter size
```

## Notes

- The tool uses points as the unit of measurement (72 points = 1 inch)
- Default size is A4 (595x842 points)
- The content is scaled to fit within the target size while maintaining aspect ratio
- Content is centered on the page 