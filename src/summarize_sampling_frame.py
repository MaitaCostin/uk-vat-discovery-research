import csv
from pathlib import Path


root = Path(__file__).resolve().parent.parent

input_file = root / "data" / "processed" / "july_awarded_suppliers.csv"
output_file = root / "data" / "processed" / "july_unique_company_candidates.csv"


with input_file.open(encoding="utf-8-sig") as file:
    suppliers = list(csv.DictReader(file))


missing = []
companies = {}

for supplier in suppliers:
    company_number = supplier["companies_house_number_raw"].strip().upper()

    if not company_number:
        missing.append(supplier)
        continue

    if company_number not in companies:
        companies[company_number] = {
            "companies_house_number": company_number,
            "supplier_name": supplier["supplier_name"],
            "ppon": supplier["ppon"],
            "website": supplier["website"],
            "source_notice_ids": [],
            "appearance_count": 0,
        }

    companies[company_number]["appearance_count"] += 1

    notice_id = supplier["notice_id"]

    if notice_id not in companies[company_number]["source_notice_ids"]:
        companies[company_number]["source_notice_ids"].append(notice_id)


rows = []

for company in companies.values():
    number = company["companies_house_number"]

    rows.append(
        {
            "companies_house_number": number,
            "format_status": (
                "plausible"
                if len(number) == 8 and number.isalnum()
                else "needs_review"
            ),
            "supplier_name": company["supplier_name"],
            "ppon": company["ppon"],
            "website": company["website"],
            "appearance_count": company["appearance_count"],
            "source_notice_ids": " | ".join(
                company["source_notice_ids"]
            ),
        }
    )


columns = [
    "companies_house_number",
    "format_status",
    "supplier_name",
    "ppon",
    "website",
    "appearance_count",
    "source_notice_ids",
]

with output_file.open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)


plausible = [
    row for row in rows
    if row["format_status"] == "plausible"
]

needs_review = [
    row for row in rows
    if row["format_status"] == "needs_review"
]


print(f"Awarded supplier rows: {len(suppliers)}")
print(f"Rows missing company number: {len(missing)}")
print(f"Unique company numbers: {len(rows)}")
print(f"Plausible company numbers: {len(plausible)}")
print(f"Company numbers needing review: {len(needs_review)}")
print(f"Output: {output_file}")