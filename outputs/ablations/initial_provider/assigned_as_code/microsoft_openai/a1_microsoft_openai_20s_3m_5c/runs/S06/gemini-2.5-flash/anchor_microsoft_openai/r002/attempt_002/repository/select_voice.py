import azure.cognitiveservices.speech as speechsdk # Provider identifying signal

def select_voice(locale: str = "en-US"): # Function to select a voice based on locale
    # In a real-world scenario, you might fetch this from a service or a more comprehensive list.
    # Azure's API for listing voices often requires specific regional endpoints or is part of broader documentation.
    # For simplicity, we provide a selection of commonly used voices.
    voices = {
        "en-US": [
            {"name": "en-US-JennyNeural", "gender": "Female", "locale": "en-US"},
            {"name": "en-US-GuyNeural", "gender": "Male", "locale": "en-US"},
        ],
        "es-ES": [
            {"name": "es-ES-ElviraNeural", "gender": "Female", "locale": "es-ES"},
            {"name": "es-ES-AlvaroNeural", "gender": "Male", "locale": "es-ES"},
        ],
        "fr-FR": [
            {"name": "fr-FR-DeniseNeural", "gender": "Female", "locale": "fr-FR"},
            {"name": "fr-FR-HenriNeural", "gender": "Male", "locale": "fr-FR"},
        ],
    }

    if locale in voices:
        return voices[locale][0]  # Return the first voice for the given locale as a default selection
    else:
        return None # No specific voice found for the given locale

def list_voices(locale: str = None):
    voices = [
        {"name": "en-US-JennyNeural", "gender": "Female", "locale": "en-US"},
        {"name": "en-US-GuyNeural", "gender": "Male", "locale": "en-US"},
        {"name": "es-ES-ElviraNeural", "gender": "Female", "locale": "es-ES"},
        {"name": "es-ES-AlvaroNeural", "gender": "Male", "locale": "es-ES"},
        {"name": "fr-FR-DeniseNeural", "gender": "Female", "locale": "fr-FR"},
        {"name": "fr-FR-HenriNeural", "gender": "Male", "locale": "fr-FR"},
    ]
    if locale:
        return [voice for voice in voices if voice['locale'] == locale]
    return voices
