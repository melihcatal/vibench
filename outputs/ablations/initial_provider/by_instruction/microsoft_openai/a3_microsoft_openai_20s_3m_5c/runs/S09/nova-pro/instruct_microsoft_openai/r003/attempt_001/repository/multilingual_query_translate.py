from.embeddings_client import get_text_analytics_client

def multilingual_query_translate(query, target_language):
    client = get_text_analytics_client()
    translated_query = client.translate_query(query, target_language)
    return translated_query

if __name__ == '__main__':
    print(multilingual_query_translate('Hello, world!', 'es'))