from google.cloud import language_v2

def check_payload_safety(decrypted_text: str):
    """
    Checks decrypted text payloads for unsafe content using Google Cloud Language AI's moderateText.
    """
    client = language_v2.LanguageServiceClient()

    document = language_v2.Document(
        content=decrypted_text, 
        type_=language_v2.Document.Type.PLAIN_TEXT
    )

    response = client.moderate_text(document=document)

    return response.moderation_categories
