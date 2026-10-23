from document_client import create_textract_client, load_image_bytes
from typing import List, Dict


def _get_text(result_block: Dict, blocks: Dict) -> str:
    text = ""
    if "Relationships" in result_block:
        for relationship in result_block["Relationships"]:
            if relationship["Type"] == "CHILD":
                for word_id in relationship["Ids"]:
                    word = blocks[word_id]
                    if "Text" in word:
                        text += word["Text"] + " "
    return text.strip()


def extract_key_values(image_path: str) -> List[Dict[str, str]]:
    data = load_image_bytes(image_path)
    client = create_textract_client()
    response = client.analyze_document(Document={"Bytes": data}, FeatureTypes=["FORMS"])
    blocks_map = {block["Id"]: block for block in response["Blocks"]}
    key_map = {}
    value_map = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            if block["Relationships"]:
                rel = block["Relationships"][0]
                if rel["Type"] == "VALUE":
                    value_map[block["Id"]] = rel["Ids"][0]
                elif rel["Type"] == "KEY":
                    key_map[block["Id"]] = rel["Ids"][0]
    pairs = []
    for kv_id, key_id in key_map.items():
        key_text = _get_text(blocks_map[key_id], blocks_map)
        value_id = value_map.get(kv_id)
        if value_id:
            value_text = _get_text(blocks_map[value_id], blocks_map)
            pairs.append({"key": key_text, "value": value_text})
    return pairs
