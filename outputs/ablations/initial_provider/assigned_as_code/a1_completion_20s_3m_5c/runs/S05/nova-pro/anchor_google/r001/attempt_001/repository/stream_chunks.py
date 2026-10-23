from speech_client import get_speech_client, normalize_response
from speech_models import create_streaming_config, create_audio_content

def stream_chunks(audio_generator):
    client = get_speech_client()
    streaming_config = create_streaming_config()
    requests = (types.StreamingRecognizeRequest(audio_content=audio_chunk) for audio_chunk in audio_generator)
    response = client.streaming_recognize(streaming_config, requests)
    return normalize_response(response)