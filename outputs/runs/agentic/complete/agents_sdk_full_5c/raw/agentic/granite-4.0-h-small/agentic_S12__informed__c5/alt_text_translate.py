import os
from vision_client import VisionClient
from vision_models import normalize_description
import google.genai as genai

def alt_text_translate(image_path, target_language='es'):
    """Generates an alt-text description for an image using Google Gemini, then translates it.
    Returns the translated alt-text string.
    """
    # 1. Generate description via Gemini (same-scenario vision service)
    client = VisionClient(service='vision')
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    description = client.describe_image(Image={'Bytes': image_bytes})
    description_text = description.get('captions', [{}])[0].get('text', '')
    # 2. Translate using Google Gemini API
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(description_text, generation_config=genai.GenerationConfig(language=target_language))
    return response.text.strip()
