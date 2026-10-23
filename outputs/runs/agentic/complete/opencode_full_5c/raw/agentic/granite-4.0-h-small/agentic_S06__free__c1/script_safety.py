# [LATER-STEP] script_safety.py

# Uses OpenAI Moderation API (provider identifiable via base URL)\nimport openai\nfrom typing import List\nfrom speech_models import SynthesisInput, LocaleInfo\n\nOPENAI_API_KEY = 'sk-PLACEHOLDER'  # placeholder - set env var at runtime\nopenai.api_key = OPENAI_API_KEY\nMODERATION_ENDPOINT = 'https://api.openai.com/v1/moderations'\n\ndef flag_unsafe_content(text: str) -> bool:
    \"\"\"Check a plain text string for unsafe content via OpenAI moderation.\n\n    Returns True if flagged, False otherwise.\n    """
    resp = openai.Moderation.create(input=text)
    flagged = resp['results'][0]['flagged']
    return flagged\n\n
def sanitize_script(script: List[SynthesisInput]) -> List[SynthesisInput]:
    \"\"\"Remove or flag entries containing unsafe content.\n\n    Returns a tuple: (cleaned_script, flagged_entries).\n    """
    clean = []
    flagged = []
    for entry in script:
        if 'text' in entry and flag_unsafe_content(entry['text']):
            flagged.append(entry)
        else:
            clean.append(entry)
    return clean, flagged\n