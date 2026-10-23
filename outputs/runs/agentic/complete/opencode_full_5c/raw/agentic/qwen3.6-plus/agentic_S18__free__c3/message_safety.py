import os
import json
from typing import Optional
from google.cloud import aiplatform
from vertexai.generative_models import (
    GenerativeModel,
    SafetySetting,
    HarmCategory,
    HarmBlockThreshold,
)
from messaging_models import EventMessage, normalize_payload


GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "default-project")
GCP_LOCATION = os.environ.get("VERTEX_AI_LOCATION", "us-central1")
SAFETY_MODEL_ID = "gemini-1.5-flash-001"


def initialize_vertex_ai():
    aiplatform.init(
        project=GCP_PROJECT_ID,
        location=GCP_LOCATION,
    )


def check_message_safety(text: str, categories: list = None) -> dict:
    initialize_vertex_ai()

    safety_settings = [
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
    ]

    model = GenerativeModel(
        SAFETY_MODEL_ID,
        safety_settings=safety_settings,
    )

    prompt = f"Analyze the following text for unsafe content and return a JSON object with keys: safe (boolean), categories_flagged (list of strings), severity (low/medium/high), and reason (string). Text: {text}"

    try:
        response = model.generate_content(prompt)
        result_text = response.text
        result_json = json.loads(result_text)
        return {
            "safe": result_json.get("safe", True),
            "categories_flagged": result_json.get("categories_flagged", []),
            "severity": result_json.get("severity", "low"),
            "reason": result_json.get("reason", ""),
            "model_id": SAFETY_MODEL_ID,
        }
    except json.JSONDecodeError:
        return {
            "safe": True,
            "categories_flagged": [],
            "severity": "unknown",
            "reason": "Could not parse safety analysis response",
            "model_id": SAFETY_MODEL_ID,
        }
    except Exception as exc:
        return {
            "safe": True,
            "categories_flagged": [],
            "severity": "unknown",
            "reason": f"Safety check failed: {str(exc)}",
            "model_id": SAFETY_MODEL_ID,
        }


def check_event_payload_safety(event_data: dict) -> dict:
    event = EventMessage.from_dict(event_data)
    payload = normalize_payload(event.payload)
    text_to_check = " ".join(str(v) for v in payload.values())
    return check_message_safety(text_to_check)
