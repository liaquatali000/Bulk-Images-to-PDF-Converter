/*
 * This file is part of Image & PDF Converter.
 *
 * Image & PDF Converter is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Image & PDF Converter is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from fpdf import FPDF
from PIL import Image
import os
import logging
from datetime import datetime
import threading
import fitz  # PyMuPDF

class ImageConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image & PDF Converter v0.2")
        self.window.geometry("800x700")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("Custom.TButton", padding=10)
        
        # Supported formats
        self.image_formats = {
            '.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', 
            '.webp', '.ico', '.ppm', '.pgm', '.pbm'
        }
        
        # Initialize variables
        self.input_files = []
        self.output_path = None
        self.conversion_running = False
        self.total_files = 0
        self.processed_files = 0
        self.convert_to_pdf = True
        self.output_format = tk.StringVar(value='png')
        
        # Create main frame
        self.main_frame = ttk.Frame(self.window, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title and Subheading
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(pady=10)
        
        title_label = ttk.Label(
            title_frame, 
            text="Image & PDF Converter",
            font=("Helvetica", 16, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Created by Liaqat Ali",
            font=("Helvetica", 10, "italic")
        )
        subtitle_label.pack()
        
        # Mode selection frame
        mode_frame = ttk.LabelFrame(self.main_frame, text="Conversion Mode", padding="10")
        mode_frame.pack(fill=tk.X, pady=5)
        
        # Radio buttons for mode selection
        self.mode_var = tk.BooleanVar(value=True)
        ttk.Radiobutton(
            mode_frame,
            text="Images to PDF",
            variable=self.mode_var,
            value=True,
            command=self.update_mode
        ).pack(side=tk.LEFT, padx=20)
        
        ttk.Radiobutton(
            mode_frame,
            text="PDF to Images",
            variable=self.mode_var,
            value=False,
            command=self.update_mode
        ).pack(side=tk.LEFT, padx=20)
        
        # Format selection
        self.format_frame = ttk.Frame(mode_frame)
        ttk.Label(self.format_frame, text="Output Format:").pack(side=tk.LEFT, padx=5)
        format_combo = ttk.Combobox(
            self.format_frame,
            textvariable=self.output_format,
            values=['png', 'jpg', 'webp', 'bmp'],
            width=10,
            state='readonly'
        )
        format_combo.pack(side=tk.LEFT)
        self.format_frame.pack_forget()
        
        # File selection frame
        file_frame = ttk.LabelFrame(self.main_frame, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        # Buttons for file selection
        ttk.Button(
            file_frame,
            text="Select Files",
            command=self.select_files,
            style="Custom.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            file_frame,
            text="Select Output Location",
            command=self.select_output_location,
            style="Custom.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        # Convert button
        self.convert_button = ttk.Button(
            file_frame,
            text="Convert Files",
            command=self.start_conversion,
            style="Custom.TButton"
        )
        self.convert_button.pack(side=tk.LEFT, padx=5)
        
        # Status frame
        status_frame = ttk.LabelFrame(self.main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Selected files info
        self.files_label = ttk.Label(status_frame, text="Selected Files: 0")
        self.files_label.pack(pady=5)
        
        self.output_label = ttk.Label(status_frame, text="Output Location: Not selected")
        self.output_label.pack(pady=5)
        
        # Progress frame
        progress_frame = ttk.Frame(status_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            status_frame,
            orient="horizontal",
            length=400,
            mode="determinate"
        )
        self.progress_bar.pack(fill=tk.X, pady=10)
        
        # Log area
        self.log_text = scrolledtext.ScrolledText(
            self.main_frame,
            height=10,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def select_files(self):
        if self.convert_to_pdf:
            filetypes = [("Image files", 
                         " ".join(f"*{fmt}" for fmt in self.image_formats))]
        else:
            filetypes = [("PDF files", "*.pdf")]
            
        files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=filetypes
        )
        
        if files:
            self.input_files = list(files)
            self.files_label.config(text=f"Selected Files: {len(self.input_files)}")
            self.update_status(f"Selected {len(self.input_files)} files")
            
    def select_output_location(self):
        self.output_path = filedialog.askdirectory(
            title="Select Output Location"
        )
        
        if self.output_path:
            self.output_label.config(text=f"Output Location: {self.output_path}")
            self.update_status(f"Output location set to: {self.output_path}")
            
    def update_mode(self):
        self.convert_to_pdf = self.mode_var.get()
        if self.convert_to_pdf:
            self.format_frame.pack_forget()
        else:
            self.format_frame.pack(side=tk.LEFT, padx=20)
        
        # Clear selected files when mode changes
        self.input_files = []
        self.files_label.config(text="Selected Files: 0")
        
    def update_status(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def start_conversion(self):
        if not self.input_files:
            self.update_status("Please select files first!")
            return
            
        if not self.output_path:
            self.update_status("Please select output location!")
            return
            
        if not self.conversion_running:
            self.conversion_running = True
            self.convert_button.config(text="Stop Conversion")
            thread = threading.Thread(target=self.convert_files)
            thread.start()
        else:
            self.conversion_running = False
            self.convert_button.config(text="Convert Files")
            
    def convert_files(self):
        self.total_files = len(self.input_files)
        self.processed_files = 0
        self.progress_bar["value"] = 0
        successful = 0
        failed = 0
        
        try:
            if self.convert_to_pdf:
                # Convert each image to individual PDF
                for file_path in self.input_files:
                    if not self.conversion_running:
                        break
                        
                    try:
                        # Create a new PDF for each image
                        pdf = FPDF()
                        pdf.add_page()
                        
                        # Get original filename without extension
                        base_name = os.path.splitext(os.path.basename(file_path))[0]
                        output_file = os.path.join(self.output_path, f"{base_name}.pdf")
                        
                        # Convert and save
                        img = Image.open(file_path)
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        pdf.image(file_path, x=10, y=10, w=190)
                        pdf.output(output_file)
                        
                        successful += 1
                        self.update_status(f"Converted: {os.path.basename(file_path)}")
                    except Exception as e:
                        failed += 1
                        self.update_status(f"Error processing {os.path.basename(file_path)}: {str(e)}")
                    
                    self.processed_files += 1
                    self.progress_bar["value"] = (self.processed_files / self.total_files) * 100
            
            else:
                # Convert PDF to images
                for pdf_path in self.input_files:
                    if not self.conversion_running:
                        break
                        
                    try:
                        pdf_document = fitz.open(pdf_path)
                        # Get original filename without extension
                        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
                        
                        # If PDF has only one page, don't add page number to filename
                        if pdf_document.page_count == 1:
                            page = pdf_document[0]
                            image = page.get_pixmap()
                            output_file = os.path.join(self.output_path, f"{base_name}.{self.output_format.get()}")
                            image.save(output_file)
                        else:
                            # If multiple pages, add page number to filename
                            for page_number in range(pdf_document.page_count):
                                page = pdf_document[page_number]
                                image = page.get_pixmap()
                                output_file = os.path.join(self.output_path, 
                                    f"{base_name}_{page_number + 1}.{self.output_format.get()}")
                                image.save(output_file)
                            
                        pdf_document.close()
                        successful += 1
                        self.update_status(f"Converted: {os.path.basename(pdf_path)}")
                    except Exception as e:
                        failed += 1
                        self.update_status(f"Error converting {os.path.basename(pdf_path)}: {str(e)}")
                    
                    self.processed_files += 1
                    self.progress_bar["value"] = (self.processed_files / self.total_files) * 100
        
        except Exception as e:
            self.update_status(f"Conversion error: {str(e)}")
        
        summary = f"Completed! Successfully converted: {successful}, Failed: {failed}"
        self.update_status(summary)
        
        self.conversion_running = False
        self.convert_button.config(text="Convert Files")
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageConverter()
    app.run()