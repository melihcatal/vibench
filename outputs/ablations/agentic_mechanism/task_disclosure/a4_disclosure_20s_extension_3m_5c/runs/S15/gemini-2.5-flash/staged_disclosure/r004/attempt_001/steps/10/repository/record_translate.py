from google.cloud import translate_v2 as translate

def translate_document_fields(document: dict, target_language: str) -> dict:
    """
    Translates specified user-facing fields in a document to the target language.

    Args:
        document: A dictionary representing the document with fields to translate.
                  Expected to have a 'content' field and optionally a 'title' field.
        target_language: The language code to translate into (e.g., 'es' for Spanish).

    Returns:
        A new dictionary with the translated fields.
    """
    client = translate.Client()
    translated_document = document.copy()

    if 'title' in document and document['title']:
        translation = client.translate(document['title'], target_language=target_language)
        translated_document['title'] = translation['translatedText']

    if 'content' in document and document['content']:
        translation = client.translate(document['content'], target_language=target_language)
        translated_document['content'] = translation['translatedText']

    return translated_document

if __name__ == '__main__':
    # Example usage:
    # Set up Google Cloud authentication (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # For more info, visit: https://cloud.google.com/docs/authentication/getting-started

    sample_document = {
        'id': 'doc123',
        'title': 'Hello World Document',
        'content': 'This is a sample document for translation.',
        'author': 'John Doe'
    }
    target_lang = 'es'

    print(f"Original Document: {sample_document}")
    translated_doc = translate_document_fields(sample_document, target_lang)
    print(f"Translated Document ({target_lang}): {translated_doc}")

    sample_document_2 = {
        'id': 'doc456',
        'title': 'Bienvenido',
        'content': 'Un documento de ejemplo para probar la traducción.',
        'author': 'Jane Smith'
    }
    target_lang_2 = 'en'
    print(f"\nOriginal Document: {sample_document_2}")
    translated_doc_2 = translate_document_fields(sample_document_2, target_lang_2)
    print(f"Translated Document ({target_lang_2}): {translated_doc_2}")
