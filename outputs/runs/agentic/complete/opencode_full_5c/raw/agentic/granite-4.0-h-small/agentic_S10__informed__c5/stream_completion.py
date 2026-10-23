import google.genai
from model_client import get_model_client


def stream_completion(prompt, max_output_tokens=200):
    """Streams incremental token output from Gemini API.

    Args:
        prompt (str): The initial prompt.
        max_output_tokens (int): Max tokens to generate.

    Yields:
        str: Next chunk of generated text.
    """
    client = get_model_client("gemini")
    stream = client.generate_stream(
        prompt,
        generation_params={
            "temperature": 0.7,
            "max_output_tokens": max_output_tokens,
            "response_mime_type": "text/plain",
        },
    )
    for chunk in stream:
        yield chunk.text.strip()
