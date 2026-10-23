import os
from typing import Dict, Any
from messaging_client import get_openai_client

def summarize_message_content(text_content: str, model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
    openai_client = get_openai_client()
    try:
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes messages concisely."},
                {"role": "user", "content": f"Please summarize the following message:\n\n{text_content}"}
            ],
            temperature=0.7,
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()
        return {"summary": summary, "model_used": model}
    except Exception as e:
        return {"error": str(e), "summary": "Could not generate summary."}