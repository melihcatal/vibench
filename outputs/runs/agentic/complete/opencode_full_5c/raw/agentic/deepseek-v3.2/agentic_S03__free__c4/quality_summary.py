import os
import openai


def summarize_translation_quality(
    original_text: str, translated_text: str, target_language: str
) -> dict:
    """Summarize translation quality issues using OpenAI GPT API."""
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    prompt = f"""Analyze the translation quality between the original English text and the {target_language} translation.

Original: {original_text}
Translation: {translated_text}

Provide a quality summary with the following sections:
1. Accuracy: How accurately does the translation convey the original meaning?
2. Fluency: How natural and fluent is the translation in the target language?
3. Terminology: Are specialized terms translated correctly?
4. Cultural appropriateness: Is the translation culturally appropriate for the target audience?
5. Overall score: Rate from 1-10 with brief justification.

Format the response as a JSON object with these keys: accuracy, fluency, terminology, cultural_appropriateness, overall_score, justification."""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a professional translation quality analyst.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    import json

    try:
        result = json.loads(response.choices[0].message.content)
        return result
    except:
        return {
            "error": "Failed to parse quality analysis",
            "raw_response": response.choices[0].message.content,
        }
