import os
from typing import List, Dict, Optional

import requests


def detect_image_text(
    image_bytes: bytes,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> List[Dict[str, str]]:
    """
    Detects text in an image using Azure AI Vision.

    Args:
        image_bytes: Bytes of the image to analyze.
        endpoint: Azure AI Vision endpoint. If None, uses AZURE_VISION_ENDPOINT.
        key: Azure AI Vision key. If None, uses AZURE_VISION_KEY.

    Returns:
        List of dictionaries containing 'text' and 'bounding_box' for each detected text region.
    """
    if not endpoint:
        endpoint = os.getenv("AZURE_VISION_ENDPOINT")
    if not key:
        key = os.getenv("AZURE_VISION_KEY")

    if not endpoint or not key:
        raise ValueError("Azure AI Vision endpoint and key must be provided.")

    url = f"{endpoint}/vision/v3.2/read/analyze"
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/octet-stream",
    }

    try:
        response = requests.post(url, headers=headers, data=image_bytes)
        response.raise_for_status()
        operation_url = response.headers["Operation-Location"]

        # Poll for results
        while True:
            result = requests.get(
                operation_url, headers={"Ocp-Apim-Subscription-Key": key}
            )
            result.raise_for_status()
            if result.json().get("status") in ["succeeded", "failed"]:
                break

        if result.json().get("status") == "succeeded":
            read_results = result.json().get("analyzeResult", {}).get("readResults", [])
            texts = []
            for read_result in read_results:
                for line in read_result.get("lines", []):
                    texts.append(
                        {
                            "text": line.get("text", ""),
                            "bounding_box": str(line.get("boundingBox", [])),
                        }
                    )
            return texts
        else:
            raise Exception("Azure AI Vision text detection failed.")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Azure AI Vision error: {e}")
