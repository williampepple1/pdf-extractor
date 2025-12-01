"""
Example usage of PDFExtractor
"""

from pdf_extractor import PDFExtractor

def example_usage():
    """Demonstrate various ways to use PDFExtractor"""
    
    pdf_file = "sample.pdf"  # Replace with your PDF file path
    
    try:
        with PDFExtractor(pdf_file) as extractor:
            print(f"PDF has {extractor.total_pages} pages\n")
            
            # Example 1: Extract all pages to JSON
            print("Example 1: Extracting all pages to JSON...")
            all_pages = extractor.extract_all_pages()
            extractor.export_to_json(all_pages, "all_pages.json")
            print(f"✓ Exported {len(all_pages)} pages to all_pages.json\n")
            
            # Example 2: Extract specific page to CSV
            print("Example 2: Extracting page 1 to CSV...")
            page_1 = extractor.extract_page(1)
            extractor.export_to_csv([page_1], "page_1.csv")
            print("✓ Exported page 1 to page_1.csv\n")
            
            # Example 3: Extract whole document to JSON
            print("Example 3: Extracting whole document to JSON...")
            whole_doc = extractor.extract_whole_document()
            extractor.export_to_json(whole_doc, "whole_document.json")
            print("✓ Exported whole document to whole_document.json\n")
            
            # Example 4: Access extracted data directly
            print("Example 4: Accessing extracted text directly...")
            page_data = extractor.extract_page(1)
            print(f"Page 1 text preview: {page_data['text'][:100]}...")
            
    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_file}' not found.")
        print("Please update the pdf_file variable with a valid PDF path.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    example_usage()

