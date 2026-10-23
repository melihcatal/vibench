from speech_client import build_audio_config, build_voice_params, get_tts_client, load_tts_config
from speech_models import normalize_ssml_payload, make_synthesis_input, response_to_dict


def synthesize_ssml(payload, config=None):
    config = load_tts_config(config)
    payload = normalize_ssml_payload(payload)
    client = get_tts_client()
    response = client.synthesize_speech(input=make_synthesis_input(payload), voice=build_voice_params(config), audio_config=build_audio_config(config))
    return response_to_dict(response)
