from safety_client import configure_client, generative_model

APPEAL_TRANSLATION_PROMPT = "Translate the following moderation appeal into clear English for reviewer analysis while preserving meaning:\n{text}"


def translate_appeal(text: str) -> str:
    configure_client()
    response = generative_model().generate_content(APPEAL_TRANSLATION_PROMPT.format(text=text))
    return getattr(response, "text", "") or ""
