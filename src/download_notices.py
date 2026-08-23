import json
from pathlib import Path
from urllib.request import urlopen

root = Path(__file__).resolve().parent.parent
ids_file = root / "data" / "raw" / "july_notice_ids.txt"
output_folder = root / "data" / "raw" / "july_notices"

notice_ids = [
    line.strip()
    for line in ids_file.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

output_folder.mkdir(parents=True, exist_ok=True)

for position, notice_id in enumerate(notice_ids, start=1):
    output_file = output_folder / f"{notice_id}_release.json"
    url = (
        "https://www.find-tender.service.gov.uk/"
        f"api/1.0/ocdsReleasePackages/{notice_id}"
    )

    if output_file.exists():
        print(f"[{position}/{len(notice_ids)}] {notice_id}: already exists")
        continue

    try:
        data = urlopen(url, timeout=60).read()
        json.loads(data)
        output_file.write_bytes(data)

        print(f"[{position}/{len(notice_ids)}] {notice_id}: downloaded")

    except Exception as error:
        print(f"[{position}/{len(notice_ids)}] {notice_id}: FAILED - {error}")