import os
from openai import OpenAI
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse

def translate_markup(request: MarkupTranslationRequest) -> MarkupTranslationResponse:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4", # Using a concrete model identifier
        messages=[
            {"role": "system", "content": f"You are a highly accurate translation engine. Translate the HTML content from {request.source_language} to {request.target_language}. Preserve all HTML tags and attributes exactly as they are. Only translate the translatable text content within the tags."},
            {"role": "user", "content": request.markup_content}
        ]
    )
    
    translated_markup_content = response.choices[0].message.content
    return MarkupTranslationResponse(translated_markup_content=translated_markup_content, detected_language=request.source_language) # Assuming source for simplicity
