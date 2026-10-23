from google.cloud import translate_v2 as translate


def translate_invoice_notes(notes, target_language='en'):
    client = translate.Client()
    translated_notes = []
    for note in notes:
        result = client.translate(note, target_language=target_language)
        translated_notes.append(result['translatedText'])
    return translated_notes