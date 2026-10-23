import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import os

def summarize_onboarding_state(onboarding_data: str):
    # Initialize Vertex AI
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    # vertexai.init(project="your-gcp-project-id", location="us-central1")
    
    # For this example, assuming project and location are already configured or default.
    # Replace with your actual project and location
    vertexai.init(project="YOUR_GCP_PROJECT_ID", location="us-central1")

    model = GenerativeModel("gemini-pro")
    
    prompt = f"Summarize the following onboarding state for a support agent, highlighting any incomplete steps or potential issues: {onboarding_data}"
    
    response = model.generate_content(prompt)
    
    return response.text
