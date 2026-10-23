import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_asset_content(project_id: str, location: str, text_content: str) -> str:
    """Summarizes content extracted from a stored asset using Google Vertex AI Gemini Pro.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region to use (e.g., "us-central1").
        text_content: The text content to summarize.

    Returns:
        A summarized string of the provided text content.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")
    
    # The prompt for summarization
    prompt = f"Summarize the following content: {text_content}"

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage (replace with your actual project ID, location, and asset content)
    # Ensure you have authenticated with gcloud before running (e.g., gcloud auth application-default login)
    
    # For demonstration, using placeholder values.
    # In a real scenario, you would extract content from a stored asset (e.g., from GCS, S3, etc.)
    # and pass it to the summarize_asset_content function.
    
    your_project_id = "YOUR_GOOGLE_CLOUD_PROJECT_ID"  # Replace with your project ID
    your_location = "us-central1"  # Replace with your desired region
    
    # Placeholder for content extracted from a stored asset
    sample_asset_content = (
        "This is a sample document about the benefits of cloud computing. "
        "Cloud computing offers many advantages, including scalability, cost-effectiveness, "
        "and increased flexibility. Users can access resources on demand and only pay "
        "for what they use, leading to significant savings. Furthermore, cloud providers "
        "handle infrastructure maintenance, allowing businesses to focus on their core "
        "competencies. Security in the cloud is also a major concern, but providers "
        "invest heavily in robust security measures. Overall, cloud computing is "
        "transforming the way businesses operate by providing efficient and reliable "
        "IT solutions."
    )
    
    if your_project_id == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
        print("Please replace 'YOUR_GOOGLE_CLOUD_PROJECT_ID' with your actual Google Cloud Project ID.")
        print("Also, ensure you have authenticated with gcloud (e.g., 'gcloud auth application-default login').")
    else:
        print(f"Summarizing content for project: {your_project_id} in {your_location}...")
        summary = summarize_asset_content(your_project_id, your_location, sample_asset_content)
        print("\n--- Summary ---")
        print(summary)
