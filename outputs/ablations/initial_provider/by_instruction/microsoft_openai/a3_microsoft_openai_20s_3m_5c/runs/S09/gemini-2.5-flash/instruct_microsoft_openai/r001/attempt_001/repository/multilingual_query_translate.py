import openai
import os
from typing import List

def translate_query(query: str, target_language: str = "English") -> str:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    translation_prompt = f"Translate the following text to {target_language}: '{query}'"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that translates text."},
            {"role": "user", "content": translation_prompt}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def multilingual_query_translate(query: str, target_languages: List[str]) -> Dict[str, str]:
    translated_queries = {}
    for lang in target_languages:
        translated_queries[lang] = translate_query(query, lang)
    return translated_queries
