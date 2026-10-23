import os
from openai import OpenAI

def is_annotation_safe(annotation_text: str) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        input=annotation_text
    )
    return not response.results[0].flagged