import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def extract_key_values_from_image(image_path: str):
    endpoint = os.environ["VISION_ENDPOINT"]
    key = os.environ["VISION_KEY"]

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    with open(image_path, "rb") as f:
        image_data = f.read()

    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.READ]
    )

    key_value_pairs = {}
    if result.read is not None:
        # For robust key-value pair extraction, Azure AI Document Intelligence is the recommended service.
        # Azure AI Vision's READ feature primarily extracts raw text and its bounding boxes.
        # This implementation will demonstrate a very basic, heuristic-based approach for key-value extraction
        # by looking for common patterns like 'Key: Value' or 'Key Value' on a single line.
        # This is highly simplified and for demonstration purposes within the constraints of using Azure AI Vision.

        lines = []
        for block in result.read.blocks:
            for line in block.lines:
                lines.append(line.text)
        
        # Simple heuristic: look for lines containing a colon or a strong key-value indicator
        for line_text in lines:
            if ":" in line_text:
                parts = line_text.split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key and value:
                        key_value_pairs[key] = value
            # Add other heuristics if necessary, e.g., using regex for common patterns

    return key_value_pairs
