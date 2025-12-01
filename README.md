# PDF Extractor

A Python tool for extracting text from PDF files and exporting to CSV or JSON formats. Supports extraction of individual pages or entire documents.

## Features

- ✅ Extract text from PDF files
- ✅ Export to CSV or JSON format
- ✅ Extract individual pages or entire document
- ✅ **Line-by-line extraction** - Each line as a separate row
- ✅ Command-line interface
- ✅ **FastAPI web server** with REST API
- ✅ **Downloadable file responses** - All endpoints return downloadable files
- ✅ Separate endpoints for CSV and JSON formats
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

All extract endpoints return **downloadable files** (JSON or CSV). The file will automatically download when accessed via browser or API clients like Postman.

#### 1. Extract All Pages

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
curl -X POST "http://localhost:8000/extract/all/json" \
  -F "file=@document.pdf" \
  -o output.json

# CSV download
curl -X POST "http://localhost:8000/extract/all/csv" \
  -F "file=@document.pdf" \
  -o output.csv
```

**Example with Python:**
```python
import requests

with open("document.pdf", "rb") as f:
    # Get JSON file
    response = requests.post(
        "http://localhost:8000/extract/all/json",
        files={"file": f}
    )
    with open("output.json", "wb") as out_file:
        out_file.write(response.content)
    
    # Get CSV file
    f.seek(0)  # Reset file pointer
    response = requests.post(
        "http://localhost:8000/extract/all/csv",
        files={"file": f}
    )
    with open("output.csv", "wb") as out_file:
        out_file.write(response.content)
```

#### 2. Extract Specific Page

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
curl -X POST "http://localhost:8000/extract/page/json?page=1" \
  -F "file=@document.pdf" \
  -o page1.json

# Extract page 1 as CSV
curl -X POST "http://localhost:8000/extract/page/csv?page=1" \
  -F "file=@document.pdf" \
  -o page1.csv
```

#### 3. Extract Whole Document

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
curl -X POST "http://localhost:8000/extract/whole/json" \
  -F "file=@document.pdf" \
  -o whole_document.json

# Extract whole document as CSV
curl -X POST "http://localhost:8000/extract/whole/csv" \
  -F "file=@document.pdf" \
  -o whole_document.csv
```

#### 4. Extract Lines (Line-by-Line Extraction) ⭐ NEW

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
curl -X POST "http://localhost:8000/extract/lines" \
  -F "file=@document.pdf" \
  -o lines.csv

# Extract lines as JSON
curl -X POST "http://localhost:8000/extract/lines/json" \
  -F "file=@document.pdf" \
  -o lines.json

# Extract lines as CSV (explicit)
curl -X POST "http://localhost:8000/extract/lines/csv" \
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

#### 5. Get PDF Info

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
All CSV endpoints return downloadable CSV files with appropriate headers. Files are automatically downloaded when accessed via browser or API clients.

### Using Postman

When making requests in Postman:
1. All extract endpoints return downloadable files
2. Use the "Save Response" button to save the file
3. Or the file will automatically download in your browser
4. Files are named based on your PDF filename (e.g., `document_extracted.csv`)

## Requirements

- Python 3.7+
- PyMuPDF (fitz) >= 1.23.0
- pandas >= 2.0.0
- fastapi >= 0.104.0
- uvicorn >= 0.24.0
- python-multipart >= 0.0.6

## License

MIT

