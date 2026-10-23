from typing import Dict
from identity_models import NormalizedProfile

# Placeholder for a third‑party translation SDK (e.g., DeepL, Google Translate)
# For illustration we define a minimal stub that could be swapped out.
try:
    from deep_translator import GoogleTranslator  # type: ignore
except ImportError:
    # Simple no‑op stub if the library is not installed
    class GoogleTranslator:
        def translate(self, text: str, dest_lang: str = "en") -> str:
            # Very naive placeholder – replace with real call in production
            return text


class ConsentTranslator:
    """
    Translate identity‑provider consent copy into the user's preferred language.
    Input is a dict of consent strings keyed by language code (e.g., provider may
    return a JSON payload with a 'copy' field that contains translatable snippets).
    """

    def __init__(self, target_lang: str = "en"):
        self.target_lang = target_lang
        self.translator = GoogleTranslator(source="auto", target=self.target_lang)

    def translate_consent(self, consent_payload: Dict) -> Dict:
        """
        Translates all textual fields inside consent_payload.
        Expected keys: 'title', 'description', 'scopes', 'additional_info'
        Returns a new dict with translated strings.
        """
        translated = {}
        for key in ["title", "description", "scopes", "additional_info"]:
            raw = consent_payload.get(key)
            if raw:
                translated[key] = self.translator.translate(raw)
            else:
                translated[key] = ""
        return translated

    def enrich_profile_with_translated_consent(
        self, profile: NormalizedProfile, raw_consent: Dict
    ) -> NormalizedProfile:
        """
        Add a new field to the profile containing translated consent copy.
        The field name can be 'consent_copy' (type: Dict[str, str]).
        """
        translated = self.translate_consent(raw_consent)
        # Merge into profile dict while preserving existing fields
        profile_dict = dict(profile)
        profile_dict["consent_copy"] = translated
        return NormalizedProfile(**profile_dict)
