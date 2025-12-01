"""
PDF Extractor - Extract text from PDFs and export to CSV or JSON
Supports extraction of individual pages or entire documents
"""

import fitz  # PyMuPDF
import json
import csv
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Union
import argparse


class PDFExtractor:
    """Extract text from PDF files and export to CSV or JSON"""
    
    def __init__(self, pdf_path: Union[str, Path]):
        """
        Initialize PDF extractor
        
        Args:
            pdf_path: Path to the PDF file
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        self.doc = fitz.open(str(self.pdf_path))
        self.total_pages = len(self.doc)
    
    def extract_page(self, page_num: int) -> Dict[str, Union[str, int]]:
        """
        Extract text from a specific page
        
        Args:
            page_num: Page number (1-indexed)
            
        Returns:
            Dictionary with page number and extracted text
        """
        if page_num < 1 or page_num > self.total_pages:
            raise ValueError(f"Page number must be between 1 and {self.total_pages}")
        
        page = self.doc[page_num - 1]  # Convert to 0-indexed
        text = page.get_text()
        
        return {
            "page_number": page_num,
            "text": text.strip(),
            "total_pages": self.total_pages
        }
    
    def extract_all_pages(self) -> List[Dict[str, Union[str, int]]]:
        """
        Extract text from all pages
        
        Returns:
            List of dictionaries, each containing page number and text
        """
        pages_data = []
        for page_num in range(1, self.total_pages + 1):
            page_data = self.extract_page(page_num)
            pages_data.append(page_data)
        
        return pages_data
    
    def extract_whole_document(self) -> Dict[str, Union[str, int]]:
        """
        Extract text from entire document as a single block
        
        Returns:
            Dictionary with combined text from all pages
        """
        all_text = []
        for page_num in range(1, self.total_pages + 1):
            page = self.doc[page_num - 1]
            text = page.get_text()
            all_text.append(text.strip())
        
        combined_text = "\n\n".join(all_text)
        
        return {
            "document": str(self.pdf_path.name),
            "text": combined_text,
            "total_pages": self.total_pages
        }
    
    def export_to_json(self, data: Union[Dict, List[Dict]], output_path: Optional[str] = None) -> str:
        """
        Export extracted data to JSON file
        
        Args:
            data: Dictionary or list of dictionaries to export
            output_path: Optional output file path. If None, generates from PDF name
            
        Returns:
            Path to the created JSON file
        """
        if output_path is None:
            output_path = self.pdf_path.stem + "_extracted.json"
        
        output_path = Path(output_path)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return str(output_path)
    
    def export_to_csv(self, data: Union[Dict, List[Dict]], output_path: Optional[str] = None) -> str:
        """
        Export extracted data to CSV file
        
        Args:
            data: Dictionary or list of dictionaries to export
            output_path: Optional output file path. If None, generates from PDF name
            
        Returns:
            Path to the created CSV file
        """
        if output_path is None:
            output_path = self.pdf_path.stem + "_extracted.csv"
        
        output_path = Path(output_path)
        
        # Convert to list if single dictionary
        if isinstance(data, dict):
            data = [data]
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Export to CSV
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        return str(output_path)
    
    def close(self):
        """Close the PDF document"""
        if self.doc:
            self.doc.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


def main():
    """Command-line interface for PDF extraction"""
    parser = argparse.ArgumentParser(
        description="Extract text from PDF files and export to CSV or JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract all pages to JSON
  python pdf_extractor.py input.pdf --format json
  
  # Extract all pages to CSV
  python pdf_extractor.py input.pdf --format csv
  
  # Extract specific page to JSON
  python pdf_extractor.py input.pdf --format json --page 1
  
  # Extract whole document (combined) to CSV
  python pdf_extractor.py input.pdf --format csv --whole
  
  # Custom output file
  python pdf_extractor.py input.pdf --format json --output result.json
        """
    )
    
    parser.add_argument('pdf_file', help='Path to the PDF file')
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'csv'],
        default='json',
        help='Output format (default: json)'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file path (default: auto-generated from PDF name)'
    )
    parser.add_argument(
        '--page', '-p',
        type=int,
        help='Extract specific page number (1-indexed). If not specified, extracts all pages'
    )
    parser.add_argument(
        '--whole', '-w',
        action='store_true',
        help='Extract entire document as a single block (combines all pages)'
    )
    
    args = parser.parse_args()
    
    try:
        with PDFExtractor(args.pdf_file) as extractor:
            print(f"Processing PDF: {args.pdf_file}")
            print(f"Total pages: {extractor.total_pages}")
            
            # Determine extraction mode
            if args.whole:
                print("Extracting whole document...")
                data = extractor.extract_whole_document()
            elif args.page:
                print(f"Extracting page {args.page}...")
                data = extractor.extract_page(args.page)
            else:
                print("Extracting all pages...")
                data = extractor.extract_all_pages()
            
            # Export data
            if args.format == 'json':
                output_file = extractor.export_to_json(data, args.output)
                print(f"✓ Exported to JSON: {output_file}")
            else:
                output_file = extractor.export_to_csv(data, args.output)
                print(f"✓ Exported to CSV: {output_file}")
            
            # Print summary
            if isinstance(data, list):
                print(f"✓ Extracted {len(data)} page(s)")
            else:
                if 'page_number' in data:
                    print(f"✓ Extracted page {data['page_number']}")
                else:
                    print(f"✓ Extracted whole document ({data['total_pages']} pages)")
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except ValueError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

