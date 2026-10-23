import os
from vision_client import VisionClient
from vision_models import VisionModels
import json
from google.cloud import storage


def summarize_visual_analysis(image_path: str, analysis_results: dict) -> str:
    """Create a short summary of combined visual analysis outputs.

    Args:
        image_path: Original image file path.
        analysis_results: Dict where keys are step names and values are step responses.

    Returns:
        Human-friendly summary string.
    """
    summary_lines = [f"Analysis summary for image: {image_path}"]
    for step, result in analysis_results.items():
        model = VisionModels.get_model_name(step)
        if step == "detect_image_labels":
            labels = result.get("labels", [])
            summary_lines.append(
                f"  ✓ Labels (model: {model}): {', '.join([lbl['description'] for lbl in labels])}"
            )
        elif step == "describe_image":
            summary_lines.append(
                f"  ✓ Description (model: {model}): {result.get('text', '').strip()[:120]}..."
            )
        elif step == "detect_image_text":
            summary_lines.append(
                f"  ✓ Extracted text (model: {model}): {', '.join(result.get('text_lines', []))}"
            )
        elif step == "score_image_safety":
            summary_lines.append(
                f"  ✓ Safety (model: {model}): {'SAFE' if all(v == 'SAFE' for v in result.values()) else 'UNSAFE'}"
            )
    return "\n".join(summary_lines)


def upload_summary_to_storage(image_path: str, summary_text: str):
    """Upload the textual summary to managed object storage (Google Cloud Storage)."""
    bucket_name = os.getenv("IMAGE_SUMMARY_BUCKET", "my-bucket")  # placeholder env var
    summary_key = f"summaries/{os.path.basename(image_path)}.txt"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(summary_key)
    blob.upload_from_string(summary_text, content_type="text/plain")
    return f"gs://{bucket_name}/{summary_key}"
