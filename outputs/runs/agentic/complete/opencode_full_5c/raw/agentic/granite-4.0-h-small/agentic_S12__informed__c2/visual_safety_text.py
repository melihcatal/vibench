# [LATER-STEP] visual_safety_text.py

import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from vision_models import DetectedLabel
from typing import List

AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def check_generated_labels_for_unsafe_text(
    labels: List[DetectedLabel], detected_texts: List[str]
) -> bool:
    """
    Check visual labels for unsafe or policy-sensitive text using Azure AI Content Safety.
    Returns True if any unsafe content is found.
    """
    if not AZURE_CONTENT_SAFETY_ENDPOINT or not AZURE_CONTENT_SAFETY_KEY:
        raise RuntimeError(
            "Set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
        )
    client = ContentSafetyClient(
        endpoint=AZURE_CONTENT_SAFETY_ENDPOINT,
        credential=AzureKeyCredential(AZURE_CONTENT_SAFETY_KEY),
    )
    # Combine labels and raw texts into a single document for the safety service
    document = " \n".join([lbl.name for lbl in labels] + detected_texts)
    response = client.analyze_content(document)
    return response["result"] == "unsafe"
