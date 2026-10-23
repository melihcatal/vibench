import google.generativeai as genai
genai.configure(api_key='your-gemini-api-key')

def moderate_profile_text(text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f'Moderate the following text for inappropriate content: {text}')
    return response.text