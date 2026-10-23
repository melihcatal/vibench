from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str):
    client = OpenAI(api_key=None)
    return {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "query": query,
        "target_language": target_language,
        "client": type(client).__name__,
    }
