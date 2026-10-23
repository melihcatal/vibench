from translation_client import get_openai_client


def summarize_quality(
    original_text: str, translated_text: str, source_language: str, target_language: str
) -> str:
    """
    Summarizes potential quality issues in a translation using an LLM.

    Args:
        original_text: The source text.
        translated_text: The translated text.
        source_language: The source language name.
        target_language: The target language name.

    Returns:
        A summary of potential quality issues.
    """
    client = get_openai_client()
    prompt = f"""
    Please evaluate the quality of the following translation from {source_language} to {target_language}.
    Provide a brief summary of any potential issues regarding grammar, fluency, tone, and accuracy.
    If there are no issues, state that the translation is of high quality.

    Source Text ({source_language}):
    "{original_text}"

    Translated Text ({target_language}):
    "{translated_text}"

    Quality Summary:
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a translation quality expert."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=256,
    )
    return response.choices[0].message.content.strip()
