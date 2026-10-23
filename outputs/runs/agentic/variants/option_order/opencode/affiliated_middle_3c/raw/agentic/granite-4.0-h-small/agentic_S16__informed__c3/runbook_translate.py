import re

# Simple translation of English runbook notes to Spanish using hardcoded mappings
EN_TO_ES = {
    "Current version is": "Versión actual es",
    "Latest version is": "Versión más reciente es",
    "Rotate secret": "Rotar secreto",
    "Secret ID": "Identificador de secreto",
    "Version ID": "Identificador de versión",
    "Successfully rotated": "Rotado con éxito",
    "Failed to rotate": "No se pudo rotar",
}

PUNCTUATION = {".": ".", "?": "?", "!": "!"}


def runbook_translate(text: str) -> str:
    """Translate runbook lines from English to Spanish."""
    # Replace known phrases first
    for old, new in EN_TO_ES.items():
        text = text.replace(old, new)
    # Preserve punctuation at the end of sentences
    # Simple heuristic: split on whitespace, translate each word, then re‑attach punctuation
    # Split while keeping punctuation markers
    parts = re.split(r"(\s+)", text)
    translated = []
    for part in parts:
        # If part is punctuation, leave it unchanged
        if part in PUNCTUATION:
            translated.append(part)
        else:
            translated.append(part.strip())
    return "".join(translated)
