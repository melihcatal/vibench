from translation_client import get_openai_client
from translation_models import TranslationRequest, TranslationResponse
import os

def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = get_openai_client()
    
    # Using gpt-3.5-turbo for translation
    # https://platform.openai.com/docs/api-reference/chat/create
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a highly accurate translation engine. Translate the following text from {request.source_language} to {request.target_language}. Respond only with the translated text."},
            {"role": "user", "content": request.text}
        ]
    )
    
    translated_text = response.choices[0].message.content.strip()
    
    # OpenAI chat completion API does not directly return detected language for the input
    # For simplicity, we are assuming the source_language is correct or can be detected by another means if needed.
    return TranslationResponse(translated_text=translated_text)

