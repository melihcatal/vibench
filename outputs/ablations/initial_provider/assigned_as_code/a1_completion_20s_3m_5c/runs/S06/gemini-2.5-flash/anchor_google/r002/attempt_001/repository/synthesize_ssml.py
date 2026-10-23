from speech_client import SpeechClient
from speech_models import SynthesisPayload
from google.cloud import texttospeech

def synthesize_ssml(payload: SynthesisPayload):
    client = SpeechClient().get_client()
    synthesis_input = payload.to_synthesis_input()
    voice_params = payload.to_voice_selection_params()
    audio_config = payload.to_audio_config()

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config
    )
    return {"audio_bytes": response.audio_content, "content_type": "audio/mpeg"}
