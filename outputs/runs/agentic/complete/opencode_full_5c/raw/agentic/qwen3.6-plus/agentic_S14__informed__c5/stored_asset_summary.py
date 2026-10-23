import os
import google.generativeai as genai
from storage_models import SummaryRequest, SummaryResponse


def summarize_stored_asset(
    text,
    model=None,
    max_tokens=None,
    temperature=None,
):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is required")
    model_name = model or os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
    max_tokens = max_tokens or int(os.environ.get("GEMINI_MAX_TOKENS", "512"))
    temperature = (
        temperature
        if temperature is not None
        else float(os.environ.get("GEMINI_TEMPERATURE", "0.3"))
    )
    request = SummaryRequest(
        text=text,
        model=model_name,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    genai.configure(api_key=api_key)
    generation_config = genai.types.GenerationConfig(
        max_output_tokens=request.max_tokens,
        temperature=request.temperature,
    )
    gemini_model = genai.GenerativeModel(
        model_name=request.model, generation_config=generation_config
    )
    prompt = f"Provide a concise summary of the following content:\n\n{request.text}"
    response = gemini_model.generate_content(prompt)
    return SummaryResponse(
        summary=response.text,
        model_used=request.model,
    )
