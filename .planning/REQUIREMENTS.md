# Requirements: DACTE PDF Extractor

**Defined:** 2026-05-04
**Core Value:** Users can upload DACTE PDFs and instantly receive a formatted Excel spreadsheet with all extracted transport data

## v1 Requirements

### Upload

- [ ] **UPLD-01**: User can upload a single PDF file via the web interface
- [ ] **UPLD-02**: User can upload multiple PDF files in a single batch
- [ ] **UPLD-03**: System validates that uploaded files are PDF format
- [ ] **UPLD-04**: System rejects non-PDF files with a clear error message

### Extraction

- [ ] **EXTR-01**: System extracts CTE number from header (CT-e N. / NÚMERO), stripping leading zeros
- [ ] **EXTR-02**: System extracts Planta (MUNICÍPIO) from DESTINATÁRIO block
- [ ] **EXTR-03**: System extracts Valor (VALOR TOTAL DA MERCADORIA) as a numeric float
- [ ] **EXTR-04**: System extracts Valor serviço (VALOR TOTAL DA PRESTAÇÃO DO SERVIÇO / VALOR A RECEBER) as a numeric float
- [ ] **EXTR-05**: System extracts CONTEINER code from OBSERVAÇÕES section (after "CONTAINER:")
- [ ] **EXTR-06**: System extracts Data emissão (DATA DE EMISSÃO) from DACTE header
- [ ] **EXTR-07**: System converts Brazilian number format (1.262.526,08) to float correctly
- [ ] **EXTR-08**: System handles missing CONTEINER gracefully (fills with "N/A" or blank)

### Export

- [ ] **EXPO-01**: System generates Excel (.xlsx) with correct column order: CTE, Tipo, Data emissão, Planta, Valor, Valor serviço, CONTEINER
- [ ] **EXPO-02**: Financial columns (Valor, Valor serviço) are formatted as Brazilian currency (R$) in Excel
- [ ] **EXPO-03**: Financial values are stored as numbers in Excel (not text strings)
- [ ] **EXPO-04**: User can download the generated Excel file from the browser
- [ ] **EXPO-05**: Tipo column is present but left empty (generic field)

### Interface

- [ ] **UI-01**: Web interface has a polished, modern design with drag-and-drop upload area
- [ ] **UI-02**: User sees processing status/feedback while PDFs are being parsed
- [ ] **UI-03**: User sees extracted data summary before downloading Excel

## v2 Requirements

### Advanced Features

- **ADV-01**: User can preview extracted data in a table before export
- **ADV-02**: User can edit extracted values before generating Excel
- **ADV-03**: System supports OCR for scanned/image-based DACTEs
- **ADV-04**: User can configure column mapping

## Out of Scope

| Feature | Reason |
|---------|--------|
| User authentication | Single-purpose tool, no accounts needed |
| Database storage | Ephemeral processing only |
| OCR for scanned PDFs | Only text-based PDFs in v1 |
| Multi-language UI | Portuguese-only interface |
| API endpoints | Web-only interface in v1 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| UPLD-01 | Phase 1 | Pending |
| UPLD-02 | Phase 1 | Pending |
| UPLD-03 | Phase 1 | Pending |
| UPLD-04 | Phase 1 | Pending |
| EXTR-01 | Phase 2 | Pending |
| EXTR-02 | Phase 2 | Pending |
| EXTR-03 | Phase 2 | Pending |
| EXTR-04 | Phase 2 | Pending |
| EXTR-05 | Phase 2 | Pending |
| EXTR-06 | Phase 2 | Pending |
| EXTR-07 | Phase 2 | Pending |
| EXTR-08 | Phase 2 | Pending |
| EXPO-01 | Phase 3 | Pending |
| EXPO-02 | Phase 3 | Pending |
| EXPO-03 | Phase 3 | Pending |
| EXPO-04 | Phase 3 | Pending |
| EXPO-05 | Phase 3 | Pending |
| UI-01 | Phase 4 | Pending |
| UI-02 | Phase 4 | Pending |
| UI-03 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0 ✓

---
*Requirements defined: 2026-05-04*
*Last updated: 2026-05-04 after initial definition*
