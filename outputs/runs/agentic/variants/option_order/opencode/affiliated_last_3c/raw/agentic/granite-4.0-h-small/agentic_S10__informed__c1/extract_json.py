# Extract structured JSON from text using a hosted LLM via Mistral API
import mistralai


def extract_json(text: str, model: str = "mistral-large-latest") -> dict:
    """Extract structured JSON from a prompt using a hosted LLM.

    Args:
        text: The input text containing structured data.
        model: Model identifier for the Mistral endpoint.

    Returns:
        Parsed JSON object.
    """
    client = mistralai.Clients(secret_key="MISTRAL_API_KEY")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": text}],
        temperature=0.0,
    )
    # Ensure the response is valid JSON
    import json

    return json.loads(response.choices[0].message.content)
