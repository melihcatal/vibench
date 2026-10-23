from translation_client import TranslationClient
from translation_models import normalize_text_input, parse_translation_response

def quality_summary(source_text: str, translated_text: str, target_language: str, source_language: str = "en") -> str:
    """
    Summarizes translation quality issues using OpenAI.
    """
    client_manager = TranslationClient()
    client = client_manager.get_client()
    model_name = client_manager.get_model_name()

    system_prompt = (
        "You are an expert translation quality assurance specialist. "
        f"Your task is to identify and summarize any quality issues in the provided {target_language} translated text, "
        f"compared to the original {source_language} source text. "
        "Focus on accuracy, fluency, grammar, style, and completeness. "
        "If no issues are found, state that the translation quality is excellent." 
        "Provide a concise summary of findings."
    )

    user_prompt = (
        f"Source ({source_language}):\n\n{source_text}\n\n"
        f"Translation ({target_language}):\n\n{translated_text}\n\n"
        "Please summarize any quality issues found in the translation."
    )

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )
    return parse_translation_response(response.choices[0].message.content)
