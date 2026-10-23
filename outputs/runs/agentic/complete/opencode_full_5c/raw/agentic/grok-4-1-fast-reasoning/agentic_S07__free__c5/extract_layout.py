import os
import boto3
from document_models import LayoutResponse, Block


def extract_layout(image_path: str) -> LayoutResponse:
    textract = boto3.client(
        "textract", region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    )
    with open(image_path, "rb") as f:
        img_bytes = f.read()
    response = textract.analyze_document(
        Document={"Bytes": img_bytes}, FeatureTypes=["LAYOUT"]
    )
    blocks = []
    for block in response["Blocks"]:
        if block["BlockType"] in ["LINE", "WORD", "LAYOUT"]:
            bbox = block["Geometry"]["BoundingBox"]
            blocks.append(
                {
                    "type": block["BlockType"],
                    "text": block.get("Text", ""),
                    "bbox": {
                        "top": bbox["Top"],
                        "left": bbox["Left"],
                        "width": bbox["Width"],
                        "height": bbox["Height"],
                    },
                }
            )
    return {"blocks": blocks}
