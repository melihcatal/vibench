from google.cloud import aiplatform
import os

def summarize_records(document_records: list[str]) -> str:
    """
    Summarizes a list of document records using Google Cloud's Generative AI.
    """
    # Initialize Vertex AI client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using `gcloud auth application-default login`
    aiplatform.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location="us-central1")

    # Use the GenerativeModel class for text generation
    # The concrete provider is Google Cloud and the model family is identifiable.
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    combined_text = "\n\n".join(document_records)
    prompt = f"Please summarize the following document records:\n\n{combined_text}"

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example Usage
    records = [
        "Record 1: This is the first document record. It talks about AI and machine learning.",
        "Record 2: The second record discusses cloud computing and its benefits.",
        "Record 3: This last record focuses on data science and big data analytics."
    ]
    summary = summarize_records(records)
    print("Summary:")
    print(summary)
