import json
import os
from typing import Dict, Any

import boto3

from messaging_models import Message

def check_message_safety(message: Message, region_name: str, language_code: str = 'en') -> Dict[str, Any]:
    """
    Checks the message payload text for unsafe content, specifically PII (Personally Identifiable Information),
    using AWS Comprehend.
    """
    comprehend_client = boto3.client("comprehend", region_name=region_name)

    safety_results = {
        "message_id": message.id,
        "pii_detection": [],
        "is_safe": True,
        "details": "No PII detected."
    }

    message_text = message.body.get("text")
    if message_text and isinstance(message_text, str):
        try:
            pii_response = comprehend_client.detect_pii_entities(Text=message_text, LanguageCode=language_code)
            if pii_response["Entities"]:
                safety_results["pii_detection"] = pii_response["Entities"]
                safety_results["is_safe"] = False
                safety_results["details"] = "PII detected in message content."
        except Exception as e:
            safety_results["is_safe"] = False
            safety_results["details"] = f"Error during PII detection: {str(e)}"
    else:
        safety_results["details"] = "No text content found for safety check."

    return safety_results
