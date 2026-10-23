from model_client import client
from model_models import extract_completion_content

def translate_output(text: str, target_language: str = "Spanish") -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Translate the following text to {target_language}:\n\n{text}"}
        ],
        temperature=0.1,
    )
    return extract_completion_content(response)