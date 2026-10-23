from.embeddings_client import get_text_analytics_client

def retrieval_audio_brief(search_results):
    client = get_text_analytics_client()
    audio_brief = client.generate_audio_brief(search_results)
    return audio_brief

if __name__ == '__main__':
    print(retrieval_audio_brief(['Result 1', 'Result 2']))