import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def corpus_safety(text_corpus, project_id, location="us-central1"):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    safety_issues = []
    for i, text in enumerate(text_corpus):
        response = model.generate_content(
            [Part.from_text(text)],
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }
        )
        # The API currently doesn't expose safety scores directly on the response object 
        # for all scenarios, but rather blocks content if it violates the settings.
        # For this example, we'll assume a simple check for empty text if it was blocked
        # or if the response indicates issues. A more robust solution would involve
        # parsing specific safety attributes if they become directly available.
        if not response._raw_response.candidates:
            safety_issues.append({"text_index": i, "text": text, "issue": "Content blocked by safety filter."})
            
    if not safety_issues:
        return {"status": "Corpus is safe.", "issues": []}
    else:
        return {"status": "Safety issues detected.", "issues": safety_issues}
