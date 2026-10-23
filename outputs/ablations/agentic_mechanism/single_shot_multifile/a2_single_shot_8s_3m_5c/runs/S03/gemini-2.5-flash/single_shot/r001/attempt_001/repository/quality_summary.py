import os
from openai import OpenAI

def summarize_translation_quality(source_text: str, translated_text: str, target_language: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = (
        f"Analyze the following translation from the original text into {target_language}. "
        "Identify any potential quality issues such as accuracy, fluency, grammar, style, or cultural appropriateness. "
        "Provide a brief summary of the assessment and suggest areas for improvement."
        f"\n\nOriginal Text: {source_text}"
        f"\nTranslated Text: {translated_text}"
    )

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for translation quality assessment."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    summary = response.choices[0].message.content
    return summary
