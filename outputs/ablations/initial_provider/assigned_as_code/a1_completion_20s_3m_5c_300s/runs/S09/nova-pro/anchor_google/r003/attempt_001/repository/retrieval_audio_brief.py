from embeddings_client import DirectEmbeddingsClient


def retrieval_audio_brief(search_results, config=None):
    client = DirectEmbeddingsClient(config)
    audio_brief = client.generate_audio_brief(search_results)
    return {"audio_brief": audio_brief}