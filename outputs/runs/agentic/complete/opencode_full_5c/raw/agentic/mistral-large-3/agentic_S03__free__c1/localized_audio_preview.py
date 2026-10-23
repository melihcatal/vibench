from typing import List
import os
from gtts import gTTS
from pydub import AudioSegment
from io import BytesIO
from translation_models import TranslationResponse


def generate_spoken_preview(
    translations: List[TranslationResponse], output_dir: str = "."
) -> List[str]:
    audio_files = []

    for i, translation in enumerate(translations):
        if isinstance(translation.translated_text, str):
            tts = gTTS(
                text=translation.translated_text,
                lang=translation.detected_source_language or "en",
            )
            audio_file = os.path.join(output_dir, f"translation_{i}.mp3")
            tts.save(audio_file)
            audio_files.append(audio_file)
        elif isinstance(translation.translated_text, list):
            for j, text in enumerate(translation.translated_text):
                tts = gTTS(text=text, lang=translation.detected_source_language or "en")
                audio_file = os.path.join(output_dir, f"translation_{i}_{j}.mp3")
                tts.save(audio_file)
                audio_files.append(audio_file)

    return audio_files
