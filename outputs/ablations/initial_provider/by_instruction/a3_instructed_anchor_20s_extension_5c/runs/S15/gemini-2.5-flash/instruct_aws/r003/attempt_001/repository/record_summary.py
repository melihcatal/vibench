import os
import google.generativeai as genai

# Configure Google Cloud Vertex AI
genai.configure(api_key=os.environ.get("VERTEX_AI_API_KEY"))

def summarize_document_records(records: list[dict]):
    if not records:
        return {"status": "success", "summary": "No records to summarize."}

    model = genai.GenerativeModel('gemini-pro')
    
    # Prepare the content for summarization
    text_to_summarize = ""
    for i, record in enumerate(records):
        text_to_summarize += f"Document {i+1}:\n{record}\n\n"
    
    prompt = f"Please summarize the following document records:\n\n{text_to_summarize}"
    
    try:
        response = model.generate_content(prompt)
        return {"status": "success", "summary": response.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
