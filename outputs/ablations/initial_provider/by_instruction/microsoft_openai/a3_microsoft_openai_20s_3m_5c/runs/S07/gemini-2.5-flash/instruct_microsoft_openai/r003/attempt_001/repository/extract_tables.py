import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

def extract_tables_from_image(image_path: str):
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

    tables_data = []
    if result.read is not None:
        # Azure AI Vision's READ feature extracts text, but directly extracting table structure (cells, rows) as a distinct entity
        # is typically more robust with Azure AI Document Intelligence. 
        # For the purpose of this task and staying within Azure AI Vision, we'll iterate through lines
        # and assume a post-processing step would interpret table-like structures based on bounding boxes.
        # If a more direct table extraction is needed within Azure, Azure AI Document Intelligence would be the service to use.

        # This is a simplified representation. A real-world table extraction would involve more sophisticated logic
        # to group lines into cells and cells into rows/columns based on their spatial relationships.
        for block in result.read.blocks:
            for line in block.lines:
                # For now, we'll just store lines that might be part of a table.
                # A more advanced implementation would analyze bounding boxes to infer table structure.
                tables_data.append({"text": line.text, "bounding_box": line.bounding_box})
    return tables_data
