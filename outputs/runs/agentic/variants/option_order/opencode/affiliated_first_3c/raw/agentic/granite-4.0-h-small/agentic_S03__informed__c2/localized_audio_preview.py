import time
from functools import lru_cache


class LocalizedAudioPreview:
    MAX_CACHE_SIZE = 100  # samples to cache locally
    CACHE_TTL_SECONDS = 3600  # keep for 1 hour

    @lru_cache(maxsize=MAX_CACHE_SIZE)
    def generate_preview(self, translated_text: str, language_code: str = "en") -> str:
        """Generate a spoken audio preview of localized copy.
        In a real implementation this would synthesize speech via a TTS API.
        Here we simulate a preview ID.
        """
        preview_id = f"preview-{language_code}-{hash(translated_text)}"
        # Simulate delay to represent network synthesis
        time.sleep(0.2)
        return f"Synthetic preview for {language_code} : {preview_id}"


if __name__ == "__main__":
    preview = LocalizedAudioPreview().generate_preview(
        "Hello world", language_code="es"
    )
    print(preview)
    # Subsequent calls to the same text return cached result
    preview_cached = LocalizedAudioPreview().generate_preview(
        "Hello world", language_code="es"
    )
    print("Cached?", preview == preview_cached)
