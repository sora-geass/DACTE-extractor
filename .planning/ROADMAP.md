# Roadmap: DACTE PDF Extractor

**Created:** 2026-05-04
**Milestone:** v1.0 — MVP
**Phases:** 4
**Granularity:** Coarse

## Overview

| # | Phase | Goal | Requirements | Plans |
|---|-------|------|--------------|-------|
| 1 | Backend Setup & Upload | Flask server with PDF upload endpoint | UPLD-01..04 | 1-2 |
| 2 | PDF Extraction Engine | pdfplumber + regex extraction for all DACTE fields | EXTR-01..08 | 1-3 |
| 3 | Excel Export & Download | pandas + openpyxl output with currency formatting | EXPO-01..05 | 1-2 |
| 4 | Frontend Polish & Integration | Modern UI with drag-drop, status feedback, data preview | UI-01..03 | 1-2 |

## Phase Details

### Phase 1: Backend Setup & Upload
**Goal:** Flask web server accepting PDF file uploads with validation
**Requirements:** UPLD-01, UPLD-02, UPLD-03, UPLD-04
**UI hint**: no

**Success Criteria:**
1. Flask app starts and serves upload endpoint
2. Single PDF upload accepted and stored temporarily
3. Multiple PDF batch upload works
4. Non-PDF files rejected with error response
5. File size limits enforced

**Depends on:** Nothing

---

### Phase 2: PDF Extraction Engine
**Goal:** Extract all required fields from DACTE PDFs using pdfplumber and regex
**Requirements:** EXTR-01, EXTR-02, EXTR-03, EXTR-04, EXTR-05, EXTR-06, EXTR-07, EXTR-08
**UI hint**: no

**Success Criteria:**
1. CTE number extracted correctly from header, leading zeros handled
2. Planta (município) extracted from destinatário block
3. Valor total da mercadoria extracted and converted to float
4. Valor serviço extracted and converted to float
5. Container code extracted from observações or marked N/A
6. Data emissão extracted from header
7. Brazilian number format converted correctly (1.262.526,08 → 1262526.08)
8. Tested against provided DACTES.pdf sample

**Depends on:** Phase 1

---

### Phase 3: Excel Export & Download
**Goal:** Generate formatted Excel spreadsheet and serve as download
**Requirements:** EXPO-01, EXPO-02, EXPO-03, EXPO-04, EXPO-05
**UI hint**: no

**Success Criteria:**
1. Excel file generated with correct column order (CTE, Tipo, Data emissão, Planta, Valor, Valor serviço, CONTEINER)
2. Financial columns formatted as R$ currency in Excel
3. Values stored as numbers (Excel recognizes them, not text)
4. Tipo column present but empty
5. File downloads successfully via browser
6. Output matches the format shown in user's screenshot reference

**Depends on:** Phase 2

---

### Phase 4: Frontend Polish & Integration
**Goal:** Modern, polished web interface with drag-drop upload and processing feedback
**Requirements:** UI-01, UI-02, UI-03
**UI hint**: yes

**Success Criteria:**
1. Drag-and-drop upload area with visual feedback
2. Processing indicator shows while PDFs are being parsed
3. Extracted data summary visible before download
4. Design is premium (dark theme, gradients, smooth animations)
5. End-to-end flow works: upload → extract → preview → download

**Depends on:** Phase 3

---

## Milestone Boundary

**v1.0 complete when:**
- All 4 phases pass success criteria
- End-to-end test with DACTES.pdf produces correct Excel output
- UI is polished and production-ready
