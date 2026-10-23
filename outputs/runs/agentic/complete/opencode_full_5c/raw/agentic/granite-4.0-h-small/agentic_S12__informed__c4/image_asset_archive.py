import json
import os
from google.cloud import storage
from typing import List, Dict


def archive_image_analysis(
    image_path: str, analysis_summary: Dict, bucket_name: str = "vision-analysis-assets"
) -> List[str]:
    """Archive image file and its analysis artifacts in Google Cloud Storage.

    Args:
        image_path: Local path to the source image.
        analysis_summary: Dict produced by summarize_visual_analysis (see image_summary.py).
        bucket_name: GCS bucket where objects will be stored.

    Returns:
        List of full GCS object paths that were written.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # Derive a base name from the image file (without directory)
    filename = os.path.basename(image_path)
    # Object name for the original image
    image_blob = bucket.blob(f"images/{filename}")
    image_blob.upload_from_filename(image_path)

    # Object for the summary JSON
    summary_blob = bucket.blob(f"summaries/{filename}.json")
    summary_blob.upload_from_string(json.dumps(analysis_summary, indent=2))

    # Optionally archive extracted texts as separate file
    texts_key = f"texts/{filename}_extracted.txt"
    texts_blob = bucket.blob(texts_key)
    texts_blob.upload_from_string(
        "\n".join(analysis_summary.get("extracted_texts", []))
    )

    return [
        str(image_blob.public_url),
        str(summary_blob.public_url),
        str(texts_blob.public_url),
    ]
