import os
import json
from openai import OpenAI
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse

def translate_dictionary_values(request: DictionaryTranslationRequest) -> DictionaryTranslationResponse:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Convert dictionary to a string for the model
    dict_as_string = json.dumps(request.dictionary)

    response = client.chat.completions.create(
        model="gpt-4", # Using a concrete model identifier
        messages=[
            {"role": "system", "content": f"You are a highly accurate translation engine. Translate only the values of the provided JSON object from {request.source_language} to {request.target_language}. Preserve all keys exactly as they are. Respond with the translated JSON object."},
            {"role": "user", "content": dict_as_string}
        ]
    )
    
    translated_dict_as_string = response.choices[0].message.content
    
    # Attempt to parse the response back into a dictionary
    try:
        translated_dictionary = json.loads(translated_dict_as_string)
    except json.JSONDecodeError:
        # Fallback if the model doesn't return perfect JSON, try to extract values if possible
        # For simplicity, we'll raise an error here, but in a real scenario, more robust parsing might be needed.
        raise ValueError("OpenAI model did not return a valid JSON object for dictionary translation.")

    return DictionaryTranslationResponse(translated_dictionary=translated_dictionary, detected_language=request.source_language) # Assuming source for simplicity
