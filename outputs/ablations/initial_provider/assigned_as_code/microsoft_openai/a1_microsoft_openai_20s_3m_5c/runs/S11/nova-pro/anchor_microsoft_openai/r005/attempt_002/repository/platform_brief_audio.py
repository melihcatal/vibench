import google.generativeai as genai

def generate_spoken_briefing(text):
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f'Generate a spoken briefing from the following text: {text}')
    return response.audio