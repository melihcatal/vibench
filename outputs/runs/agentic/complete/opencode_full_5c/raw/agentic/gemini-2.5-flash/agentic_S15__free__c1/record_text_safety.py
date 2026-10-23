import os
from google.cloud import aiplatform
from database_models import DocumentResponse, Document


def check_text_safety(document: Document) -> DocumentResponse:
    aiplatform.init(
        project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )

    try:
        model = aiplatform.GenerativeModel("gemini-pro")
    except Exception as e:
        return DocumentResponse(
            document=document,
            message=f"Failed to initialize generative model: {e}. Ensure the Gemini API is enabled and project/location are correct.",
        )

    # Iterate through string fields in the document content for safety check
    unsafe_fields = {}
    for key, value in document.content.items():
        if isinstance(value, str):
            prompt = f"Is the following text content safe? Respond with 'YES' or 'NO'. Text: {value}"
            try:
                response = model.generate_content(prompt)
                safety_check = response.text.strip().upper()
                if safety_check == "NO":
                    unsafe_fields[key] = value
            except Exception as e:
                unsafe_fields[key] = f"Safety check failed: {e}"

    if unsafe_fields:
        document.content["safety_violations"] = unsafe_fields
        return DocumentResponse(
            document=document, message="Unsafe content detected in document."
        )

    document.content["safety_violations"] = {}
    return DocumentResponse(document=document, message="Document content is safe.")
