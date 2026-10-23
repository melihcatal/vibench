from translation_client import get_openai_client
from translation_models import TranslationRequest, TranslationResponse
from typing import List

def batch_translate(requests: List[TranslationRequest]) -> List[TranslationResponse]:
    client = get_openai_client()
    responses: List[TranslationResponse] = []

    for request in requests:
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
            detected_source_language = request.source_language if request.source_language != "auto" else "unknown"
            responses.append(TranslationResponse(translated_text=translated_text, detected_source_language=detected_source_language))
        except Exception as e:
            responses.append(TranslationResponse(translated_text=f"Error: {str(e)}", detected_source_language="error"))
    return responses
