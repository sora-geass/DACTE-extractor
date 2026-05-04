# Pitfalls Research: DACTE PDF Extractor

## Critical Pitfalls

### 1. Brazilian Number Format Conversion
**Risk:** HIGH
**What goes wrong:** Values like `1.262.526,08` get parsed incorrectly if treated as US format
**Prevention:** Always strip dots first, then replace comma with dot before float conversion
```python
def parse_br_currency(value_str):
    return float(value_str.replace('.', '').replace(',', '.'))
```
**Phase:** Core extraction logic

### 2. PDF Text Ordering
**Risk:** MEDIUM
**What goes wrong:** pdfplumber may return text in unexpected order depending on PDF generator
**Prevention:** Use `extract_text(layout=True)` to preserve spatial layout, or use `page.crop()` for specific regions
**Phase:** PDF parsing

### 3. Regex Fragility Across DACTE Variants
**Risk:** MEDIUM
**What goes wrong:** Different DACTE generators (SEFAZ, third-party) may use slightly different labels
**Prevention:** Use flexible regex patterns (e.g., allow for "CONTAINER" and "CONTÊINER", "CT-e" and "CTE")
**Phase:** Extraction rules

### 4. Excel Number vs Text
**Risk:** HIGH
**What goes wrong:** If values are written as strings to Excel, they display as text (green triangle warning)
**Prevention:** Write float values to cells, then apply `number_format = 'R$ #,##0.00'`
**Phase:** Excel generation

### 5. Multi-page DACTEs
**Risk:** LOW
**What goes wrong:** Some DACTEs span multiple pages; observações may be on page 2
**Prevention:** Concatenate text from all pages before regex extraction
**Phase:** PDF parsing

### 6. File Upload Security
**Risk:** MEDIUM
**What goes wrong:** Unrestricted file uploads can be exploited
**Prevention:** Validate file extension (.pdf only), use `secure_filename`, limit file size
**Phase:** Web interface
