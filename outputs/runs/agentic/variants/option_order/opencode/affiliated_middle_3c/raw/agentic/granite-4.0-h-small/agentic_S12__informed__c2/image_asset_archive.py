# [LATER-STEP] image_asset_archive.py

import os
import shutil
from archive_client import ArchiveClient


def archive_analysis_artifacts(
    image_path: str, analysis_results: dict, archive_path: str = "./image_archives"
):
    """Archive image‑analysis artifacts including the original image, extracted data, and captions.

    Creates a timestamped folder inside `archive_path` containing:
      - the source image file
      - a JSON file with normalized analysis data
      - a human‑readable summary report
    """
    # Ensure target archive directory exists
    os.makedirs(archive_path, exist_ok=True)
    timestamp = os.getenv("ARCHIVE_TIMESTAMP", time.strftime("%Y%m%d_%H%M%S"))
    archive_dir = os.path.join(archive_path, timestamp)
    os.makedirs(archive_dir, exist_ok=True)

    # 1. Copy the original image
    shutil.copy2(image_path, os.path.join(archive_dir, os.path.basename(image_path)))

    # 2. Write normalized JSON (using vision_models normalization)
    norm = normalize_vision_response(analysis_results)
    with open(os.path.join(archive_dir, "analysis.json"), "w", encoding="utf-8") as f:
        import json

        json.dump(
            {
                "labels": [lbl.description for lbl in norm.labels],
                "captions": [c.text for c in norm.captions],
                "texts": [t.description for t in norm.texts],
                "unsafe": [
                    {"category": u.category, "score": u.score} for u in norm.unsafe
                ],
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    # 3. Write human‑readable summary (reuse image_summary)
    summary = summarize_analysis(image_path, analysis_results)
    with open(os.path.join(archive_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"Archived analysis to {archive_dir}")


# Helper import placeholder – the actual implementation lives in `archive_client.py`
# from archive_client import ArchiveClient
