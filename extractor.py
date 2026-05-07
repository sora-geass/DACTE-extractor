"""
DACTE PDF Data Extractor Module
Extracts structured data from DACTE (Documento Auxiliar do Conhecimento de Transporte Eletrônico) PDFs
using pdfplumber for text extraction and regex for field parsing.
"""

import re
import pdfplumber


def parse_br_currency(value_str: str) -> float:
    """
    Convert Brazilian currency format to float.
    Examples:
        "1.262.526,08" -> 1262526.08
        "224.901,98" -> 224901.98
        "2.560,88" -> 2560.88
        "97,00" -> 97.0
    """
    if not value_str:
        return 0.0
    # Remove dots (thousands separator), replace comma with dot (decimal)
    cleaned = value_str.strip().replace('.', '').replace(',', '.')
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def classify_tipo(origem: str, destino: str) -> str:
    """
    Classify the transport type based on origin and destination cities.
    
    Business rules:
        - Plant (Indaiatuba/Sorocaba/Porto Feliz) → Sumaré = "Transferência"
        - Port (Guarujá/Santos) → Sumaré = "Importação/{port}"
        - Sumaré → Plant = "Entrega"
        - Sumaré → Port (Guarujá/Santos) = "Exportação/{port}"
    """
    # Normalize to uppercase, strip, and remove basic accents
    def normalize(text):
        t = text.upper().strip()
        replacements = {'Á': 'A', 'À': 'A', 'Â': 'A', 'Ã': 'A', 'É': 'E', 'Ê': 'E', 'Í': 'I', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ú': 'U', 'Ç': 'C'}
        for search, replace in replacements.items():
            t = t.replace(search, replace)
        return t
        
    orig = normalize(origem)
    dest = normalize(destino)
    
    plants = {'INDAIATUBA', 'SOROCABA', 'PORTO FELIZ'}
    ports = {'GUARUJA', 'SANTOS'}
    company = 'SUMARE'
    
    if orig in plants and dest == company:
        return 'Transferência'
    elif orig in ports and dest == company:
        return f'Importação/{origem.title()}'
    elif orig == company and dest in plants:
        return 'Entrega'
    elif orig == company and dest in ports:
        return f'Exportação/{destino.title()}'
    else:
        # Fallback: show origin → destination
        return f'{origem.title()} → {destino.title()}'


def extract_dacte_data(page_text: str) -> dict:
    """
    Extract all required fields from a single DACTE page text.
    
    Returns dict with keys:
        cte, tipo, data_emissao, planta, valor, valor_servico, conteiner
    """
    result = {
        'cte': '',
        'tipo': '',
        'data_emissao': '',
        'planta': '',
        'valor': 0.0,
        'valor_servico': 0.0,
        'conteiner': 'N/A',
        'op_emissor': '',
        'observacao': '',
        'placa': '',
        'cte_substituto': '',
        'empresa': ''
    }
    
    # 1. CTE Number - from header "N.000059966" pattern
    m = re.search(r'N\.(\d{6,})', page_text)
    if m:
        # Convert to int to strip leading zeros, then back to string
        result['cte'] = str(int(m.group(1)))
    else:
        # Fallback: try NÚMERO field
        m = re.search(r'N[ÚU]MERO\s+(\d{6,})', page_text, re.IGNORECASE)
        if m:
            result['cte'] = str(int(m.group(1)))
    
    # 1.5. Tipo - from ORIGEM DA PRESTAÇÃO and DESTINO DA PRESTAÇÃO
    # PDF text pattern: "ORIGEM DA PRESTAÇÃO DESTINO DA PRESTAÇÃO\nCITY1/UF CITY2/UF"
    m = re.search(
        r'ORIGEM DA PRESTA.{1,5}O\s+DESTINO DA PRESTA.{1,5}O\s*\n\s*(\S+)/\S+\s+(\S+)/\S+',
        page_text
    )
    if m:
        origem_city = m.group(1).strip()
        destino_city = m.group(2).strip()
        result['tipo'] = classify_tipo(origem_city, destino_city)
    
    # 2. Data de Emissão
    m = re.search(r'DATA DE EMISS.O.*?(\d{2}/\d{2}/\d{4})', page_text, re.DOTALL)
    if m:
        result['data_emissao'] = m.group(1)
    
    # 3. Planta (Município do Destinatário)
    # The Destinatário is the Toyota plant. Due to horizontal text extraction, 
    # Remetente and Destinatário fields are on the same line.
    m = re.search(r'MUNIC.PIO.*?(?:CEP|CNPJ).*?MUNIC.PIO\s+([\w\s/À-Ú]+?)\s+CEP', page_text)
    if m:
        planta_raw = m.group(1).strip()
    else:
        # Fallback: search explicitly for known plant names near DESTINATÁRIO
        m2 = re.search(r'DESTINAT.RIO.*?(INDAIATUBA|SOROCABA|PORTO\s*FELIZ)', page_text, re.DOTALL | re.IGNORECASE)
        if m2:
            planta_raw = m2.group(1).strip()
        else:
            m3 = re.search(r'DESTINAT.RIO.*?MUNIC.PIO\s+([\w\s/À-Ú]+?)\s+CEP', page_text, re.DOTALL)
            planta_raw = m3.group(1).strip() if m3 else ""

    if planta_raw:
        # Remove state abbreviation (e.g. "/ SP") and apply title case
        planta_raw = re.sub(r'\s*/\s*[A-Z]{2}\s*$', '', planta_raw).strip()
        # Normalize Porto Feliz spacing if needed
        planta_raw = re.sub(r'(?i)PORTO\s*FELIZ', 'Porto Feliz', planta_raw)
        result['planta'] = planta_raw.title()
    
    # 4. Valor Total da Mercadoria
    # The value appears on the next line after "VALOR TOTAL DA MERCADORIA"
    m = re.search(
        r'VALOR TOTAL DA MERCADORIA\n.*?([\d]+(?:\.[\d]{3})*,[\d]{2})',
        page_text
    )
    if m:
        result['valor'] = parse_br_currency(m.group(1))
    
    # 5. Valor do Serviço (VALOR A RECEBER)
    m = re.search(r'VALOR A RECEBER\s*\n?\s*([\d]+(?:\.[\d]{3})*,[\d]{2})', page_text)
    if m:
        result['valor_servico'] = parse_br_currency(m.group(1))
    else:
        # Fallback: VALOR TOTAL DA PRESTAÇÃO
        m = re.search(
            r'VALOR TOTAL (?:DA )?PRESTA.{1,5}O.*?([\d]+(?:\.[\d]{3})*,[\d]{2})',
            page_text, re.DOTALL
        )
        if m:
            result['valor_servico'] = parse_br_currency(m.group(1))
    
    # 6. Container (from OBSERVAÇÕES section)
    m = re.search(r'CONTEINER?:\s*([A-Z]{4}\d{6,7})', page_text, re.IGNORECASE)
    if not m:
        m = re.search(r'CONTAINER?:\s*([A-Z]{4}\d{6,7})', page_text, re.IGNORECASE)
    if m:
        result['conteiner'] = m.group(1)
    else:
        result['conteiner'] = 'N/A'
    
    # 7. Veículo/Placa verification
    target_plates = ['TKD4H07', 'TJY0D20', 'TJY7J95', 'TIP3G54', 'TLK6C49']
    for plate in target_plates:
        if plate in page_text:
            result['op_emissor'] = ''
            result['observacao'] = 'SCANIA'
            result['placa'] = plate
            result['cte_substituto'] = ''
            result['empresa'] = 'TOYOTA'
            break
            
    return result


def extract_from_pdf(pdf_path: str) -> list:
    """
    Extract DACTE data from a PDF file.
    Each page is treated as a separate DACTE document.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of dicts, one per DACTE (page) found
    """
    results = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            
            # Check if this page contains DACTE content
            if 'DACTE' in text or 'CT-e' in text or 'CONHECIMENTO' in text:
                data = extract_dacte_data(text)
                if data['cte']:  # Only add if we found a CTE number
                    results.append(data)
    
    return results


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <pdf_file>")
        sys.exit(1)
    
    results = extract_from_pdf(sys.argv[1])
    for r in results:
        print(f"CTE: {r['cte']}, Planta: {r['planta']}, Valor: {r['valor']}, "
              f"Serviço: {r['valor_servico']}, Container: {r['conteiner']}, "
              f"Data: {r['data_emissao']}")
