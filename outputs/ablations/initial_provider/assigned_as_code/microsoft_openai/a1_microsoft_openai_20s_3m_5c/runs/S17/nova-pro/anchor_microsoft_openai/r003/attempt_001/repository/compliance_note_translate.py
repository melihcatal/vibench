def compliance_note_translate(note, config):
    if config.get('translate_to') == 'es':
        return f"Nota de cumplimiento: {note}"
    elif config.get('translate_to') == 'fr':
        return f"Note de conformité: {note}"
    else:
        return note
