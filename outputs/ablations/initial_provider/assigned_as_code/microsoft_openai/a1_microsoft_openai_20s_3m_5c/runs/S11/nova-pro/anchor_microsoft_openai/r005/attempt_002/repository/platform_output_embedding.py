import google.generativeai as genai

def embed_platform_output(text):
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f'Embed the following text: {text}')
    return response.embedding