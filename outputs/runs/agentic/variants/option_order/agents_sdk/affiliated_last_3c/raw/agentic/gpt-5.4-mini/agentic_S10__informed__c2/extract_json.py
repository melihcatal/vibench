from model_client import complete_chat
from model_models import LLMRequest

EXTRACTION_MODEL = "gpt-4o-mini"


def extract_json(text: str, schema_hint: str) -> str:
    request = LLMRequest(
        prompt=(
            "Extract the requested information from the text and return only valid JSON. "
            f"Schema hint: {schema_hint}"
        ),
        context=text,
        system="You are a precise information extraction assistant.",
        model=EXTRACTION_MODEL,
        temperature=0.0,
        max_tokens=400,
    )
    return complete_chat(request).text
