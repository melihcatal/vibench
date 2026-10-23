```python
# appeal_translate.py
# LATER-STEP: Translate appeal text for review

from typing import Dict

# Placeholder: integrate with translation provider (e.g., DeepL, Google Cloud Translation)
# For demo purposes we return the original text unchanged

def translate_appeal(original: str, target_lang: str = 'en') -> str:
    """Return the appeal text translated to target_lang.

    Returns original text when no real translation service is configured.
    """
    # TODO: replace with actual provider client call
    print(f"[APPEAL] Translating '{original}' to {target_lang} (demo)")
    return original

# Example hook for a real provider
# def translate_appeal(provider_client, original, target_lang):
#     return provider_client.translate(original, target_lang)
```