import os
import json
from typing import Dict, List, Any, Optional
import requests
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials


def extract_layout_from_image(
    image_path: str, include_tables: bool = True, include_lines: bool = True
) -> Dict[str, Any]:
    """
    Extract layout elements (blocks, lines, tables) from a document using Azure Computer Vision Read API.

    Args:
        image_path: Path to the image file
        include_tables: Whether to extract table structures
        include_lines: Whether to extract line information

    Returns:
        Dictionary containing layout elements
    """
    endpoint = os.environ.get(
        "AZURE_VISION_ENDPOINT", "https://your-endpoint.cognitiveservices.azure.com/"
    )
    subscription_key = os.environ.get("AZURE_VISION_KEY", "your-subscription-key")

    client = ComputerVisionClient(
        endpoint, CognitiveServicesCredentials(subscription_key)
    )

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    read_response = client.read_in_stream(image_data, raw=True)

    operation_location = read_response.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    import time

    while True:
        result = client.get_read_result(operation_id)
        if result.status not in ["notStarted", "running"]:
            break
        time.sleep(1)

    if result.status == "failed":
        raise Exception(f"Azure Read API failed: {result}")

    layout_data = {"pages": [], "blocks": [], "lines": [], "tables": []}

    for page in result.analyze_result.read_results:
        page_info = {
            "page_number": page.page,
            "width": page.width,
            "height": page.height,
            "angle": page.angle,
            "unit": page.unit,
        }
        layout_data["pages"].append(page_info)

        for line in page.lines:
            line_info = {
                "text": line.text,
                "bounding_box": line.bounding_box,
                "words": [
                    {"text": w.text, "bounding_box": w.bounding_box} for w in line.words
                ],
            }
            layout_data["lines"].append(line_info)

    return layout_data


def extract_layout_from_url(image_url: str) -> Dict[str, Any]:
    """
    Extract layout elements from an image URL using Azure Computer Vision Read API.

    Args:
        image_url: URL of the image

    Returns:
        Dictionary containing layout elements
    """
    endpoint = os.environ.get(
        "AZURE_VISION_ENDPOINT", "https://your-endpoint.cognitiveservices.azure.com/"
    )
    subscription_key = os.environ.get("AZURE_VISION_KEY", "your-subscription-key")

    client = ComputerVisionClient(
        endpoint, CognitiveServicesCredentials(subscription_key)
    )

    read_response = client.read(image_url, raw=True)

    operation_location = read_response.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    import time

    while True:
        result = client.get_read_result(operation_id)
        if result.status not in ["notStarted", "running"]:
            break
        time.sleep(1)

    if result.status == "failed":
        raise Exception(f"Azure Read API failed: {result}")

    layout_data = {"pages": [], "blocks": [], "lines": [], "tables": []}

    for page in result.analyze_result.read_results:
        page_info = {
            "page_number": page.page,
            "width": page.width,
            "height": page.height,
            "angle": page.angle,
            "unit": page.unit,
        }
        layout_data["pages"].append(page_info)

        for line in page.lines:
            line_info = {
                "text": line.text,
                "bounding_box": line.bounding_box,
                "words": [
                    {"text": w.text, "bounding_box": w.bounding_box} for w in line.words
                ],
            }
            layout_data["lines"].append(line_info)

    return layout_data
