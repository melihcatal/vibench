def consent_translate(consent_copy):
    translated_copy = {}
    for key, value in consent_copy.items():
        if key in ['terms', 'privacy']:
            translated_copy[key] = value
    return translated_copy