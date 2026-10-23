from google.generativeai import GenerativeModel

model = GenerativeModel('gemini-pro')

def moderation_summary(text):
    response = model.generate_content(text)
    return response.text
