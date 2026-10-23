# LATER-STEP
# Archive image analysis artifacts and derived captions in managed object storage
import json
from vision_models import save_to_storage


def archive_analysis_artifacts(
    image_id: str,
    labels_path: str,
    description_path: str,
    texts_path: str,
    safety_path: str,
    caption_path: str,
):
    """Persist analysis files to remote storage.

    Args:
        image_id: Identifier used for naming objects.
        labels_path: Local path of label detection result.
        description_path: Local path of image description.
        texts_path: Local path of extracted text.
        safety_path: Local path of safety moderation result.
        caption_path: Local path of final caption.
    """
    # Example: upload each file to a bucket with a prefix based on image_id
    save_to_storage(labels_path, f"archive/{image_id}/labels.json")
    save_to_storage(description_path, f"archive/{image_id}/description.txt")
    save_to_storage(texts_path, f"archive/{image_id}/texts.json")
    save_to_storage(safety_path, f"archive/{image_id}/safety.json")
    save_to_storage(caption_path, f"archive/{image_id}/caption.txt")
