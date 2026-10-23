def compliance_note_translate(note, language='en'):
    translation_map = {
        'en': 'Encryption and compliance notes are provided for review.',
        'es': 'Se proporcionan notas de encriptación y cumplimiento para su revisión.'
    }
    return translation_map.get(language, note)