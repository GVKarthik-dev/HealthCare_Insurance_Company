import io
from pypdf import PdfReader
from typing import List

def extract_pages_text(file_bytes: bytes) -> List[str]:
    """Extracts text from each page of the PDF."""
    reader = PdfReader(io.BytesIO(file_bytes))
    pages_text = []
    for page in reader.pages:
        pages_text.append(page.extract_text() or "")
    return pages_text

def get_page_count(file_bytes: bytes) -> int:
    reader = PdfReader(io.BytesIO(file_bytes))
    return len(reader.pages)
