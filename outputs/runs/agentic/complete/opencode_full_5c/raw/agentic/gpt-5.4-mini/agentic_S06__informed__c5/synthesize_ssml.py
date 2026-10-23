from azure.cognitiveservices.speech import SpeechSynthesizer, AudioDataStream

from speech_client import create_speech_config


def synthesize_ssml(ssml: str) -> bytes:
    speech_config = create_speech_config()
    synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_ssml_async(ssml).get()
    stream = AudioDataStream(result)
    return stream.read_data()
