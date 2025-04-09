import os
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io

def standardize_pdf(input_path, output_path, target_size=(595, 842)):  # A4 size in points (72 dpi)
    """
    Standardize all pages in a PDF to the same size while maintaining quality.
    
    Args:
        input_path (str): Path to the input PDF file
        output_path (str): Path to save the standardized PDF
        target_size (tuple): Target size in points (width, height)
    """
    # Create output directory if it doesn't exist and if there's a directory path
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Read the input PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        # Get the current page size
        current_width = float(page.mediabox.width)
        current_height = float(page.mediabox.height)
        
        # Calculate scaling factors
        scale_x = target_size[0] / current_width
        scale_y = target_size[1] / current_height
        
        # Use the smaller scale to maintain aspect ratio
        scale = min(scale_x, scale_y)
        
        # Scale the page
        page.scale(scale, scale)
        
        # Center the page
        new_width = current_width * scale
        new_height = current_height * scale
        
        x_offset = (target_size[0] - new_width) / 2
        y_offset = (target_size[1] - new_height) / 2
        
        page.mediabox.lower_left = (x_offset, y_offset)
        page.mediabox.upper_right = (x_offset + new_width, y_offset + new_height)
        
        # Add the processed page to the writer
        writer.add_page(page)
    
    # Write the output PDF
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
        print(f"PDF standardized and saved to {output_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Standardize PDF page sizes')
    parser.add_argument('input', help='Input PDF file path')
    parser.add_argument('output', help='Output PDF file path')
    parser.add_argument('--width', type=int, default=595, help='Target width in points (default: 595 for A4)')
    parser.add_argument('--height', type=int, default=842, help='Target height in points (default: 842 for A4)')
    
    args = parser.parse_args()
    
    standardize_pdf(args.input, args.output, (args.width, args.height)) 