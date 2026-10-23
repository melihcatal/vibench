import os
import google.generativeai as genai

def summarize_audit_events(audit_events_text):
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"Summarize the following federated login audit events:\n\n{audit_events_text}\n\nProvide a concise summary of key activities and any anomalies."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing audit events with Google Generative AI: {e}")
        return None
