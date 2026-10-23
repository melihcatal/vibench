from __future__ import annotations

import json
import os
from typing import Any, Dict

import boto3
import requests
from openai import OpenAI

from vision_models import ImageSource, image_to_data_uri


def get_azure_vision_config() -> Dict[str, str]:
    endpoint = os.environ["AZURE_VISION_ENDPOINT"].rstrip("/")
    key = os.environ["AZURE_VISION_KEY"]
    return {"endpoint": endpoint, "key": key}


def get_openai_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


def get_aws_rekognition_client():
    region = (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )
    return boto3.client("rekognition", region_name=region)


def get_moderation_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"]
    return OpenAI(api_key=api_key)


def azure_vision_analyze(image: ImageSource, features: str) -> Dict[str, Any]:
    config = get_azure_vision_config()
    url = f"{config['endpoint']}/computervision/imageanalysis:analyze?api-version=2024-02-01&features={features}"
    headers = {
        "Ocp-Apim-Subscription-Key": config["key"],
    }
    if image.image_url:
        headers["Content-Type"] = "application/json"
        payload: Any = {"url": image.image_url}
    else:
        headers["Content-Type"] = "application/octet-stream"
        payload = image.image_bytes
    response = requests.post(
        url,
        headers=headers,
        json=payload if isinstance(payload, dict) else None,
        data=payload if isinstance(payload, (bytes, bytearray)) else None,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def openai_vision_response(image: ImageSource, prompt: str) -> Dict[str, Any]:
    client = get_openai_client()
    input_image = image_to_data_uri(image)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": input_image},
                ],
            }
        ],
    )
    return json.loads(response.model_dump_json())
