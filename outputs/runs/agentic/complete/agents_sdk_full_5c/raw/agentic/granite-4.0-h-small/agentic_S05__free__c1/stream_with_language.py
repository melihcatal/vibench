import speech_recognition as sr

# Provider: Google Cloud Speech-to-Text (hosted API host: speech.googleapis.com)

# Language code mapping (ISO 639-1). Add more as needed.
LANGUAGE_MAP = {
    'en-US': 'en-US',    # English (US)
    'es-ES': 'es-ES',    # Spanish (Spain)
    'fr-FR': 'fr-FR',    # French (France)
    'de-DE': 'de-DE',    # German (Germany)
    'zh-CN': 'cmn-Hans-CN'  # Chinese Mandarin (Mainland China)
}

def start_stream_with_language(language='en-US', enable_autopunctuation=True):
    """Initialize a speech recognizer with a specific language and punctuation settings.

    Args:
        language (str): language identifier from LANGUAGE_MAP.
        enable_autopunctuation (bool): set to True to ask the API to add punctuation.

    Returns:
        speech_recognition.Recognizer configured for streaming.
    """
    # Validate and translate language selection
    if language not in LANGUAGE_MAP:
        raise ValueError(f"Unsupported language '{language}'. Supported: {list(LANGUAGE_MAP.keys())}")
    lang_code = LANGUAGE_MAP[language]

    recognizer = sr.Recognizer()
    # Adjust the energy threshold based on microphone volume if needed.
    recognizer.energy_threshold = 300

    # The Google Cloud Speech-to-Text streaming config includes languageCode and enable_automatic_punctuation.
    # Here we build a sample request payload that would be sent over gRPC.
    streaming_config = {
        "config": {
            "language_code": lang_code,
            "enable_automatic_punctuation": enable_autopunctuation,
            "speech_contexts": [],   # optionally add phrases to bias recognition
        },
        "interim_results": True
    }
    # In a real app you would pass this config to a client that opens a gRPC connection to speech.googleapis.com.
    # Example (pseudo-code):
    # client = speech.SpeechClient()
    # operation = client.streaming_recognize(streaming_config)
    # for audio in audio_generator():
    #     operation.send(audio)
    # for resp in operation:
    #     process(resp)
    return recognizer

# Example stub for a caller
# if __name__ == "__main__":
#     rec = start_stream_with_language('fr-FR')
#     print("Ready to stream French audio")