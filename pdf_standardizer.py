import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io

class PDFStandardizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Standardizer")
        self.root.geometry("600x400")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input file selection
        self.input_path = tk.StringVar()
        ttk.Label(self.main_frame, text="Input PDF:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.main_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.select_input).grid(row=0, column=2)
        
        # Output file selection
        self.output_path = tk.StringVar()
        ttk.Label(self.main_frame, text="Output PDF:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.main_frame, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.select_output).grid(row=1, column=2)
        
        # Page size options with presets
        size_frame = ttk.LabelFrame(self.main_frame, text="Target Page Size", padding="10")
        size_frame.grid(row=2, column=0, columnspan=3, pady=20, sticky=(tk.W, tk.E))
        
        self.width = tk.StringVar(value="595")
        self.height = tk.StringVar(value="842")
        
        # Add preset sizes dropdown
        self.presets = {
            "A4": (595, 842),
            "Letter": (612, 792),
            "Legal": (612, 1008),
            "Custom": None
        }
        
        ttk.Label(size_frame, text="Preset:").grid(row=0, column=0, sticky=tk.W)
        self.preset_var = tk.StringVar(value="A4")
        preset_dropdown = ttk.Combobox(size_frame, textvariable=self.preset_var, values=list(self.presets.keys()))
        preset_dropdown.grid(row=0, column=1, padx=5)
        preset_dropdown.bind('<<ComboboxSelected>>', self.update_size_from_preset)
        
        ttk.Label(size_frame, text="Width (points):").grid(row=1, column=0, sticky=tk.W)
        self.width_entry = ttk.Entry(size_frame, textvariable=self.width, width=10)
        self.width_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(size_frame, text="Height (points):").grid(row=1, column=2, sticky=tk.W, padx=20)
        self.height_entry = ttk.Entry(size_frame, textvariable=self.height, width=10)
        self.height_entry.grid(row=1, column=3, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.main_frame, length=300, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Convert button
        ttk.Button(self.main_frame, text="Convert PDF", command=self.convert_pdf).grid(row=4, column=0, columnspan=3, pady=10)
        
        # Status label
        self.status = tk.StringVar()
        ttk.Label(self.main_frame, textvariable=self.status).grid(row=5, column=0, columnspan=3)

    def update_size_from_preset(self, event=None):
        preset = self.preset_var.get()
        if preset != "Custom":
            width, height = self.presets[preset]
            self.width.set(str(width))
            self.height.set(str(height))

    def select_input(self):
        filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filename:
            self.input_path.set(filename)
            if not self.output_path.get():
                output = os.path.splitext(filename)[0] + "_standardized.pdf"
                self.output_path.set(output)

    def select_output(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.output_path.set(filename)

    def convert_pdf(self):
        try:
            input_file = self.input_path.get()
            output_file = self.output_path.get()
            
            if not input_file or not output_file:
                messagebox.showerror("Error", "Please select input and output files")
                return
                
            try:
                width = int(self.width.get())
                height = int(self.height.get())
                if width <= 0 or height <= 0:
                    raise ValueError("Dimensions must be positive")
            except ValueError:
                messagebox.showerror("Error", "Invalid dimensions")
                return
            
            self.status.set("Converting PDF...")
            self.progress['value'] = 0
            self.root.update()
            
            # Test the input file
            try:
                reader = PdfReader(input_file)
                num_pages = len(reader.pages)
            except Exception:
                messagebox.showerror("Error", "Invalid or corrupted input PDF")
                return
            
            standardize_pdf(input_file, output_file, (width, height), 
                          progress_callback=lambda p: self.update_progress(p))
            
            self.status.set("Conversion complete!")
            messagebox.showinfo("Success", f"PDF successfully converted and saved to:\n{output_file}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.set("Conversion failed")
        finally:
            self.progress['value'] = 0

    def update_progress(self, percentage):
        self.progress['value'] = percentage
        self.root.update()

def standardize_pdf(input_path, output_path, target_size=(595, 842), progress_callback=None):
    """
    Standardize all pages in a PDF to the same size while maintaining quality.
    
    Args:
        input_path (str): Path to the input PDF file
        output_path (str): Path to save the standardized PDF
        target_size (tuple): Target size in points (width, height)
        progress_callback (function): Callback function for progress updates
    """
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    total_pages = len(reader.pages)
    
    for i, page in enumerate(reader.pages):
        current_width = float(page.mediabox.width)
        current_height = float(page.mediabox.height)
        
        scale_x = target_size[0] / current_width
        scale_y = target_size[1] / current_height
        scale = min(scale_x, scale_y)
        
        page.scale(scale, scale)
        
        new_width = current_width * scale
        new_height = current_height * scale
        
        x_offset = (target_size[0] - new_width) / 2
        y_offset = (target_size[1] - new_height) / 2
        
        page.mediabox.lower_left = (x_offset, y_offset)
        page.mediabox.upper_right = (x_offset + new_width, y_offset + new_height)
        
        writer.add_page(page)
        
        if progress_callback:
            progress_callback((i + 1) * 100 / total_pages)
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFStandardizerApp(root)
    root.mainloop()