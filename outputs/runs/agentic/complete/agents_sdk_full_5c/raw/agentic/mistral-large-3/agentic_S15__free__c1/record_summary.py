from typing import Dict, Any
import openai

def summarize_record(document: Dict[str, Any], model: str = "gpt-4o-mini") -> str:
    """
    Summarizes retrieved document records using OpenAI's GPT model.
    """
    prompt = f"Summarize the following document in 2-3 sentences:\n\n{document}"
    response = openai.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()