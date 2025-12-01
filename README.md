# 📄 PDF Extractor

<div align="center">

**A powerful Python tool for extracting text from PDF files and exporting to CSV or JSON formats**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ✨ Features

- 🔍 **Extract text from PDF files** - Supports complex PDF layouts
- 📊 **Export to CSV or JSON** - Multiple output formats
- 📑 **Flexible extraction modes**:
  - Extract individual pages
  - Extract entire document
  - Extract line by line
  - **Extract sentence by sentence** ⭐ NEW
- 🌐 **FastAPI web server** - REST API with automatic documentation
- 💾 **Downloadable file responses** - All endpoints return downloadable files
- 🔌 **Separate endpoints** - Dedicated endpoints for CSV and JSON formats
- 🖥️ **Command-line interface** - Use from terminal
- 🐍 **Programmatic API** - Easy integration in Python projects

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd pdf-extractor

# Install dependencies
pip install -r requirements.txt
```

### Start the Server

```bash
# Option 1: Using Python
python app.py

# Option 2: Using uvicorn directly (recommended)
uvicorn app:app --host 127.0.0.1 --port 8001 --reload
```

The server will start at `http://localhost:8001`

### Access API Documentation

Once the server is running, visit:
- 📖 **Swagger UI**: `http://localhost:8001/docs`
- 📚 **ReDoc**: `http://localhost:8001/redoc`

---

## 📖 Usage

### Command-Line Interface

#### Extract all pages to JSON (default)
```bash
python pdf_extractor.py input.pdf
```

#### Extract all pages to CSV
```bash
python pdf_extractor.py input.pdf --format csv
```

#### Extract a specific page
```bash
python pdf_extractor.py input.pdf --page 1 --format json
```

#### Extract whole document as a single block
```bash
python pdf_extractor.py input.pdf --whole --format csv
```

#### Specify custom output file
```bash
python pdf_extractor.py input.pdf --format json --output result.json
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `pdf_file` | Path to the PDF file (required) |
| `--format, -f` | Output format - `json` or `csv` (default: `json`) |
| `--output, -o` | Custom output file path (optional) |
| `--page, -p` | Extract specific page number (1-indexed) |
| `--whole, -w` | Extract entire document as a single combined block |

### Programmatic Usage

```python
from pdf_extractor import PDFExtractor

# Extract all pages
with PDFExtractor("document.pdf") as extractor:
    # Extract all pages
    pages_data = extractor.extract_all_pages()
    extractor.export_to_json(pages_data, "output.json")
    
    # Extract specific page
    page_data = extractor.extract_page(1)
    extractor.export_to_csv([page_data], "page1.csv")
    
    # Extract whole document
    whole_doc = extractor.extract_whole_document()
    extractor.export_to_json(whole_doc, "whole_document.json")
```

---

## 🌐 API Endpoints

All extract endpoints return **downloadable files** (JSON or CSV). Files automatically download when accessed via browser or API clients.

### 📋 Endpoint Overview

| Endpoint | Method | Format | Description |
|----------|--------|--------|-------------|
| `/extract/all/json` | POST | JSON | Extract all pages as JSON |
| `/extract/all/csv` | POST | CSV | Extract all pages as CSV |
| `/extract/page/json` | POST | JSON | Extract specific page as JSON |
| `/extract/page/csv` | POST | CSV | Extract specific page as CSV |
| `/extract/whole/json` | POST | JSON | Extract whole document as JSON |
| `/extract/whole/csv` | POST | CSV | Extract whole document as CSV |
| `/extract/lines` | POST | CSV | Extract line by line (default CSV) |
| `/extract/lines/json` | POST | JSON | Extract line by line as JSON |
| `/extract/lines/csv` | POST | CSV | Extract line by line as CSV |
| `/extract/sentences` | POST | CSV | Extract sentence by sentence (default CSV) ⭐ |
| `/extract/sentences/json` | POST | JSON | Extract sentence by sentence as JSON ⭐ |
| `/extract/sentences/csv` | POST | CSV | Extract sentence by sentence as CSV ⭐ |
| `/info` | POST | JSON | Get PDF metadata |

---

### 1️⃣ Extract All Pages

**JSON Endpoint:**
- **POST** `/extract/all/json` - Returns downloadable JSON file

**CSV Endpoint:**
- **POST** `/extract/all/csv` - Returns downloadable CSV file

Extract text from all pages of a PDF.

**Parameters:**
- `file` (form-data): PDF file to upload

**Example with curl:**
```bash
# JSON download
curl -X POST "http://localhost:8001/extract/all/json" \
  -F "file=@document.pdf" \
  -o output.json

# CSV download
curl -X POST "http://localhost:8001/extract/all/csv" \
  -F "file=@document.pdf" \
  -o output.csv
```

**Example with Python:**
```python
import requests

with open("document.pdf", "rb") as f:
    # Get JSON file
    response = requests.post(
        "http://localhost:8001/extract/all/json",
        files={"file": f}
    )
    with open("output.json", "wb") as out_file:
        out_file.write(response.content)
    
    # Get CSV file
    f.seek(0)  # Reset file pointer
    response = requests.post(
        "http://localhost:8001/extract/all/csv",
        files={"file": f}
    )
    with open("output.csv", "wb") as out_file:
        out_file.write(response.content)
```

---

### 2️⃣ Extract Specific Page

**JSON Endpoint:**
- **POST** `/extract/page/json?page=1` - Returns downloadable JSON file

**CSV Endpoint:**
- **POST** `/extract/page/csv?page=1` - Returns downloadable CSV file

Extract text from a specific page.

**Parameters:**
- `file` (form-data): PDF file to upload
- `page` (query, required): Page number (1-indexed)

**Example:**
```bash
# Extract page 1 as JSON
curl -X POST "http://localhost:8001/extract/page/json?page=1" \
  -F "file=@document.pdf" \
  -o page1.json

# Extract page 1 as CSV
curl -X POST "http://localhost:8001/extract/page/csv?page=1" \
  -F "file=@document.pdf" \
  -o page1.csv
```

---

### 3️⃣ Extract Whole Document

**JSON Endpoint:**
- **POST** `/extract/whole/json` - Returns downloadable JSON file

**CSV Endpoint:**
- **POST** `/extract/whole/csv` - Returns downloadable CSV file

Extract text from entire PDF as a single combined block.

**Parameters:**
- `file` (form-data): PDF file to upload

**Example:**
```bash
# Extract whole document as JSON
curl -X POST "http://localhost:8001/extract/whole/json" \
  -F "file=@document.pdf" \
  -o whole_document.json

# Extract whole document as CSV
curl -X POST "http://localhost:8001/extract/whole/csv" \
  -F "file=@document.pdf" \
  -o whole_document.csv
```

---

### 4️⃣ Extract Lines (Line-by-Line Extraction)

**Default Endpoint:**
- **POST** `/extract/lines` - Returns downloadable CSV file (default)

**JSON Endpoint:**
- **POST** `/extract/lines/json` - Returns downloadable JSON file

**CSV Endpoint:**
- **POST** `/extract/lines/csv` - Returns downloadable CSV file

Extract text line by line, where each line becomes a separate row in CSV or entry in JSON.

**Parameters:**
- `file` (form-data): PDF file to upload

**CSV Output Columns:**
- `line_number`: Sequential line number (1, 2, 3, ...)
- `page_number`: Page number where the line appears
- `text`: The actual line text

**Example:**
```bash
# Extract lines as CSV (default)
curl -X POST "http://localhost:8001/extract/lines" \
  -F "file=@document.pdf" \
  -o lines.csv

# Extract lines as JSON
curl -X POST "http://localhost:8001/extract/lines/json" \
  -F "file=@document.pdf" \
  -o lines.json

# Extract lines as CSV (explicit)
curl -X POST "http://localhost:8001/extract/lines/csv" \
  -F "file=@document.pdf" \
  -o lines.csv
```

**JSON Response Example:**
```json
{
  "filename": "document.pdf",
  "total_pages": 5,
  "total_lines": 150,
  "data": [
    {
      "line_number": 1,
      "page_number": 1,
      "text": "First line of text"
    },
    {
      "line_number": 2,
      "page_number": 1,
      "text": "Second line of text"
    }
  ]
}
```

---

### 5️⃣ Extract Sentences (Sentence-by-Sentence Extraction) ⭐ NEW

**Default Endpoint:**
- **POST** `/extract/sentences` - Returns downloadable CSV file (default)

**JSON Endpoint:**
- **POST** `/extract/sentences/json` - Returns downloadable JSON file

**CSV Endpoint:**
- **POST** `/extract/sentences/csv` - Returns downloadable CSV file

Extract text sentence by sentence, perfect for translation workflows! Each sentence is separated by punctuation marks and becomes a separate row.

**Features:**
- ✅ Splits on punctuation marks: `. ! ? ; : ,` (punctuation included in output)
- ✅ Splits on wide spaces (2+ spaces, tabs) - handles headers/subheaders
- ✅ Each sentence becomes a separate row
- ✅ Perfect for translation and text processing

**Parameters:**
- `file` (form-data): PDF file to upload

**CSV Output Columns:**
- `sentence_number`: Sequential sentence number (1, 2, 3, ...)
- `page_number`: Page number where the sentence appears
- `text`: The actual sentence text (with punctuation included)

**Example:**
```bash
# Extract sentences as CSV (default)
curl -X POST "http://localhost:8001/extract/sentences" \
  -F "file=@document.pdf" \
  -o sentences.csv

# Extract sentences as JSON
curl -X POST "http://localhost:8001/extract/sentences/json" \
  -F "file=@document.pdf" \
  -o sentences.json

# Extract sentences as CSV (explicit)
curl -X POST "http://localhost:8001/extract/sentences/csv" \
  -F "file=@document.pdf" \
  -o sentences.csv
```

**How it works:**

If your PDF contains:
```
This is a sentence. This is another sentence! Header Text    Subheader text; More text here.
```

The output will be:
- Row 1: "This is a sentence."
- Row 2: "This is another sentence!"
- Row 3: "Header Text" (separated by wide space)
- Row 4: "Subheader text;"
- Row 5: "More text here."

**JSON Response Example:**
```json
{
  "filename": "document.pdf",
  "total_pages": 5,
  "total_sentences": 120,
  "data": [
    {
      "sentence_number": 1,
      "page_number": 1,
      "text": "This is the first sentence."
    },
    {
      "sentence_number": 2,
      "page_number": 1,
      "text": "This is the second sentence!"
    }
  ]
}
```

---

### 6️⃣ Get PDF Info

**POST** `/info`

Get PDF metadata without extracting text.

**Parameters:**
- `file` (form-data): PDF file to upload

**Example:**
```bash
curl -X POST "http://localhost:8001/info" \
  -F "file=@document.pdf"
```

**Response:**
```json
{
  "filename": "document.pdf",
  "total_pages": 10,
  "file_size": 245678
}
```

---

## 📊 Output Formats

### JSON Format

**All pages:**
```json
[
  {
    "page_number": 1,
    "text": "Page 1 content...",
    "total_pages": 5
  },
  {
    "page_number": 2,
    "text": "Page 2 content...",
    "total_pages": 5
  }
]
```

**Single page:**
```json
{
  "page_number": 1,
  "text": "Page 1 content...",
  "total_pages": 5
}
```

**Whole document:**
```json
{
  "document": "document.pdf",
  "text": "Combined text from all pages...",
  "total_pages": 5
}
```

### CSV Format

**All Pages / Single Page Format:**
- `page_number`: Page number
- `text`: Extracted text content
- `total_pages`: Total number of pages

**Whole Document Format:**
- `document`: Document name
- `text`: Combined text from all pages
- `total_pages`: Total number of pages

**Lines Format:**
- `line_number`: Sequential line number (1, 2, 3, ...)
- `page_number`: Page number where the line appears
- `text`: The actual line text

**Sentences Format:**
- `sentence_number`: Sequential sentence number (1, 2, 3, ...)
- `page_number`: Page number where the sentence appears
- `text`: The actual sentence text (with punctuation included)

---

## 🛠️ Using Postman

When making requests in Postman:

1. ✅ All extract endpoints return downloadable files
2. ✅ Use the **"Save Response"** button to save the file
3. ✅ Or the file will automatically download in your browser
4. ✅ Files are named based on your PDF filename (e.g., `document_extracted.csv`)

**Tip:** If the file doesn't download automatically in Postman, use the "Save Response" → "Save to a file" option.

---

## 📦 Requirements

- Python 3.7+
- PyMuPDF (fitz) >= 1.23.0
- pandas >= 2.0.0
- fastapi >= 0.104.0
- uvicorn >= 0.24.0
- python-multipart >= 0.0.6

---

## 🎯 Use Cases

- 📚 **Document Processing** - Extract text from PDFs for analysis
- 🌍 **Translation Workflows** - Sentence-by-sentence extraction for translation
- 📊 **Data Analysis** - Convert PDFs to CSV for spreadsheet analysis
- 🔍 **Text Mining** - Extract structured data from PDF documents
- 🤖 **Automation** - Integrate PDF extraction into automated workflows
- 📝 **Content Management** - Extract and organize PDF content

---

## 📝 License

MIT License - feel free to use this project for any purpose!

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

<div align="center">

**Made with ❤️ for PDF text extraction**

</div>
