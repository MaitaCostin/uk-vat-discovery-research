"""Calculate development and holdout VAT discovery metrics."""

import csv
from collections import Counter
from pathlib import Path


root = Path(__file__).resolve().parent.parent
processed = root / "data" / "processed"

files = {
    "development": processed / "development_vat_results.csv",
    "holdout": processed / "holdout_vat_results.csv",
}


def load_results(path, expected_ranks):
    """Load a result file and check ranks and duplicates."""
    with path.open(encoding="utf-8-sig") as file:
        rows = list(csv.DictReader(file))

    ranks = [int(row["sample_rank"]) for row in rows]

    if len(ranks) != len(set(ranks)):
        raise ValueError(f"Duplicate sample ranks in {path.name}")

    if set(ranks) != set(expected_ranks):
        raise ValueError(f"Missing or unexpected ranks in {path.name}")

    return rows


def summarize(rows):
    """Calculate the main VAT discovery metrics."""
    decisions = Counter(row["decision"] for row in rows)

    candidates = [
        row for row in rows
        if row["vat_number"].strip()
    ]

    checked_candidates = [
        row for row in candidates
        if row["hmrc_status"] in {"valid", "invalid"}
    ]

    false_candidates = (
        decisions["valid_wrong_entity"]
        + decisions["candidate_hmrc_invalid"]
    )

    candidate_fp_rate = (
        false_candidates / len(candidates)
        if candidates
        else 0
    )

    verified_yield = decisions["accept"] / len(rows)

    return {
        "companies": len(rows),
        "confirmed_domains": sum(
            row["domain_status"] == "confirmed"
            for row in rows
        ),
        "vat_candidates": len(candidates),
        "hmrc_checked_candidates": len(checked_candidates),
        "accepted_relationships": decisions["accept"],
        "valid_wrong_entity": decisions["valid_wrong_entity"],
        "candidate_hmrc_invalid": decisions["candidate_hmrc_invalid"],
        "no_candidate_found": decisions["no_candidate_found"],
        "no_confirmed_domain": decisions["no_confirmed_domain"],
        "domain_unreachable": decisions["domain_unreachable"],
        "candidate_false_positive_rate": candidate_fp_rate,
        "verified_yield": verified_yield,
    }


development = load_results(
    files["development"],
    range(1, 11),
)

holdout = load_results(
    files["holdout"],
    range(11, 41),
)

datasets = {
    "development": development,
    "holdout": holdout,
    "combined": development + holdout,
}

output_rows = []

for dataset_name, rows in datasets.items():
    metrics = summarize(rows)

    print(f"\n{dataset_name.upper()}")

    for metric, value in metrics.items():
        if metric.endswith("_rate") or metric == "verified_yield":
            print(f"{metric}: {value:.1%}")
        else:
            print(f"{metric}: {value}")

        output_rows.append(
            {
                "dataset": dataset_name,
                "metric": metric,
                "value": (
                    f"{value:.4f}"
                    if isinstance(value, float)
                    else value
                ),
            }
        )


output_file = processed / "metrics_summary.csv"

with output_file.open(
    "w",
    encoding="utf-8",
    newline="",
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["dataset", "metric", "value"],
    )
    writer.writeheader()
    writer.writerows(output_rows)


print(f"\nMetrics saved to: {output_file}")