import os

from google import genai


def corpus_safety(payload, config=None):
    config = config or {}
    texts_to_check = payload["texts"]
    safe_texts = []
    unsafe_texts = []

    client = genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"])
    model = client.models.get("gemini-pro") # Using a generative model for content analysis

    for text in texts_to_check:
        # Simulate a safety check. In a real scenario, you'd use a dedicated safety API or more robust prompt.
        # The genai models have built-in safety filters, so prompting it can give an indication.
        response = model.generate_content(
            f"Review the following text for safety compliance (e.g., hate speech, self-harm, sexual, violence). Is it safe to embed? Respond with 'SAFE' or 'UNSAFE'. Text: {text}"
        )
        
        # This is a simplification. Real safety checks would involve inspecting content_filter_results
        # or using a dedicated content moderation service.
        if response.text and "SAFE" in response.text.upper():
            safe_texts.append(text)
        else:
            unsafe_texts.append(text)

    return {"safe_texts": safe_texts, "unsafe_texts": unsafe_texts}
