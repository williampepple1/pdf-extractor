# PDF Extractor

A Python tool for extracting text from PDF files and exporting to CSV or JSON formats. Supports extraction of individual pages or entire documents.

## Features

- ✅ Extract text from PDF files
- ✅ Export to CSV or JSON format
- ✅ Extract individual pages or entire document
- ✅ Command-line interface
- ✅ **FastAPI web server** with REST API
- ✅ Programmatic API for integration
- ✅ Handles complex PDF layouts

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

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

- `pdf_file`: Path to the PDF file (required)
- `--format, -f`: Output format - `json` or `csv` (default: `json`)
- `--output, -o`: Custom output file path (optional)
- `--page, -p`: Extract specific page number (1-indexed)
- `--whole, -w`: Extract entire document as a single combined block

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

## Output Formats

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

The CSV format contains columns:
- `page_number`: Page number (if applicable)
- `text`: Extracted text content
- `total_pages`: Total number of pages
- `document`: Document name (for whole document extraction)

## FastAPI Web Server

### Starting the Server

```bash
# Run the FastAPI server
python app.py

# Or using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The server will start at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Endpoints

#### 1. Extract All Pages
**POST** `/extract/all`

Extract text from all pages of a PDF.

**Parameters:**
- `file` (form-data): PDF file to upload
- `format` (query, optional): Output format - `json` or `csv` (default: `json`)

**Example with curl:**
```bash
# JSON response
curl -X POST "http://localhost:8000/extract/all?format=json" \
  -F "file=@document.pdf"

# CSV download
curl -X POST "http://localhost:8000/extract/all?format=csv" \
  -F "file=@document.pdf" \
  -o output.csv
```

**Example with Python:**
```python
import requests

with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/extract/all",
        files={"file": f},
        params={"format": "json"}
    )
    data = response.json()
    print(data)
```

#### 2. Extract Specific Page
**POST** `/extract/page`

Extract text from a specific page.

**Parameters:**
- `file` (form-data): PDF file to upload
- `page` (query, required): Page number (1-indexed)
- `format` (query, optional): Output format - `json` or `csv` (default: `json`)

**Example:**
```bash
curl -X POST "http://localhost:8000/extract/page?page=1&format=json" \
  -F "file=@document.pdf"
```

#### 3. Extract Whole Document
**POST** `/extract/whole`

Extract text from entire PDF as a single combined block.

**Parameters:**
- `file` (form-data): PDF file to upload
- `format` (query, optional): Output format - `json` or `csv` (default: `json`)

**Example:**
```bash
curl -X POST "http://localhost:8000/extract/whole?format=csv" \
  -F "file=@document.pdf" \
  -o whole_document.csv
```

#### 4. Get PDF Info
**POST** `/info`

Get PDF metadata without extracting text.

**Parameters:**
- `file` (form-data): PDF file to upload

**Example:**
```bash
curl -X POST "http://localhost:8000/info" \
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

### API Response Examples

**JSON Response (all pages):**
```json
{
  "filename": "document.pdf",
  "total_pages": 5,
  "data": [
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
}
```

**CSV Response:**
Returns a downloadable CSV file with appropriate headers.

## Requirements

- Python 3.7+
- PyMuPDF (fitz) >= 1.23.0
- pandas >= 2.0.0
- fastapi >= 0.104.0
- uvicorn >= 0.24.0
- python-multipart >= 0.0.6

## License

MIT

