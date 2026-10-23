import openai
from embeddings_client import get_openai_client
from typing import List, Tuple

def translate_query(query: str, target_language: str = "English", model: str = "gpt-3.5-turbo") -> str:
    """Translates a single query to a target language using OpenAI's chat completion model.

    Args:
        query: The query string to translate.
        target_language: The language to translate the query into (e.g., "English", "French").
        model: The OpenAI chat completion model to use for translation.

    Returns:
        The translated query string.
    """
    client = get_openai_client()

    messages = [
        {"role": "system", "content": f"You are a helpful assistant that translates text into {target_language}."},
        {"role": "user", "content": f"Translate the following query to {target_language}: '''{query}'''"}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=100
    )

    return response.choices[0].message.content.strip()

def translate_queries_batch(queries: List[str], target_language: str = "English", model: str = "gpt-3.5-turbo") -> List[str]:
    """Translates a batch of queries to a target language using OpenAI's chat completion model.

    Args:
        queries: A list of query strings to translate.
        target_language: The language to translate the queries into.
        model: The OpenAI chat completion model to use for translation.

    Returns:
        A list of translated query strings.
    """
    translated_queries = []
    for query in queries:
        translated_queries.append(translate_query(query, target_language, model))
    return translated_queries

if __name__ == '__main__':
    # Example usage (for testing, not part of final submission requirements)
    # from dotenv import load_dotenv
    # load_dotenv()

    # spanish_query = "¿Dónde está la biblioteca?"
    # translated_to_english = translate_query(spanish_query, target_language="English")
    # print(f"Original (Spanish): '{spanish_query}'")
    # print(f"Translated (English): '{translated_to_english}'")

    # french_queries = ["Bonjour le monde", "Comment allez-vous?"]
    # translated_batch = translate_queries_batch(french_queries, target_language="German")
    # print(f"\nOriginal (French): {french_queries}")
    # print(f"Translated (German): {translated_batch}")
    pass
