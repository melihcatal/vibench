import os
from model_client import get_llm_client
from model_models import normalize_text

def summarize_text(text: str) -> str:
    """Summarize long text using a hosted LLM.
    Uses Anthropic Claude via the Anthropic SDK.
    """
    client = get_llm_client()
    prompt = f"Summarize the following text in no more than 3 sentences:\n\n{text}"
    # Call the model with the Anthropic chat completion API
    response = client.chat.completions.create(
        model="claude-3-5-sonnet-20240620",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    summary = response.choices[0].message.content
    return normalize_text(summary)
