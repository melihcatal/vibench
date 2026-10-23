import json


def translate_text(target_lang: str, text: str) -> str:
    """Translates generated output to a target language using a hosted LLM.

    Args:
        target_lang (str): ISO 639-1 language code (e.g., 'es' for Spanish).
        text (str): The source text to translate.

    Returns:
        str: The translated text.
    """
    client = HostedLLMClient()  # Uses the model_client defined earlier
    model = "gpt-4o-mini"
    messages = [
        {
            "role": "system",
            "content": f"You are a professional translator. Translate the following text into {target_lang.upper()} without commentary.",
        },
        {"role": "user", "content": text},
    ]
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": 512,
    }
    response = client.generate(payload)
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    sample = "The quick brown fox jumps over the lazy dog."
    print("Spanish translation:", translate_text("es", sample))
