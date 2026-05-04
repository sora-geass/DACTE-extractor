# Research Summary: DACTE PDF Extractor

## Stack Decision
**Python + Flask + pdfplumber + pandas + openpyxl** — proven, lightweight, well-suited for structured PDF extraction and Excel generation. No heavy frameworks needed.

## Table Stakes Features
- PDF upload (single + batch)
- Regex-based field extraction (CTE, Planta, Valor, Valor serviço, Container, Data emissão)
- Brazilian currency format conversion (BR → float)
- Excel export with proper number formatting (R$ currency)
- Graceful handling of missing fields (Container = N/A)
- File download from browser

## Key Watch-Outs
1. **Number format conversion** — Must strip dots, replace comma with dot before float()
2. **Excel cell format** — Write floats, not strings; apply number_format after
3. **Regex flexibility** — Account for label variations across DACTE generators
4. **Text ordering** — Use layout=True in pdfplumber for reliable spatial extraction
5. **Security** — Validate uploads, limit file size, use secure_filename

## Architecture
Simple request-response flow:
1. User uploads PDF(s) → Flask receives files
2. pdfplumber extracts text → regex parses fields
3. pandas structures data → openpyxl formats Excel
4. Flask sends .xlsx as download attachment

No database, no auth, no persistent storage needed.
