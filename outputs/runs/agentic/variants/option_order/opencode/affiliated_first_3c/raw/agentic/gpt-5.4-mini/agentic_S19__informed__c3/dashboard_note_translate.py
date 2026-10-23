from google import genai


def dashboard_note_translate(text: str, target_locale: str, model: str = 'gemini-2.0-flash') -> str:
    client = genai.Client()
    response = client.models.generate_content(model=model, contents=f'Translate to {target_locale}: {text}')
    return response.text or ''
