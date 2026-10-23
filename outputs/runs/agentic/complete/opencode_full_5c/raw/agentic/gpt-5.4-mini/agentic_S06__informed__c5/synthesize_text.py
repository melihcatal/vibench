from azure.cognitiveservices.speech import (
    SpeechSynthesisOutputFormat,
    SpeechSynthesizer,
    AudioDataStream,
)

from speech_client import create_speech_config


def synthesize_text(text: str, voice_name: str = None) -> bytes:
    speech_config = create_speech_config()
    speech_config.set_speech_synthesis_output_format(
        SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
    )
    if voice_name:
        speech_config.speech_synthesis_voice_name = voice_name
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_text_async(text).get()
    stream = AudioDataStream(result)
    return stream.read_data()
