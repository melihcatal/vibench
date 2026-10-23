from translation_client import get_openai_client
from translation_models import TranslationRequest, TranslationResponse

def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = get_openai_client()
    
    messages = [
        {"role": "system", "content": "You are a helpful translation assistant."},
        {"role": "user", "content": f"Translate the following text from {request.source_language} to {request.target_language}:\n\n{request.text}"}
    ]

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Using a concrete OpenAI model
            messages=messages
        )
        translated_text = completion.choices[0].message.content.strip()
        
        # In a real scenario, you might have to infer the detected language
        # from the model's response if not explicitly provided.
        # For simplicity, we'll assume auto-detection or use the source_language if provided.
        detected_source_language = request.source_language if request.source_language != "auto" else "unknown"

        return TranslationResponse(translated_text=translated_text, detected_source_language=detected_source_language)
    except Exception as e:
        return TranslationResponse(translated_text=f"Error: {str(e)}", detected_source_language="error")
