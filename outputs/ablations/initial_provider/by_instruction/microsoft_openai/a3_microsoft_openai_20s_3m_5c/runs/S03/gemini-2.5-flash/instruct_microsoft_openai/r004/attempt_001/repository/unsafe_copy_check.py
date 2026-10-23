from translation_client import TranslationClient
from translation_models import normalize_text_input, parse_translation_response

def unsafe_copy_check(localized_text: str, language: str) -> str:
    """
    Checks localized copy for unsafe content using OpenAI.
    """
    client_manager = TranslationClient()
    client = client_manager.get_client()
    model_name = client_manager.get_model_name()

    system_prompt = (
        "You are a content moderation AI. Your task is to analyze the provided text "
        "and identify any content that could be considered unsafe, inappropriate, offensive, "
        "or harmful in the context of the given language and culture. "
        "Provide a brief summary of any concerns found. If no unsafe content is detected, "
        "state that the content appears safe."
    )

    user_prompt = (
        f"Analyze the following text in {language} for any unsafe content:\n\n{localized_text}"
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )
    return parse_translation_response(response.choices[0].message.content)
