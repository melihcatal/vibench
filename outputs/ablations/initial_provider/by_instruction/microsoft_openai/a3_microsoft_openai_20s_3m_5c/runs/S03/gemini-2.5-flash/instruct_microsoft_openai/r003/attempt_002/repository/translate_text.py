import os
from openai import OpenAI
from translation_models import TranslationRequest, TranslationResponse

def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4", # Using a concrete model identifier
        messages=[
            {"role": "system", "content": f"You are a highly accurate translation engine. Translate the following text from {request.source_language} to {request.target_language}."},
            {"role": "user", "content": request.text}
        ]
    )
    
    translated_text = response.choices[0].message.content
    return TranslationResponse(translated_text=translated_text, detected_language=request.source_language) # OpenAI API doesn't directly detect, assuming source for simplicity