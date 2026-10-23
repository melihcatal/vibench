from typing import Dict, Any
import openai

def summarize_record(document: Dict[str, Any], field_name: str = "content") -> str:
    """
    Summarizes a document field using OpenAI's GPT-3.5-turbo model.
    """
    content = document.get(field_name, "")
    if not content:
        return ""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize the following text:"},
            {"role": "user", "content": content}
        ],
        max_tokens=100
    )
    return response.choices[0].message["content"].strip()