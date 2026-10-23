from safety_client import moderate_text_request


def moderate_text(text: str):
    return moderate_text_request(text)
