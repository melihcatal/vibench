from typing import Dict, Any


def normalize_text_response(response: Dict[str, Any]) -> str:
    text = " ".join(
        [item["Text"] for item in response["Blocks"] if item["BlockType"] == "LINE"]
    )
    return text


def normalize_layout_response(response: Dict[str, Any]) -> Any:
    return response["Blocks"]


def normalize_tables_response(response: Dict[str, Any]) -> Any:
    return [block for block in response["Blocks"] if block["BlockType"] == "TABLE"]


def normalize_key_values_response(response: Dict[str, Any]) -> Dict[str, str]:
    key_values = {}
    for block in response["Blocks"]:
        if block["BlockType"] == "KEY_VALUE_SET":
            key = block["Text"]
            value = block["Relationships"][0]["Ids"][0]
            key_values[key] = value
    return key_values
