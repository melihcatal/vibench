# [LATER-STEP] image_asset_archive.py
# Archive image analysis artifacts and derived captions in managed object storage (IBM Cloud Object Storage as example)
import os
import json
import ibm_boto3
from ibm_botocore.client import Config
from pathlib import Path
from typing import List
from vision_models import VisionResponse

# --------------------------------------------------------- #
# CONFIGURATION (environment variables)                        #
# --------------------------------------------------------- #
IBMCOS_ENDPOINT = os.getenv("IBM_COS_ENDPOINT")
IBMCOS_APIKEY_ID = os.getenv("IBM_COS_APIKEY_ID")
IBMCOS_BUCKET = os.getenv("IBM_COS_BUCKET")
if not (IBMCOS_ENDPOINT and IBMCOS_APIKEY_ID and IBMCOS_BUCKET):
    raise RuntimeError(
        "Set IBM_COS_ENDPOINT, IBM_COS_APIKEY_ID, and IBM_COS_BUCKET environment variables"
    )

# --------------------------------------------------------- #
# CLIENT INITIALISATION                                     #
# --------------------------------------------------------- #
cos = ibm_boto3.client(
    service_name="s3",
    endpoint_url=IBMCOS_ENDPOINT,
    ibm_api_key_id=IBMCOS_APIKEY_ID,
    config=Config(signature_version="oauth"),
)


# --------------------------------------------------------- #
# ARCHIVE FUNCTIONS                                         #
# --------------------------------------------------------- #
def _archive_file(local_path: Path, cos_key: str) -> None:
    """Upload a file to COS bucket using the configured client."""
    with open(local_path, "rb") as f:
        cos.upload_fileobj(f, IBMCOS_BUCKET, cos_key)


def archive_analysis_run(
    run_id: str, imgs: List[str], responses: List[Dict[str, VisionResponse]]
) -> None:
    """Persist a complete analysis run consisting of original images and json results."""
    prefix = f"analysis/{run_id}/"
    # 1️⃣ Save raw images (assumes they are local files)
    for img_path in imgs:
        local = Path(img_path)
        cos_key = f"{prefix}{local.name}"
        _archive_file(local, cos_key)
    # 2️⃣ Save combined textual result (summary + per‑step JSON)
    combined = {
        "run_id": run_id,
        "timestamp": os.getenv("SOURCE_DATE_EPOCH", str(int(os.time()))),
        "sources": [
            {
                "type": src.get("provider"),
                "labels": src["labels"],
                "description": src.get("description"),
                "text": src.get("text"),
                "safety": src.get("safety"),
            }
            for src in responses
        ],
    }
    summary_text = summarize_responses([vars(r) for r in responses])
    combined["summary"] = summary_text
    summary_file = f"{prefix}summary.txt"
    cos.put_object(Bucket=IBMCOS_BUCKET, Key=summary_file, Body=summary_text.encode())
    # 3️⃣ Save a combined JSON artifact for programmatic consumption
    json_file = f"{prefix}results.json"
    cos.put_object(
        Bucket=IBMCOS_BUCKET,
        Key=json_file,
        Body=json.dumps(combined, indent=2).encode(),
    )


# --------------------------------------------------------- #
# DEMO / CLI ENTRY POINT                                    #
# --------------------------------------------------------- #
if __name__ == "__main__":
    import sys, json

    if len(sys.argv) < 3:
        print("Usage: image_asset_archive.py <run_id> <image_path1> [image_path2 ...]")
        sys.exit(1)
    run_id = sys.argv[1]
    img_paths = sys.argv[2:]
    # Example: load a dummy VisionResponse list (in real usage you would pass the objects produced earlier)
    # Here we just create a placeholder demo entry per image
    demo_responses = [
        {
            "provider": "Google Cloud Vision",
            "labels": [f"label_{i}" for i in range(len(img_paths))],
            "description": f"description_{i}",
        }
        for i in range(len(img_paths))
    ]
    archive_analysis_run(run_id, img_paths, demo_responses)
    print(f"Archived analysis for run {run_id} to bucket {IBMCOS_BUCKET}")
