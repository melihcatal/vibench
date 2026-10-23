from typing import Iterator
import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import SynthesisRequest, SynthesisResponse


def synthesize_ssml(request: SynthesisRequest) -> Iterator[SynthesisResponse]:
    speech_config = get_speech_config()
    audio_config = speechsdk.audio.PullAudioOutputStream.create_push_stream()
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = speech_synthesizer.speak_ssml(request.ssml)
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        stream = speechsdk.AudioDataStream(result)
        while True:
            audio_buffer = bytes(1024)
            filled_size = stream.read_data(audio_buffer)
            if filled_size == 0:
                break
            yield SynthesisResponse(audio_chunk=audio_buffer[:filled_size])
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}")