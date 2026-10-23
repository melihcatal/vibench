from document_client import get_openai_client

def ocr_safety(text: str) -> dict:
    if not text.strip():
        return {'flagged': False}
    client = get_openai_client()
    response = client.moderations.create(
        model="text-moderation-latest",
        input=text
    )
    return response.results[0]