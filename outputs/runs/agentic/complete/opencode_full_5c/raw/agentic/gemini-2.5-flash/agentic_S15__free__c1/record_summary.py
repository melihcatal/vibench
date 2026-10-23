import os
from google.cloud import aiplatform
from database_models import DocumentResponse, Document


def summarize_record(document: Document) -> DocumentResponse:
    aiplatform.init(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )

    # Using a specific model for text generation - e.g., gemini-pro
    # Ensure to enable the Gemini API in your Google Cloud project
    # and have sufficient permissions.
    try:
        model = aiplatform.GenerativeModel("gemini-pro")
    except Exception as e:
        return DocumentResponse(
            document=document,
            message=f"Failed to initialize generative model: {e}. Ensure the Gemini API is enabled and project/location are correct.",
        )

    text_content = str(document.content)
    prompt = f"Summarize the following document content: {text_content}"

    try:
        response = model.generate_content(prompt)
        summary = response.text
        # For simplicity, we'll store the summary in the content dictionary
        # In a real scenario, you might have a dedicated field for summaries
        document.content["summary"] = summary
        return DocumentResponse(
            document=document, message="Document summarized successfully."
        )
    except Exception as e:
        return DocumentResponse(
            document=document,
            message=f"Failed to summarize document with Google Cloud Generative AI: {e}",
        )
