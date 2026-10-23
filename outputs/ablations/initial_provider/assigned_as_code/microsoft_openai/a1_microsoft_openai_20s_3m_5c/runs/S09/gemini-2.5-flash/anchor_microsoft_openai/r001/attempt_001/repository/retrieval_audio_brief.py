from embeddings_client import EmbeddingsClient
from embeddings_models import TTS_MODEL

def retrieval_audio_brief(payload, config=None):
    client = EmbeddingsClient(api_key=config.get('api_key') if config else None).get_client()

    text_to_speak = payload['brief_text']
    output_filepath = payload.get('output_filepath', 'audio_brief.mp3')
    voice = payload.get('voice', 'alloy') # 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'

    response = client.audio.speech.create(
        model=TTS_MODEL,
        voice=voice,
        input=text_to_speak,
    )
    response.stream_to_file(output_filepath)
    
    return {'audio_filepath': output_filepath}
