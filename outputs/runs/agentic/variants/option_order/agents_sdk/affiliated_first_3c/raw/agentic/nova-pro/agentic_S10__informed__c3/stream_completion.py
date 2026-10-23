import google.generativeai as genai

def stream_completion(prompt):
    genai.configure(api_key='GOOGLE_API_KEY')
    model = genai.GenerativeModel('gemini-pro')
    for chunk in model.generate_content_stream(prompt):
        yield chunk.text