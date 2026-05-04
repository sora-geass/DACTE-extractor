# Stack Research: DACTE PDF Extractor

## Recommended Stack (2025)

### Backend
- **Python 3.11+** — Mature ecosystem for PDF/data processing
- **Flask 3.x** — Lightweight web framework, ideal for file upload/download workflows
- **pdfplumber 0.11+** — Layout-aware PDF text extraction (built on pdfminer.six)
- **pandas 2.x** — Data structuring and manipulation
- **openpyxl 3.x** — Excel file generation with cell formatting (currency, styles)

### Why pdfplumber over PyPDF2
- pdfplumber provides coordinate-based text extraction and layout preservation
- Better table detection for structured documents like DACTE
- Visual debugging capabilities (`.to_image()`, `.debug_tablefinder()`)
- PyPDF2 returns raw text dumps without spatial awareness — unreliable for structured docs

### Frontend
- **Vanilla HTML/CSS/JS** — Simple upload form, no framework overhead needed
- **Modern CSS** — Glassmorphism, gradients, dark mode for premium feel

### Key Libraries
| Library | Version | Purpose |
|---------|---------|---------|
| Flask | 3.x | Web server, file upload/download |
| pdfplumber | 0.11+ | PDF text extraction with layout |
| pandas | 2.x | DataFrame for structuring extracted data |
| openpyxl | 3.x | Excel generation with formatting |
| Werkzeug | 3.x | Secure file handling (comes with Flask) |

### What NOT to Use
- **PyPDF2/pypdf** — Poor at structured document extraction, no layout awareness
- **tabula-py** — Requires Java runtime, overkill for this use case
- **camelot** — Heavy dependency chain, not needed for text-based DACTEs
- **OCR (pytesseract)** — Only needed for scanned PDFs, out of scope

## Confidence: HIGH
DACTE extraction with pdfplumber + regex is a well-proven pattern in the Brazilian dev community.
