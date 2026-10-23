import os

try:
    from anthropic import Anthropic  # Using Anthropic Chat API as example
except ImportError:
    raise ImportError("Install Anthropic SDK: pip install anthropic")

# Load API key from environment (Anthropic)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise RuntimeError("Set the ANTHROPIC_API_KEY environment variable")


def summarize_quality(translated_texts: list[str]) -> str:
    """Summarize translation quality issues using Anthropic model.

    Args:
        translated_texts (list[str]): List of translated text strings.

    Returns:
        str: Summary of detected quality issues.
    """
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    prompt = (
        "You are a code reviewer specialized in translation quality.\n"
        f"Analyze the following translated texts and return a concise summary of any"
        " quality issues (e.g., mistranslations, awkward phrasing, missing tags)."
    )
    prompt += "\nTranslated texts:\\n" + "\\n".join(f"> {t}" for t in translated_texts)
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.content[0]["text"]
