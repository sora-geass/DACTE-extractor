---
phase: 1
plan: 01
title: "Flask Backend with PDF Upload, Extraction, and Excel Export"
wave: 1
depends_on: []
files_modified:
  - app.py
  - extractor.py
  - requirements.txt
  - templates/index.html
  - static/css/style.css
  - static/js/main.js
autonomous: true
requirements_addressed: [UPLD-01, UPLD-02, UPLD-03, UPLD-04, EXTR-01, EXTR-02, EXTR-03, EXTR-04, EXTR-05, EXTR-06, EXTR-07, EXTR-08, EXPO-01, EXPO-02, EXPO-03, EXPO-04, EXPO-05, UI-01, UI-02, UI-03]
---

# Plan 01: Complete DACTE PDF Extractor Application

<objective>
Build the complete DACTE PDF Extractor web application: Flask backend with PDF upload endpoint, pdfplumber-based extraction engine with regex parsing, Excel generation with openpyxl formatting, and a polished modern frontend with drag-and-drop upload.
</objective>

<must_haves>
- Flask app serves upload page and handles PDF file submissions
- pdfplumber extracts text from DACTE PDFs
- Regex patterns extract: CTE, Planta, Valor, Valor serviço, Container, Data emissão
- Brazilian number format (1.262.526,08) correctly converted to float
- Excel output with correct column order and R$ currency formatting
- Missing container handled gracefully (N/A)
- File downloads as .xlsx from browser
- Modern, polished UI with drag-and-drop
</must_haves>

## Tasks

<task id="1">
<title>Create requirements.txt with all dependencies</title>
<read_first>
- None (new file)
</read_first>
<action>
Create requirements.txt with:
```
flask>=3.0
pdfplumber>=0.11
pandas>=2.0
openpyxl>=3.1
werkzeug>=3.0
```
</action>
<acceptance_criteria>
- requirements.txt contains flask, pdfplumber, pandas, openpyxl, werkzeug
- All versions specified with >= minimum
</acceptance_criteria>
</task>

<task id="2">
<title>Create PDF extraction module (extractor.py)</title>
<read_first>
- DACTES.pdf (sample document for pattern testing)
</read_first>
<action>
Create extractor.py with:

1. `parse_br_currency(value_str)` — converts "1.262.526,08" to float 1262526.08 by stripping dots, replacing comma with dot
2. `extract_dacte_data(pdf_path)` — opens PDF with pdfplumber, concatenates all pages text, applies regex:
   - CTE: r'(?:CT-e\s*N[.º°]?\s*|NÚMERO\s*)\n?\s*(\d+)' — extract number, strip leading zeros with lstrip('0') or int() conversion
   - Data emissão: r'DATA\s*DE\s*EMISSÃO\s*\n?\s*(\d{2}/\d{2}/\d{4})'
   - Planta (município destinatário): r'DESTINAT[ÁA]RIO.*?MUNIC[ÍI]PIO\s*\n?\s*([A-ZÀ-Ú\s]+?)(?:\s*/\s*\w{2})?\s*(?:CEP|$)'
   - Valor total mercadoria: r'VALOR\s*TOTAL\s*(?:DA\s*)?MERCADORIA\s*\n?\s*([\d.,]+)'
   - Valor serviço: r'(?:VALOR\s*(?:TOTAL\s*)?(?:DA\s*)?PRESTA[ÇC][ÃA]O|VALOR\s*A\s*RECEBER)\s*\n?\s*([\d.,]+)'
   - Container: r'CONTAINER?:\s*([A-Z]{4}\d{7})'
3. Return dict with keys: cte, tipo (empty string), data_emissao, planta, valor, valor_servico, conteiner
4. Handle missing container with "N/A"
5. `process_multiple_pdfs(file_paths)` — calls extract_dacte_data for each, returns list of dicts
</action>
<acceptance_criteria>
- extractor.py contains function extract_dacte_data
- extractor.py contains function parse_br_currency
- parse_br_currency("1.262.526,08") returns 1262526.08
- Container extraction returns "N/A" when not found
- Function handles multi-page PDFs by concatenating text
</acceptance_criteria>
</task>

<task id="3">
<title>Create Flask app with upload and download endpoints (app.py)</title>
<read_first>
- extractor.py (extraction functions to import)
</read_first>
<action>
Create app.py with:

1. Flask app configuration:
   - UPLOAD_FOLDER = tempfile.mkdtemp()
   - MAX_CONTENT_LENGTH = 50 * 1024 * 1024 (50MB)
   - ALLOWED_EXTENSIONS = {'pdf'}

2. Routes:
   - GET / — render templates/index.html
   - POST /upload — accept multiple PDF files, validate extensions, call extractor, generate Excel, return download
   
3. Excel generation function `generate_excel(data_list)`:
   - Create DataFrame with columns: CTE, Tipo, Data emissão, Planta, Valor, Valor serviço, CONTEINER
   - Write to BytesIO using openpyxl engine
   - Apply number_format 'R$ #,##0.00' to Valor and Valor serviço columns
   - Apply header styling (dark blue background #1B2A4A, white text, bold)
   - Auto-fit column widths
   - Return BytesIO object

4. Error handling:
   - Non-PDF files: return JSON error with 400 status
   - Extraction failures: include error info in response, continue with other files
   - Empty upload: return JSON error

5. send_file with mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
</action>
<acceptance_criteria>
- app.py contains Flask app with routes / and /upload
- app.py imports from extractor module
- Excel generation uses openpyxl with number_format 'R$ #,##0.00'
- Header cells have PatternFill with dark blue color
- Non-PDF files rejected with 400 status
- send_file returns .xlsx download
</acceptance_criteria>
</task>

<task id="4">
<title>Create modern frontend (HTML + CSS + JS)</title>
<read_first>
- None (new files)
</read_first>
<action>
Create templates/index.html:
- Modern HTML5 page with meta charset, viewport
- Title: "DACTE PDF Extractor"
- Drag-and-drop upload area with visual feedback
- File list showing selected PDFs
- Processing spinner/animation during upload
- Results table showing extracted data summary
- Download button for Excel file
- Link to static CSS and JS

Create static/css/style.css:
- Dark theme with gradient background (#0a0a1a to #1a1a2e)
- Glassmorphism card for upload area (backdrop-filter: blur, semi-transparent bg)
- Upload zone with dashed border, hover/dragover effects (border color change, scale)
- Smooth animations: fadeIn, slideUp, pulse for processing
- Typography: Inter font from Google Fonts
- Color palette: primary #4f46e5 (indigo), accent #06b6d4 (cyan), success #10b981
- Responsive design for mobile
- Table styling with alternating rows, hover effects
- Button with gradient background, hover transform

Create static/js/main.js:
- Drag and drop event handlers (dragover, dragleave, drop)
- File input change handler
- FormData upload via fetch POST to /upload
- Processing state management (show/hide spinner)
- Display results in table after successful extraction
- Trigger file download for Excel
- Error handling with user-friendly messages
</action>
<acceptance_criteria>
- templates/index.html exists with drag-drop upload area
- static/css/style.css has dark theme with glassmorphism
- static/js/main.js handles drag-drop and fetch upload
- CSS contains @import for Inter font
- JS displays processing indicator during upload
- JS shows results table with extracted data
</acceptance_criteria>
</task>

<verification>
1. `pip install -r requirements.txt` completes without errors
2. `python app.py` starts Flask server on port 5000
3. Upload DACTES.pdf via the web interface
4. Excel file downloads with correct data
5. CTE number extracted correctly (e.g., 59966)
6. Valor and Valor serviço are numbers in Excel (not text)
7. Currency formatting shows R$ prefix in Excel
8. Container code extracted or "N/A" shown
</verification>
