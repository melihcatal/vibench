import os
import google.generativeai as genai

def stored_asset_summary(payload: dict) -> dict:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following text:\n\n{payload['text']}"

    response = model.generate_content(prompt)
    
    # The response might have multiple parts or candidates. We'll take the first one.
    if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
        summary_text = " ".join([part.text for part in response.candidates[0].content.parts])
        return {"summary": summary_text}
    else:
        return {"summary": "Could not generate summary."}
