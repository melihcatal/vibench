import os
from google.generativeai import GenerativeModel

model = GenerativeModel('gemini-pro')

def answer_with_context(question, context):
    response = model.generate_content([context, question])
    return response.text