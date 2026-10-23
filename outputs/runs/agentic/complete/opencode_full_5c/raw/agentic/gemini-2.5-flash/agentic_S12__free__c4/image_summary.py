import google.generativeai as genai
import os

def summarize_image_analysis(analysis_results):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = "Summarize the following image analysis results:
" + str(analysis_results)
    response = model.generate_content(prompt)
    return response.text
