import os
from model_client import get_llm_client
from model_models import LLMResponse

def spoken_brief(text: str, model_name: str = "gpt-4o-mini") -> str:
    """Generate a spoken (audio-friendly) brief summary from model output.
    Tailors language for a voice synthesis pipeline: short sentences, natural pacing.
    Uses a hosted LLM to rewrite the input text accordingly.
    Identifies provider via SDK import and model identifier.
    Returns the spoken-friendly version.
    """
    client = get_llm_client(model_name)
    prompt = (
        "Rewrite the following content into a concise, spoken-friendly brief. Use short sentences,"
        " clear pacing, and avoid overly technical phrasing. Keep it under 100 words."
        "\n\n{text}"
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    norm_resp = LLMResponse.from_openai(response)
    return norm_resp.get_content()
