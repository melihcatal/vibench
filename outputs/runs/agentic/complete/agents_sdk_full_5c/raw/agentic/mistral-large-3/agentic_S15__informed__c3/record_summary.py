from typing import Dict, Any
import openai

def summarize_record(document: Dict[str, Any], fields: list[str]) -> str:
    openai.api_key = openai.api_key or os.getenv("OPENAI_API_KEY")
    content = " ".join(str(document.get(field, "")) for field in fields)
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the following document fields concisely."},
            {"role": "user", "content": content}
        ],
        max_tokens=150
    )
    return response.choices[0].message["content"]