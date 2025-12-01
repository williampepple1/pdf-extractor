"""
FastAPI server for PDF extraction
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from pathlib import Path
from typing import Optional
import io
import json

from pdf_extractor import PDFExtractor

app = FastAPI(
    title="PDF Extractor API",
    description="Extract text from PDF files and export to CSV or JSON",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "PDF Extractor API",
        "version": "1.0.0",
        "endpoints": {
            "extract_all_json": "/extract/all/json",
            "extract_all_csv": "/extract/all/csv",
            "extract_page_json": "/extract/page/json",
            "extract_page_csv": "/extract/page/csv",
            "extract_whole_json": "/extract/whole/json",
            "extract_whole_csv": "/extract/whole/csv",
            "extract_lines": "/extract/lines (defaults to CSV)",
            "extract_lines_json": "/extract/lines/json",
            "extract_lines_csv": "/extract/lines/csv",
            "info": "/info"
        }
    }


# Helper function to process PDF file
async def process_pdf_file(file: UploadFile):
    """Helper to save uploaded PDF to temporary file"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    return tmp_path, file.filename


# Extract All Pages - JSON
@app.post("/extract/all/json")
async def extract_all_pages_json(file: UploadFile = File(...)):
    """
    Extract text from all pages of a PDF and return as downloadable JSON file
    
    - **file**: PDF file to extract from
    
    Returns extracted data as downloadable JSON file
    """
    tmp_path = None
    try:
        tmp_path, filename = await process_pdf_file(file)
        
        with PDFExtractor(tmp_path) as extractor:
            data = extractor.extract_all_pages()
            
            # Create JSON content
            json_data = {
                "filename": filename,
                "total_pages": extractor.total_pages,
                "data": data
            }
            
            json_content = json.dumps(json_data, indent=2, ensure_ascii=False)
            
            # Properly encode filename for Content-Disposition header
            safe_filename = Path(filename).stem + "_extracted.json"
            
            return StreamingResponse(
                io.BytesIO(json_content.encode('utf-8')),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{safe_filename}"',
                    "Content-Type": "application/json"
                }
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# Extract All Pages - CSV
@app.post("/extract/all/csv")
async def extract_all_pages_csv(file: UploadFile = File(...)):
    """
    Extract text from all pages of a PDF and return as CSV
    
    - **file**: PDF file to extract from
    
    Returns extracted data as CSV file download
    """
    tmp_path = None
    try:
        tmp_path, filename = await process_pdf_file(file)
        
        with PDFExtractor(tmp_path) as extractor:
            data = extractor.extract_all_pages()
            
            # Create CSV in memory
            import pandas as pd
            df = pd.DataFrame(data)
            
            # Convert to CSV string
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8')
            csv_content = csv_buffer.getvalue()
            
            safe_filename = Path(filename).stem + "_extracted.csv"
            
            return StreamingResponse(
                io.BytesIO(csv_content.encode('utf-8')),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{safe_filename}"',
                    "Content-Type": "text/csv"
                }
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# Extract Specific Page - JSON
@app.post("/extract/page/json")
async def extract_page_json(
    file: UploadFile = File(...),
    page: int = Query(..., ge=1, description="Page number (1-indexed)")
):
    """
    Extract text from a specific page of a PDF and return as downloadable JSON file
    
    - **file**: PDF file to extract from
    - **page**: Page number to extract (1-indexed)
    
    Returns extracted data as downloadable JSON file
    """
    tmp_path = None
    try:
        tmp_path, filename = await process_pdf_file(file)
        
        with PDFExtractor(tmp_path) as extractor:
            if page > extractor.total_pages:
                raise HTTPException(
                    status_code=400,
                    detail=f"Page {page} does not exist. PDF has {extractor.total_pages} pages"
                )
            
            data = extractor.extract_page(page)
            
            # Create JSON content
            json_data = {
                "filename": filename,
                "page": page,
                "total_pages": extractor.total_pages,
                "data": data
            }
            
            json_content = json.dumps(json_data, indent=2, ensure_ascii=False)
            
            # Properly encode filename for Content-Disposition header
            safe_filename = Path(filename).stem + f"_page_{page}.json"
            
            return StreamingResponse(
                io.BytesIO(json_content.encode('utf-8')),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{safe_filename}"',
                    "Content-Type": "application/json"
                }
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# Extract Specific Page - CSV
@app.post("/extract/page/csv")
async def extract_page_csv(
    file: UploadFile = File(...),
    page: int = Query(..., ge=1, description="Page number (1-indexed)")
):
    """
    Extract text from a specific page of a PDF and return as CSV
    
    - **file**: PDF file to extract from
    - **page**: Page number to extract (1-indexed)
    
    Returns extracted data as CSV file download
    """
    tmp_path = None
    try:
        tmp_path, filename = await process_pdf_file(file)
        
        with PDFExtractor(tmp_path) as extractor:
            if page > extractor.total_pages:
                raise HTTPException(
                    status_code=400,
                    detail=f"Page {page} does not exist. PDF has {extractor.total_pages} pages"
                )
            
            data = extractor.extract_page(page)
            
            import pandas as pd
            df = pd.DataFrame([data])
            
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8')
            csv_content = csv_buffer.getvalue()
            
            safe_filename = Path(filename).stem + f"_page_{page}.csv"
            
            return StreamingResponse(
                io.BytesIO(csv_content.encode('utf-8')),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{safe_filename}"',
                    "Content-Type": "text/csv"
                }
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# Extract Whole Document - JSON
@app.post("/extract/whole/json")
async def extract_whole_document_json(file: UploadFile = File(...)):
    """
    Extract text from entire PDF as a single combined block and return as downloadable JSON file
    
    - **file**: PDF file to extract from
    
    Returns extracted data as downloadable JSON file
    """
    tmp_path = None
    try:
        tmp_path, filename = await process_pdf_file(file)
        
        with PDFExtractor(tmp_path) as extractor:
            data = extractor.extract_whole_document()
            
            # Create JSON content
            json_data = {
                "filename": filename,
                "total_pages": extractor.total_pages,
                "data": data
            }
            
            json_content = json.dumps(json_data, indent=2, ensure_ascii=False)
            
            # Properly encode filename for Content-Disposition header
            safe_filename = Path(filename).stem + "_whole_document.json"
            
            return StreamingResponse(
                io.BytesIO(json_content.encode('utf-8')),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{safe_filename}"',
                    "Content-Type": "application/json"
                }
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# Extract Whole Document - CSV
@app.post("/extract/whole/csv")
async def extract_whole_document_csv(file: UploadFile = File(...)):
    """
    Extract text from entire PDF as a single combined block and return as CSV
    
    - **file**: PDF file to extract from
    
    Returns extracted data as CSV file download
    """
    tmp_path = None
    try:
        tmp_path, filename = await process_pdf_file(file)
        
        with PDFExtractor(tmp_path) as extractor:
            data = extractor.extract_whole_document()
            
            import pandas as pd
            df = pd.DataFrame([data])
            
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8')
            csv_content = csv_buffer.getvalue()
            
            safe_filename = Path(filename).stem + "_whole_document.csv"
            
            return StreamingResponse(
                io.BytesIO(csv_content.encode('utf-8')),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{safe_filename}"',
                    "Content-Type": "text/csv"
                }
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# Extract Lines - JSON
@app.post("/extract/lines/json")
async def extract_lines_json(file: UploadFile = File(...)):
    """
    Extract text from PDF line by line, where each line becomes a separate entry
    
    - **file**: PDF file to extract from
    
    Returns extracted data as downloadable JSON file with each line as a separate entry
    """
    tmp_path = None
    try:
        tmp_path, filename = await process_pdf_file(file)
        
        with PDFExtractor(tmp_path) as extractor:
            lines_data = []
            line_number = 1
            
            # Extract from all pages
            for page_num in range(1, extractor.total_pages + 1):
                page = extractor.doc[page_num - 1]
                text = page.get_text()
                
                # Split text into lines
                lines = text.split('\n')
                
                for line in lines:
                    line_text = line.strip()
                    # Only include non-empty lines
                    if line_text:
                        lines_data.append({
                            "line_number": line_number,
                            "page_number": page_num,
                            "text": line_text
                        })
                        line_number += 1
            
            json_data = {
                "filename": filename,
                "total_pages": extractor.total_pages,
                "total_lines": len(lines_data),
                "data": lines_data
            }
            
            json_content = json.dumps(json_data, indent=2, ensure_ascii=False)
            safe_filename = Path(filename).stem + "_lines.json"
            
            return StreamingResponse(
                io.BytesIO(json_content.encode('utf-8')),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{safe_filename}"',
                    "Content-Type": "application/json"
                }
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# Extract Lines - CSV
@app.post("/extract/lines/csv")
async def extract_lines_csv(file: UploadFile = File(...)):
    """
    Extract text from PDF line by line, where each line becomes a separate row in CSV
    
    - **file**: PDF file to extract from
    
    Returns extracted data as downloadable CSV file with each line as a separate row
    """
    tmp_path = None
    try:
        tmp_path, filename = await process_pdf_file(file)
        
        with PDFExtractor(tmp_path) as extractor:
            lines_data = []
            line_number = 1
            
            # Extract from all pages
            for page_num in range(1, extractor.total_pages + 1):
                page = extractor.doc[page_num - 1]
                text = page.get_text()
                
                # Split text into lines
                lines = text.split('\n')
                
                for line in lines:
                    line_text = line.strip()
                    # Only include non-empty lines
                    if line_text:
                        lines_data.append({
                            "line_number": line_number,
                            "page_number": page_num,
                            "text": line_text
                        })
                        line_number += 1
            
            # Create CSV
            import pandas as pd
            df = pd.DataFrame(lines_data)
            
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8')
            csv_content = csv_buffer.getvalue()
            
            safe_filename = Path(filename).stem + "_lines.csv"
            
            return StreamingResponse(
                io.BytesIO(csv_content.encode('utf-8')),
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f'attachment; filename="{safe_filename}"',
                    "Content-Type": "text/csv"
                }
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


# Extract Lines - Default (CSV) - Must be after extract_lines_csv is defined
@app.post("/extract/lines")
async def extract_lines(file: UploadFile = File(...)):
    """
    Extract text from PDF line by line, where each line becomes a separate row in CSV (default)
    
    - **file**: PDF file to extract from
    
    Returns extracted data as downloadable CSV file with each line as a separate row
    """
    # Call the CSV endpoint function
    return await extract_lines_csv(file)


@app.post("/info")
async def get_pdf_info(file: UploadFile = File(...)):
    """
    Get information about a PDF file without extracting text
    
    - **file**: PDF file to analyze
    
    Returns PDF metadata and page count
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name
    
    try:
        with PDFExtractor(tmp_path) as extractor:
            return JSONResponse(content={
                "filename": file.filename,
                "total_pages": extractor.total_pages,
                "file_size": len(content)
            })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
