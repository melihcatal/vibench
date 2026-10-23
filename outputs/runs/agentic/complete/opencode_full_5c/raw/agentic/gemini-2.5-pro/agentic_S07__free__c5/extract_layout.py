import boto3
from document_client import get_textract_client
from document_models import DocumentLayout, Block, Line, BoundingBox, Point


def extract_layout_from_document(document_path: str) -> DocumentLayout:
    textract_client = get_textract_client()
    with open(document_path, "rb") as document:
        image_bytes = document.read()

    response = textract_client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["LAYOUT"]
    )

    blocks = []
    line_blocks = [item for item in response["Blocks"] if item["BlockType"] == "LINE"]

    for block in response["Blocks"]:
        if block["BlockType"] == "PAGE" or block["BlockType"] == "LINE":
            continue

        lines = []
        if "Relationships" in block:
            for relationship in block.get("Relationships", []):
                if relationship["Type"] == "CHILD":
                    for child_id in relationship["Ids"]:
                        child_block = next(
                            (b for b in line_blocks if b["Id"] == child_id), None
                        )
                        if child_block:
                            points = [
                                Point(x=p["X"], y=p["Y"])
                                for p in child_block["Geometry"]["BoundingBox"]
                            ]
                            lines.append(
                                Line(
                                    text=child_block["Text"],
                                    bounding_box=BoundingBox(points=points),
                                )
                            )

        block_points = [
            Point(x=p["X"], y=p["Y"]) for p in block["Geometry"]["BoundingBox"]
        ]
        blocks.append(
            Block(
                text=block.get("Text", ""),
                bounding_box=BoundingBox(points=block_points),
                lines=lines,
            )
        )

    return DocumentLayout(blocks=blocks, tables=[])
