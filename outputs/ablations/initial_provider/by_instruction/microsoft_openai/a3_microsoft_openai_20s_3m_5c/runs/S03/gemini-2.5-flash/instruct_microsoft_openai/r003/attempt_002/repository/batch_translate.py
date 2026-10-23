import os
from openai import OpenAI
from typing import List
from translation_models import BatchTranslationRequest, BatchTranslationResponse

def batch_translate(request: BatchTranslationRequest) -> BatchTranslationResponse:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    translated_texts = []
    detected_languages = []

    for text in request.texts:
        response = client.chat.completions.create(
            model="gpt-4", # Using a concrete model identifier
            messages=[
                {"role": "system", "content": f"You are a highly accurate translation engine. Translate the following text from {request.source_language} to {request.target_language}."},
                {"role": "user", "content": text}
            ]
        )
        translated_texts.append(response.choices[0].message.content)
        detected_languages.append(request.source_language) # Assuming source for simplicity
    
    return BatchTranslationResponse(translated_texts=translated_texts, detected_languages=detected_languages)
