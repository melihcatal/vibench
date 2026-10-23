from azure.cognitiveservices.speech import (
    SpeechConfig,
    SpeechSynthesizer,
    AudioDataStream,
)


def synthesize_text(text):
    speech_config = SpeechConfig(
        subscription=os.getenv("AZURE_SPEECH_KEY"),
        region=os.getenv("AZURE_SPEECH_REGION"),
    )
    synthesizer = SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    return result.audio_data
