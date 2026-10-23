import google.generativeai as genai
genai.configure(api_key='your-gemini-api-key')

def translate_onboarding_copy(text, target_language):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f'Translate the following text to {target_language}: {text}')
    return response.text