# Bulk Image to PDF Converter

A robust Python script for bulk converting images (PNG, JPG, etc.) to PDF files with progress tracking, logging, and duplicate prevention.

## 🌟 Features

- **Multi-Format Support**: Converts JPG, JPEG, PNG, BMP, GIF, and TIFF images
- **Smart Processing**: 
  - Automatically rotates landscape images
  - Skips already converted images
  - Maintains original image quality
- **Progress Tracking**:
  - Real-time progress bar
  - Detailed conversion statistics
  - Comprehensive logging system
- **Error Handling**:
  - Robust error management
  - Detailed error logging
  - Continues processing even if some files fail
- **Output Management**:
  - Organized output folder structure
  - Prevents duplicate file names
  - Preserves original file names

## 📋 Requirements

- Python 3.6+
- Required packages:
  ```
  fpdf
  Pillow
  tqdm
  ```

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bulk-image-to-pdf-converter.git
   cd bulk-image-to-pdf-converter
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

1. Place the script in the folder containing your images
2. Run the script:
   ```bash
   python convert_images.py
   ```
3. The script will:
   - Create an 'output' folder for PDFs
   - Create a 'logs' folder for logging
   - Convert all new images to PDFs
   - Skip previously converted images

## 📁 Directory Structure

```
your-folder/
│
├── convert_images.py          # Main script
├── requirements.txt          # Package requirements
├── images/                   # Your source images
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
│
├── output/                   # Generated PDFs (created automatically)
│   ├── image1.pdf
│   ├── image2.pdf
│   └── ...
│
└── logs/                     # Log files (created automatically)
    └── conversion_YYYYMMDD_HHMMSS.log
```

## 📝 Log Files

The script generates detailed log files containing:
- List of processed files
- Conversion statistics
- Error messages (if any)
- Processing duration
- Skipped files information

## ⚙️ Configuration

The script uses default A4 size (210x297mm) for PDFs. To modify this or other settings, edit the constants at the beginning of the script.

## 🔍 Error Handling

- Invalid image files are automatically skipped
- Processing continues even if individual conversions fail
- All errors are logged with detailed information
- Summary report shows successful and failed conversions

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- FPDF library for PDF creation
- Pillow library for image processing
- tqdm library for progress bars
