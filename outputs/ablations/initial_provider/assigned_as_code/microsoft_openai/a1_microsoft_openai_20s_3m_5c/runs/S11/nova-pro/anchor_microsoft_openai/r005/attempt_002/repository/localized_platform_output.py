import google.generativeai as genai

def translate_platform_output(text, target_language):
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f'Translate the following text to {target_language}: {text}')
    return response.text