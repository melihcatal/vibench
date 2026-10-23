from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str = "en"):
    client = OpenAI()
    return {
        "provider": "openai",
        "target_language": target_language,
        "translated_query": query,
    }
