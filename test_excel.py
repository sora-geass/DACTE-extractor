"""
Test script: Generate Excel from DACTES.pdf to verify end-to-end extraction
"""
import sys
sys.path.insert(0, '.')

from extractor import extract_from_pdf
from app import generate_excel

# Extract data from the sample PDF
data = extract_from_pdf('DACTES.pdf')

print(f"Extracted {len(data)} DACTEs:")
print("-" * 90)
print(f"{'CTE':>8} | {'Planta':<20} | {'Valor':>15} | {'Serviço':>12} | {'Container':<12} | {'Data':<12}")
print("-" * 90)

for row in data:
    print(f"{row['cte']:>8} | {row['planta']:<20} | {row['valor']:>15,.2f} | {row['valor_servico']:>12,.2f} | {row['conteiner']:<12} | {row['data_emissao']:<12}")

print("-" * 90)

# Generate Excel
excel = generate_excel(data)

# Save the file
output_path = 'DACTE_Extraidos_Teste.xlsx'
with open(output_path, 'wb') as f:
    f.write(excel.read())

print(f"\nExcel saved to: {output_path}")
print("Open it to verify formatting (R$ currency, dark blue headers, autofilter)")
