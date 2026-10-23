from translation_client import openai_client


def summarize_translation_quality(
    original_text: str, translated_text: str, source_lang: str, target_lang: str
) -> str:
    if not openai_client:
        raise ValueError(
            "OpenAI client not initialized. Please set OPENAI_API_KEY environment variable."
        )

    prompt = f"""Summarize any potential quality issues in the translation from {source_lang} to {target_lang}. 
    Original text: {original_text}
    Translated text: {translated_text}
    Focus on accuracy, fluency, and cultural appropriateness. Provide a concise summary.
    """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",  # Using a cost-effective model for summarization
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes translation quality issues.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()
