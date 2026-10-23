import boto3


def extract_text(document):
    client = boto3.client("textract")
    response = client.detect_document_text(Document={"Bytes": document})
    text = " ".join(
        [
            item["Text"]
            for block in response["Blocks"]
            if block["BlockType"] == "LINE"
            for item in block["Relationships"]
            if item["Type"] == "CHILD"
            for child_block in response["Blocks"]
            if child_block["Id"] == item["Ids"][0]
            and child_block["BlockType"] == "WORD"
        ]
    )
    return text
