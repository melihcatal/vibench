# localized_audio_preview.py
from IPython.display import Audio
from typing import List
from translation_models import TranslateResponse


def generate_audio_preview(text: str) -> Audio:
    """Generate an audio preview (placeholder) from translated text."""
    # Placeholder: replace with real TTS service like gTTS or Google Cloud Text-to-Speech
    return Audio(text=text, lang="en")


def create_localized_previews(translations: List[TranslateResponse]) -> List[Audio]:
    """Return a list of Audio objects for each translated segment."""
    return [generate_audio_preview(t["translated_text"]) for t in translations]
