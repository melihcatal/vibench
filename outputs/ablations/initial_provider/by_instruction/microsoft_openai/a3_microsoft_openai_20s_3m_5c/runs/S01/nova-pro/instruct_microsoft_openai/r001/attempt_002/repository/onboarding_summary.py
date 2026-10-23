import google.generativeai as genai
genai.configure(api_key='your-gemini-api-key')

def summarize_onboarding_state(text):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f'Summarize the following onboarding state: {text}')
    return response.text