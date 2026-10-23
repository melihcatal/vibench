from typing import Dict, Any
import openai

def summarize_record(document: Dict[str, Any], fields_to_summarize: list) -> str:
    """
    Summarizes specified fields of a document using OpenAI's GPT-3.5-turbo model.
    """
    openai.api_key = "sk-proj-..."
    content = " ".join(str(document.get(field, "")) for field in fields_to_summarize)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize the following content."},
            {"role": "user", "content": content}
        ],
        max_tokens=150
    )
    return response.choices[0].message['content'].strip()