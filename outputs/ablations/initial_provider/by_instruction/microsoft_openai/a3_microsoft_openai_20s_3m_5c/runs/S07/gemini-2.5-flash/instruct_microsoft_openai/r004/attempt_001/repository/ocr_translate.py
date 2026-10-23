from document_client import get_translator_client

def translate_text(text: str, target_language: str = "en") -> str:
    client = get_translator_client()
    
    # The translate method expects a list of InputTextItem
    from azure.ai.translation.text.models import InputTextItem
    request_body = [InputTextItem(text=text)]
    
    response = client.translate(content=request_body, to=[target_language])
    
    translated_text = ""
    if response and response[0].translations:
        translated_text = response[0].translations[0].text
        
    return translated_text
