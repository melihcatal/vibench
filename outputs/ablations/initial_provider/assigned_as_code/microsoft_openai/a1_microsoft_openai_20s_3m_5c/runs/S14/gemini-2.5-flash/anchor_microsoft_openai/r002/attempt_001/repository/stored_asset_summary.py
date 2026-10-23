from google.cloud import aiplatform
from storage_models import StoredAssetSummaryRequest

def stored_asset_summary(request: StoredAssetSummaryRequest):
    # Initialize Vertex AI
    # Make sure to set GOOGLE_CLOUD_PROJECT environment variable or configure application default credentials.
    # For simplicity, we assume the project is configured via environment variables or gcloud login.
    # A specific model ID for summarization, e.g., 'gemini-pro' or a text-bison model.
    # Replace with an appropriate model ID available in your region.
    # Using a common model like 'gemini-pro' as an example.
    
    aiplatform.init(project="YOUR_GCP_PROJECT_ID", location="us-central1") # Replace YOUR_GCP_PROJECT_ID with actual project ID

    # Load the model
    model = aiplatform.GenerativeModel('gemini-pro') # Using gemini-pro for summarization

    # Generate content
    prompt = f"Summarize the following text:\n\n{request.text_content}"
    response = model.generate_content(prompt)

    summary_text = response.candidates[0].content.parts[0].text

    return {
        "original_text_preview": request.text_content[:200] + "..." if len(request.text_content) > 200 else request.text_content,
        "summary": summary_text
    }
