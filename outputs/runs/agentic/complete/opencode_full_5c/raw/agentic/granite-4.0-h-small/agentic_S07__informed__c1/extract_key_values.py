# Placeholder implementation for key-value extraction
# This file demonstrates a same-scenario helper that would later call an OCR result

import dataclasses
from typing import Dict, List


# Local model definition for a key-value pair
@dataclasses.dataclass
class KeyValue:
    key: str
    value: str


# Normalized response container
KeyValuesResult = List[KeyValue]

# Placeholder: replace with actual OCR extraction result
# In a concrete integration you would invoke extract_text.py and then apply NLP parsing


def parse_key_values(ocr_text: List[str]) -> KeyValuesResult:
    """Very naive key-value parsing based on line patterns."""
    kv_list = []
    for line in ocr_text:
        if ":" in line:
            parts = line.split(":", 1)
            kv_list.append(
                KeyValue(
                    key=parts[0].strip(),
                    value=parts[1].strip() if len(parts) > 1 else "",
                )
            )
    return kv_list
