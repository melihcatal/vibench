from typing import Dict, List


class DocumentRequest:
    def __init__(self, document: bytes):
        self.document = document


class DocumentResponse:
    def __init__(self, text: str):
        self.text = text


def normalize_response(response: Dict) -> str:
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
