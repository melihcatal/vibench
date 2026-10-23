import google.generativeai as genai

def summarize_text(text):
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(f"Summarize the following text: {text}")
    return response.text
