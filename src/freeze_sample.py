import csv
import random
from pathlib import Path


SEED = 20260818

root = Path(__file__).resolve().parent.parent

input_file = (
    root
    / "data"
    / "processed"
    / "july_unique_company_candidates.csv"
)

ranked_output = (
    root
    / "data"
    / "processed"
    / "july_ranked_candidates.csv"
)

sample_output = (
    root
    / "data"
    / "processed"
    / "frozen_sample.csv"
)


with input_file.open(encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    original_columns = reader.fieldnames or []

    candidates = [
        row
        for row in reader
        if row["format_status"] == "plausible"
    ]


# Sort first so the result does not depend on the CSV row order.
candidates.sort(
    key=lambda row: row["companies_house_number"]
)

# Shuffle reproducibly using the fixed seed.
random.Random(SEED).shuffle(candidates)


for rank, company in enumerate(candidates, start=1):
    company["sample_rank"] = str(rank)
    company["random_seed"] = str(SEED)
    company["companies_house_validation_status"] = "not_checked"

    if rank <= 10:
        company["sample_group"] = "development"
    elif rank <= 40:
        company["sample_group"] = "holdout"
    else:
        company["sample_group"] = "reserve"


output_columns = [
    "sample_rank",
    "sample_group",
    "random_seed",
    "companies_house_validation_status",
] + original_columns


with ranked_output.open(
    "w",
    encoding="utf-8",
    newline="",
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=output_columns,
    )
    writer.writeheader()
    writer.writerows(candidates)


with sample_output.open(
    "w",
    encoding="utf-8",
    newline="",
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=output_columns,
    )
    writer.writeheader()
    writer.writerows(candidates[:40])


print(f"Plausible candidates ranked: {len(candidates)}")
print("Development companies: 10")
print("Holdout companies: 30")
print(f"Reserve companies: {len(candidates) - 40}")
print(f"Frozen sample: {sample_output}")