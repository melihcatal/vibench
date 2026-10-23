import os
import openai


def quality_summary(source_text: str, translated_text: str) -> str:
    """
    Summarizes translation quality issues using OpenAI's GPT model.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set.")

    prompt = f"""
    Source text: "{source_text}"
    Translated text: "{translated_text}"

    Please provide a brief summary of the translation quality.
    Point out any potential issues with grammar, fluency, or accuracy.
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a translation quality expert."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=256,
    )
    return response.choices[0].message.content
