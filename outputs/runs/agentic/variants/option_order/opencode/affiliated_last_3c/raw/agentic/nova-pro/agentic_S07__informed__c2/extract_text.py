import boto3


def extract_text(image_path):
    textract = boto3.client("textract")
    with open(image_path, "rb") as image:
        response = textract.detect_document_text(Document={"Bytes": image.read()})
    text = " ".join(
        [
            item["Text"]
            for block in response["Blocks"]
            if block["BlockType"] == "LINE"
            for item in block["Relationships"]
            if item["Type"] == "CHILD"
            for block in response["Blocks"]
            if block["Id"] == item["Ids"][0]
        ]
    )
    return text
