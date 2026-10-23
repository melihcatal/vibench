import json
import os
from typing import List, Dict

# ----------------------------------------------------------------------
# image_asset_archive.py – Archive analysis artifacts and derived captions
# ----------------------------------------------------------------------

# Placeholder for object‑storage SDK; example uses Alibaba Cloud OSS.
try:
    from oss2 import Bucket, Auth
except Exception:
    # If SDK is missing, define empty stubs so the file is importable.
    class Bucket:
        pass

    class Auth:
        def __init__(self, *args, **kwargs):
            pass


ARCHIVE_BUCKET = os.getenv("ARCHIVE_OSS_BUCKET")
ARCHIVE_ENDPOINT = os.getenv("ARCHIVE_OSS_ENDPOINT")
ARCHIVE_ACCESS_KEY_ID = os.getenv("ARCHIVE_OSS_ACCESS_KEY_ID")
ARCHIVE_ACCESS_KEY_SECRET = os.getenv("ARCHIVE_OSS_ACCESS_KEY_SECRET")


def archive_analysis(analysis_id: str, artifacts: List[Dict[str, Any]]) -> None:
    """Upload analysis artifacts to managed object storage (Alibaba OSS).

    Args:
        analysis_id: Unique identifier for this run (e.g., UUID).
        artifacts: List of dicts, each containing at least 'filename' and 'content'.
    """
    auth = Auth(ARCHIVE_ACCESS_KEY_ID, ARCHIVE_ACCESS_KEY_SECRET)
    bucket = Bucket(auth, ARCHIVE_ENDPOINT, ARCHIVE_BUCKET)
    for art in artifacts:
        filename = os.path.basename(art["filename"])
        bucket.put_object(filename, art["content"])
    # Store a manifest JSON listing all uploaded files
    manifest = {
        "analysis_id": analysis_id,
        "files": [os.path.basename(a["filename"]) for a in artifacts],
    }
    bucket.put_object(f"{analysis_id}/manifest.json", json.dumps(manifest))


if __name__ == "__main__":
    # Demo: archive a couple of generated files
    demo_artifacts = [
        {"filename": "label_report.txt", "content": b"Label detection result."},
        {"filename": "caption.txt", "content": b"A sunny day."},
    ]
    archive_analysis("run-12345", demo_artifacts)
    print("Archiving completed.")
