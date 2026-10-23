import azure.ai.translation.document as translation


def translate_consent(text, config):
    client = translation.DocumentTranslationClient(endpoint=config['endpoint'], credential=config['credential'])
    result = client.translate_document(document=text, to=['es'])
    return result.translations[0].content