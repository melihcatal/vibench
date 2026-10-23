from google.cloud import aiplatform
from typing import Dict, Any, List

def summarize_moderation_decisions(moderation_results: List[Dict[str, Any]], original_text: str) -> Dict[str, Any]:
    aiplatform.init(project="YOUR_GOOGLE_CLOUD_PROJECT", location="us-central1")

    model_name = "gemini-pro"
    model = aiplatform.PreviewModel.from_pretrained(model_name)

    prompt = f"""Summarize the moderation decisions for the following text. Highlight any issues found and the overall decision (e.g., allowed, blocked).

Original Text: """{original_text}"""

Moderation Results:
"""{moderation_results}"""

Summary:"""

    try:
        response = model.predict(prompt)
        summary_text = response.text.strip()

        return {
            "summary": summary_text,
            "provider": "Google Vertex AI (Gemini Pro)"
        }
    except Exception as e:
        return {
            "error": str(e),
            "provider": "Google Vertex AI (Gemini Pro)"
        }

