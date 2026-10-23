# [SAME-SCENARIO] stream_with_language.py
# Starts a streaming recognizer with language and punctuation settings using Azure Speech Streaming API
import asyncio
from azure.cognitiveservices.speech import AudioConfig, SpeechConfig, SpeechRecognizer

# Azure Speech authentication
AZURE_SPEECH_KEY = "${AZURE_SPEECH_KEY}"
AZURE_SPEECH_REGION = "eastus"

# Language configuration
LANGUAGE_CODE = "ja-JP"  # Japanese language example


async def stream_with_language(audio_source):
    speech_config = SpeechConfig(
        subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION
    )
    speech_config.speech_recognition_language = LANGUAGE_CODE
    speech_config.enable_dictation = (
        True  # Enable punctuation and language understanding
    )

    audio_config = AudioConfig(use_default_microphone=False)  # Use custom audio source

    recognizer = SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Placeholder for async iteration over audio_source
    audio_async_iter = iter(audio_source())  # Simplified for example
    result = await recognizer.recognize_once_async(audio_config=audio_config)
    print(f"Recognized: {result.text}")


if __name__ == "__main__":
    asyncio.run(stream_with_language(lambda: []))  # Placeholder
