from extractor import extract_from_pdf
data = extract_from_pdf('DACTES.pdf')
for d in data:
    print(f"CTE {d['cte']}: Tipo={d['tipo']}")
