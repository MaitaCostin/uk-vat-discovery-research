from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_ROOT / "data" / "raw" / "051168-2026_release.json"
def parse_args() -> argparse.Namespace:
    """Read command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Inspect unique awarded suppliers in a Find a Tender "
            "OCDS release package."
        )
    )

    parser.add_argument(
        "input_file",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT,
        help=(
            "Path to the OCDS release JSON file. "
            "Defaults to the Formation Design & Build test release."
        ),
    )

    return parser.parse_args()


def load_json(file_path: Path) -> dict[str, Any]:
    """Load and return a JSON document from disk."""
    if not file_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {file_path}")

    with file_path.open("r", encoding="utf-8-sig") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Expected the top-level JSON value to be an object.")

    return data


def build_party_lookup(release: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Create a lookup from OCDS party ID to its complete party object."""
    parties = release.get("parties", [])

    return {
        party["id"]: party
        for party in parties
        if isinstance(party, dict) and party.get("id")
    }


def get_awarded_supplier_ids(release: dict[str, Any]) -> list[str]:
    """Return unique supplier IDs referenced by OCDS awards."""
    supplier_ids: list[str] = []
    seen: set[str] = set()

    for award in release.get("awards", []):
        if not isinstance(award, dict):
            continue

        for supplier in award.get("suppliers", []):
            if not isinstance(supplier, dict):
                continue

            supplier_id = supplier.get("id")

            if supplier_id and supplier_id not in seen:
                seen.add(supplier_id)
                supplier_ids.append(supplier_id)

    return supplier_ids


def extract_identifier(
    party: dict[str, Any],
    expected_scheme: str,
) -> str | None:
    """Extract an organisation identifier for a requested scheme."""
    identifiers: list[dict[str, Any]] = []

    primary_identifier = party.get("identifier")
    if isinstance(primary_identifier, dict):
        identifiers.append(primary_identifier)

    additional_identifiers = party.get("additionalIdentifiers", [])
    if isinstance(additional_identifiers, list):
        identifiers.extend(
            identifier
            for identifier in additional_identifiers
            if isinstance(identifier, dict)
        )

    for identifier in identifiers:
        if identifier.get("scheme") == expected_scheme:
            value = identifier.get("id")
            return str(value) if value is not None else None

    return None


def format_address(party: dict[str, Any]) -> str:
    """Format the organisation address from the available OCDS fields."""
    address = party.get("address")

    if not isinstance(address, dict):
        return ""

    components = [
        address.get("streetAddress"),
        address.get("locality"),
        address.get("postalCode"),
        address.get("countryName") or address.get("country"),
    ]

    return "; ".join(str(value) for value in components if value)


def inspect_release_package(package: dict[str, Any]) -> None:
    """Print awarded suppliers from every release in the package."""
    releases = package.get("releases", [])

    if not isinstance(releases, list) or not releases:
        raise ValueError("No releases were found in the OCDS package.")

    for release_number, release in enumerate(releases, start=1):
        if not isinstance(release, dict):
            continue

        print(f"\nRelease {release_number}")
        print(f"OCID: {release.get('ocid', '')}")
        print(f"Release ID: {release.get('id', '')}")

        party_lookup = build_party_lookup(release)
        supplier_ids = get_awarded_supplier_ids(release)

        print(f"Awarded supplier count: {len(supplier_ids)}")

        for supplier_id in supplier_ids:
            party = party_lookup.get(supplier_id, {})

            name = party.get("name", "")
            ppon = extract_identifier(party, "GB-PPON")
            companies_house_number = extract_identifier(party, "GB-COH")
            address = format_address(party)

            contact_point = party.get("contactPoint", {})
            website = (
                contact_point.get("url", "")
                if isinstance(contact_point, dict)
                else ""
            )

            print("\nAwarded supplier")
            print(f"  Name: {name}")
            print(f"  Party ID: {supplier_id}")
            print(f"  PPON: {ppon or 'missing'}")
            print(
                "  Companies House number: "
                f"{companies_house_number or 'missing'}"
            )
            print(f"  Address: {address or 'missing'}")
            print(f"  Website: {website or 'missing'}")


def main() -> None:

    args = parse_args()
    input_file: Path = args.input_file

    if not input_file.is_absolute():
        input_file = (PROJECT_ROOT / input_file).resolve()

    print(f"Input file: {input_file}")

    package = load_json(input_file)
    inspect_release_package(package)


if __name__ == "__main__":
    main()