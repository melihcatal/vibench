import boto3
from document_client import get_textract_client
from document_models import ExtractedKeyValues, KeyValuePair


def extract_key_values_from_document(document_path: str) -> ExtractedKeyValues:
    textract_client = get_textract_client()

    with open(document_path, "rb") as document:
        image_bytes = document.read()

    response = textract_client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
    )

    key_values = []
    key_map = {}
    value_map = {}
    blocks = response["Blocks"]

    for block in blocks:
        block_id = block["Id"]
        if block["BlockType"] == "KEY_VALUE_SET":
            if "KEY" in block["EntityTypes"]:
                key_map[block_id] = block
            else:
                value_map[block_id] = block

    for block_id, key_block in key_map.items():
        value_block = None
        for rel in key_block.get("Relationships", []):
            if rel["Type"] == "VALUE":
                for value_id in rel["Ids"]:
                    value_block = value_map.get(value_id)
                    break

        if key_block and value_block:
            key_text = ""
            for rel in key_block.get("Relationships", []):
                if rel["Type"] == "CHILD":
                    for child_id in rel["Ids"]:
                        word_block = next(
                            (b for b in blocks if b["Id"] == child_id), None
                        )
                        if word_block:
                            key_text += word_block["Text"] + " "

            value_text = ""
            for rel in value_block.get("Relationships", []):
                if rel["Type"] == "CHILD":
                    for child_id in rel["Ids"]:
                        word_block = next(
                            (b for b in blocks if b["Id"] == child_id), None
                        )
                        if word_block:
                            value_text += word_block["Text"] + " "

            key_values.append(
                KeyValuePair(
                    key=key_text.strip(),
                    value=value_text.strip(),
                    confidence=key_block["Confidence"],
                )
            )

    return ExtractedKeyValues(key_values=key_values)
