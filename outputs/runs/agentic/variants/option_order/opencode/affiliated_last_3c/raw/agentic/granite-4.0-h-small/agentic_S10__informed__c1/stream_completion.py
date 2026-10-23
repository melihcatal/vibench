# Stream partial output tokens from a hosted LLM via Gemini API
import google.generativeai as genai


def stream_completion(prompt: str, model: str = "gemini-1.5-flash") -> None:
    """Stream tokens from a hosted LLM using Gemini's streaming endpoint.

    Args:
        prompt: The text prompt to complete.
        model: Gemini model identifier.
    """
    genai.configure(api_key="GOOGLE_API_KEY")
    model = genai.GenerativeModel(model)
    # Use streaming generation
    response = model.generate_content(
        prompt, generation_config=genai.types.GenerationConfig(stream=True)
    )
    for chunk in response.stream:
        print(chunk.text, end="", flush=True)
