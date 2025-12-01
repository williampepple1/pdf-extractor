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
            "extract_all": "/extract/all",
            "extract_page": "/extract/page",
            "extract_whole": "/extract/whole",
            "info": "/info"
        }
    }


@app.post("/extract/all")
async def extract_all_pages(
    file: UploadFile = File(...),
    format: str = Query("json", regex="^(json|csv)$", description="Output format: json or csv")
):
    """
    Extract text from all pages of a PDF
    
    - **file**: PDF file to extract from
    - **format**: Output format (json or csv)
    
    Returns extracted data in the specified format
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
            data = extractor.extract_all_pages()
            
            if format == "json":
                return JSONResponse(content={
                    "filename": file.filename,
                    "total_pages": extractor.total_pages,
                    "data": data
                })
            else:  # CSV
                # Create CSV in memory
                import pandas as pd
                df = pd.DataFrame(data)
                
                # Convert to CSV string
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, encoding='utf-8')
                csv_content = csv_buffer.getvalue()
                
                return StreamingResponse(
                    io.BytesIO(csv_content.encode('utf-8')),
                    media_type="text/csv",
                    headers={
                        "Content-Disposition": f"attachment; filename={Path(file.filename).stem}_extracted.csv"
                    }
                )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/extract/page")
async def extract_page(
    file: UploadFile = File(...),
    page: int = Query(..., ge=1, description="Page number (1-indexed)"),
    format: str = Query("json", regex="^(json|csv)$", description="Output format: json or csv")
):
    """
    Extract text from a specific page of a PDF
    
    - **file**: PDF file to extract from
    - **page**: Page number to extract (1-indexed)
    - **format**: Output format (json or csv)
    
    Returns extracted data in the specified format
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
            if page > extractor.total_pages:
                raise HTTPException(
                    status_code=400,
                    detail=f"Page {page} does not exist. PDF has {extractor.total_pages} pages"
                )
            
            data = extractor.extract_page(page)
            
            if format == "json":
                return JSONResponse(content={
                    "filename": file.filename,
                    "page": page,
                    "total_pages": extractor.total_pages,
                    "data": data
                })
            else:  # CSV
                import pandas as pd
                df = pd.DataFrame([data])
                
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, encoding='utf-8')
                csv_content = csv_buffer.getvalue()
                
                return StreamingResponse(
                    io.BytesIO(csv_content.encode('utf-8')),
                    media_type="text/csv",
                    headers={
                        "Content-Disposition": f"attachment; filename={Path(file.filename).stem}_page_{page}.csv"
                    }
                )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


@app.post("/extract/whole")
async def extract_whole_document(
    file: UploadFile = File(...),
    format: str = Query("json", regex="^(json|csv)$", description="Output format: json or csv")
):
    """
    Extract text from entire PDF as a single combined block
    
    - **file**: PDF file to extract from
    - **format**: Output format (json or csv)
    
    Returns extracted data in the specified format
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
            data = extractor.extract_whole_document()
            
            if format == "json":
                return JSONResponse(content={
                    "filename": file.filename,
                    "total_pages": extractor.total_pages,
                    "data": data
                })
            else:  # CSV
                import pandas as pd
                df = pd.DataFrame([data])
                
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, encoding='utf-8')
                csv_content = csv_buffer.getvalue()
                
                return StreamingResponse(
                    io.BytesIO(csv_content.encode('utf-8')),
                    media_type="text/csv",
                    headers={
                        "Content-Disposition": f"attachment; filename={Path(file.filename).stem}_whole_document.csv"
                    }
                )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


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

