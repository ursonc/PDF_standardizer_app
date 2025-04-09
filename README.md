# PDF Standardizer

A web application that allows users to standardize PDF documents to consistent page sizes.

## Features

- Upload PDF files through a modern web interface
- Standardize PDFs to common paper sizes (A4, Letter, Legal) or custom dimensions
- Preview and download the standardized PDF
- Responsive design for desktop and mobile use

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/pdf_standardizer.git
   cd pdf_standardizer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Web Application

1. Start the Flask web server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Upload a PDF file, select a target page size, and click "Standardize PDF"

4. Download your standardized PDF file

### Command Line Usage

You can also use the PDF standardizer from the command line:

```
python pdf_standardizer.py input.pdf output.pdf [--width WIDTH] [--height HEIGHT]
```

Arguments:
- `input.pdf`: Path to the input PDF file
- `output.pdf`: Path to save the standardized PDF
- `--width`: Target width in points (default: 595 for A4)
- `--height`: Target height in points (default: 842 for A4)

Example:
```
python pdf_standardizer.py document.pdf document_standardized.pdf --width 612 --height 792
```

## Page Size Reference

Common page sizes in points (72 points = 1 inch):

- A4: 595 × 842 points
- US Letter: 612 × 792 points
- US Legal: 612 × 1008 points

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 