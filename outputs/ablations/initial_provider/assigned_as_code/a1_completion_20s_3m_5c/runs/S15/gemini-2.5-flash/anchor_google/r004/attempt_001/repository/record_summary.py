import google.generativeai as genai

def record_summary(document_content, project_id, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following document content: {document_content}"
    response = model.generate_content(prompt)
    return {"summary": response.text}
