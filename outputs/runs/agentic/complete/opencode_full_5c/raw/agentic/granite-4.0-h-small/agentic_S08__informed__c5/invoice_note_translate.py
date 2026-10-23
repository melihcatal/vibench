import os
from googleai import ChatModel
from translate import translate_text

# Watsonx.ai Granite model for translation
MODEL_ID = "watsonx-granite-v1.1-chat"
MAX_TOKENS = 200


def translate_invoice_notes(original_text: str, target_lang: str = "es"):
    model = ChatModel(model_id=MODEL_ID)
    prompt = f"Translate the following invoice note into {target_lang} while preserving all details:\n\n{original_text}"
    response = model.predict(prompt, max_tokens=MAX_TOKENS, temperature=0.2)
    return response.choices[0].message.content
