import os
import azure.cognitiveservices.speech as speechsdk


def get_speech_config() -> speechsdk.SpeechConfig:
    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    service_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError(
            "AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set."
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    # Default voice setting, can be overridden
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    return speech_config


def get_speech_synthesizer() -> speechsdk.SpeechSynthesizer:
    speech_config = get_speech_config()
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    return speech_synthesizer


def get_speech_recognizer() -> speechsdk.SpeechRecognizer:
    speech_config = get_speech_config()
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )
    return speech_recognizer


if __name__ == "__main__":
    # Example usage
    # try:
    #     synthesizer = get_speech_synthesizer()
    #     print("Speech synthesizer client created successfully.")
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass
