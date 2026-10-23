import os
from typing import List
from translation_models import TranslationScore

# Placeholder for actual TTS / audio generation service (e.g., Azure Speech, Google Cloud Text-to-Speech)
# This demo builds a simple markdown preview that could be fed to a TTS API


def generate_spoken_preview(translated_texts: List[str]) -> List[str]:
    """Create a spoken audio preview for each translated text.

    Returns a list of URLs (or file names) where audio could be generated.
    In production, call a TTS service and store the result.
    """
    previews = []
    for i, text in enumerate(translated_texts):
        # Simulated file name pattern for local demo
        preview_file = f"./preview_{i + 1}.mp3"
        previews.append(preview_file)
        # TODO: Call TTS endpoint with text as audio content
        print(
            f"[LocalizedAudioPreview] Would generate audio for: {text} -> {preview_file}"
        )
    return previews


# Demonstration stub (disabled in production)
# if __name__ == "__main__":
#     demo_texts = ["Hello world", "Bonjour le monde"]
#     generated = generate_spoken_preview(demo_texts)
#     print("Generated preview files:", generated)
