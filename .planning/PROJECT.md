# DACTE PDF Extractor

## What This Is

A web application that allows users to upload DACTE (Documento Auxiliar do Conhecimento de Transporte Eletrônico) PDF files and automatically extracts structured transport data — CTE number, destination plant, cargo value, service value, container code, and emission date — exporting the results as a formatted Excel (.xlsx) spreadsheet ready for accounting and logistics workflows.

## Core Value

Users can upload one or more DACTE PDFs and instantly receive a clean, correctly formatted Excel spreadsheet with all extracted transport data — no manual data entry required.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Web interface for PDF upload (single and batch)
- [ ] PDF text extraction using pdfplumber with regex-based field parsing
- [ ] Extract CTE number from header (CT-e N. / NÚMERO), strip leading zeros
- [ ] Extract Planta (MUNICÍPIO) from DESTINATÁRIO block
- [ ] Extract Valor (VALOR TOTAL DA MERCADORIA) as float
- [ ] Extract Valor serviço (VALOR TOTAL DA PRESTAÇÃO DO SERVIÇO / VALOR A RECEBER)
- [ ] Extract CONTEINER code from OBSERVAÇÕES section (after "CONTAINER:")
- [ ] Extract Data emissão (DATA DE EMISSÃO) from DACTE header
- [ ] Generate Excel (.xlsx) with correct column order: CTE, Tipo, Data emissão, Planta, Valor, Valor serviço, CONTEINER
- [ ] Format financial columns as Brazilian currency (R$) in Excel
- [ ] Convert Brazilian number format (1.262.526,08) to float correctly
- [ ] Handle missing CONTEINER gracefully (N/A or blank)
- [ ] Download generated Excel file from the browser

### Out of Scope

- User authentication / login system — single-purpose tool, no accounts needed
- Database storage of extracted data — ephemeral processing only
- OCR for scanned/image PDFs — only text-based PDFs supported
- Multi-language support — Portuguese-only interface

## Context

- DACTE (Documento Auxiliar do Conhecimento de Transporte Eletrônico) is a standardized Brazilian transport document
- Documents follow a consistent layout with labeled sections: header, remetente, destinatário, valores, observações
- Financial values use Brazilian format: period (.) for thousands separator, comma (,) for decimal
- Container codes are alphanumeric (e.g., GCXU6488847, FFAU7080058)
- Not all shipments have containers — the field may be absent from observações
- Sample PDF (DACTES.pdf) is available in the workspace for testing
- The user provided a screenshot showing the expected Excel output format with dark blue header row

## Constraints

- **Tech Stack**: Python backend (Flask or FastAPI), pdfplumber for PDF parsing, pandas + openpyxl for Excel generation
- **PDF Library**: pdfplumber preferred (better table/text extraction than PyPDF2)
- **Regex**: All field extraction must use regex patterns for reliability
- **Number Format**: Must handle BR→float conversion (1.262.526,08 → 1262526.08)
- **Excel Format**: Financial columns must be recognized as numbers by Excel, not text strings

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| pdfplumber over PyPDF2 | Better text extraction with layout preservation for structured documents | — Pending |
| Flask for web server | Lightweight, sufficient for file upload + download workflow | — Pending |
| Regex-based extraction | DACTE fields follow consistent patterns, regex is reliable and fast | — Pending |
| No database | Single-purpose extraction tool, no need to persist data | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-04 after initialization*
