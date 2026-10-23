# [LATER-STEP] secret_label_safety.py
# Check secret labels and notes for unsafe text using Alibaba Cloud Content Moderation SDK

import os
import alibabacloud_contentmoderation20200514 as contentmoderation
from alibabacloud_tea_openapi20200326 import models as open_api_models
from alibabacloud_tea_util20200304 import models as util_models
from fetch_api_key import fetch_api_key
from fetch_db_secret import fetch_db_secret


def check_secret_labels_for_unsafe_text(secret: dict) -> bool:
    """Inspect 'labels' and 'notes' fields for unsafe language."""
    # Example secret payload with labels/notes (could come from fetch_db_secret)
    labels = secret.get("labels", [])
    notes = secret.get("notes", "")
    # Initialize Alibaba Content Moderation client (uses credentials from env)
    client = contentmoderation.Client(
        open_api_models.Config(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
            endpoint="cn-shanghai.aliyuncs.com",
        )
    )
    # Simple rule: any label containing 'test' or note containing 'password' flags unsafe
    unsafe = (
        any("test" in label.lower() for label in labels) or "password" in notes.lower()
    )
    return unsafe
