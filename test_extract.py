import pdfplumber
import re

pdf = pdfplumber.open('DACTES.pdf')
for i, page in enumerate(pdf.pages):
    text = page.extract_text()
    
    # CTE
    m = re.search(r'N\.(\d{9,})', text)
    cte = m.group(1) if m else '?'
    
    # Data emissao
    m = re.search(r'DATA DE EMISS.O.*?(\d{2}/\d{2}/\d{4})', text, re.DOTALL)
    data = m.group(1) if m else '?'
    
    # Municipio destinatario
    m = re.search(r'DESTINAT.RIO.*?MUNIC.PIO\s+([\w\s/]+?)\s+CEP', text, re.DOTALL)
    mun = m.group(1).strip() if m else '?'
    
    # Valor total mercadoria
    m = re.search(r'VALOR TOTAL DA MERCADORIA\s*([\d.,]+)', text)
    valor = m.group(1) if m else '?'
    
    # Valor a receber
    m = re.search(r'VALOR A RECEBER\s*([\d.,]+)', text)
    vserv = m.group(1) if m else '?'
    
    # Container
    m = re.search(r'CONTEINER?:\s*([A-Z]{4}\d{6,7})', text)
    cont = m.group(1) if m else 'N/A'
    
    print(f'Page {i+1}: CTE={cte}, Data={data}, Mun={mun}, Valor={valor}, VServ={vserv}, Cont={cont}')

pdf.close()
