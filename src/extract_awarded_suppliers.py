import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
input_folder = root / "data" / "raw" / "july_notices"
output_file = root / "data" / "processed" / "july_awarded_suppliers.csv"


def find_identifier(party, scheme):
    """Find an identifier such as GB-PPON or GB-COH."""
    identifiers = []

    if isinstance(party.get("identifier"), dict):
        identifiers.append(party["identifier"])

    identifiers.extend(party.get("additionalIdentifiers", []))

    for identifier in identifiers:
        if identifier.get("scheme") == scheme:
            return identifier.get("id", "")

    return ""


rows = []

json_files = sorted(input_folder.glob("*_release.json"))

for json_file in json_files:
    notice_id = json_file.name.replace("_release.json", "")

    package = json.loads(
        json_file.read_text(encoding="utf-8-sig")
    )

    for release in package.get("releases", []):
        # Create a lookup:
        # organisation ID -> complete organisation data
        parties = {
            party["id"]: party
            for party in release.get("parties", [])
            if party.get("id")
        }

        seen_in_notice = set()

        for award in release.get("awards", []):
            for supplier in award.get("suppliers", []):
                supplier_id = supplier.get("id", "")

                if not supplier_id:
                    continue

                if supplier_id in seen_in_notice:
                    continue

                seen_in_notice.add(supplier_id)

                party = parties.get(supplier_id, supplier)
                address = party.get("address", {})
                contact = party.get("contactPoint", {})
                details = party.get("details", {})

                address_text = "; ".join(
                    str(value)
                    for value in [
                        address.get("streetAddress"),
                        address.get("locality"),
                        address.get("postalCode"),
                        address.get("countryName"),
                    ]
                    if value
                )

                rows.append(
                    {
                        "notice_id": notice_id,
                        "ocid": release.get("ocid", ""),
                        "supplier_name": party.get(
                            "name",
                            supplier.get("name", ""),
                        ),
                        "party_id": supplier_id,
                        "ppon": find_identifier(
                            party,
                            "GB-PPON",
                        ),
                        "companies_house_number_raw": find_identifier(
                            party,
                            "GB-COH",
                        ),
                        "supplier_address": address_text,
                        "website": details.get("url", "") or contact.get("url", ""),
                        "source_file": json_file.name,
                    }
                )


columns = [
    "notice_id",
    "ocid",
    "supplier_name",
    "party_id",
    "ppon",
    "companies_house_number_raw",
    "supplier_address",
    "website",
    "source_file",
]

output_file.parent.mkdir(parents=True, exist_ok=True)

with output_file.open("w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)


print(f"JSON files processed: {len(json_files)}")
print(f"Awarded supplier rows written: {len(rows)}")
print(f"Output file: {output_file}")