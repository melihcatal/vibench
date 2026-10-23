import os
import deepl
from typing import List
from database_models import Document


def translate_records(
    records: List[Document], target_lang: str = "EN"
) -> List[Document]:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    for record in records:
        new_data = {}
        for k, v in record["data"].items():
            if isinstance(v, str) and v.strip():
                result = translator.translate_text(v, target_lang=target_lang)
                new_data[k] = result.text
            else:
                new_data[k] = v
        record["data"] = new_data
    return records
