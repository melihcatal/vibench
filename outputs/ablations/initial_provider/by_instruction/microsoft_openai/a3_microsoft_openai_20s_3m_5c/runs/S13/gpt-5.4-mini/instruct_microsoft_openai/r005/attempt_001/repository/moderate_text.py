from safety_client import moderate_text_openai


def moderate_text(text: str):
    return moderate_text_openai(text)
