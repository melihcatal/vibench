import os
from model_client import get_llm_client
from model_models import normalize_json

def extract_json(text: str) -> dict:
    """Extract structured JSON from text using a hosted LLM.
    Demonstrates usage with Anthropic Claude via the Anthropic SDK.
    """
    client = get_llm_client()
    system_prompt = "You are an assistant that returns ONLY valid JSON.",
    prompt = f"Extract the following information from the text below as JSON, with keys 'name', 'date', and 'status'. Do not add extra fields:\n\n{text}"
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20240620",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0,
    )
    json_str = response.choices[0].message.content.strip()
    return normalize_json(json_str)
