import vertexai
from vertexai.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold

def check_unsafe_content(text: str) -> dict:
    """
    Checks the input text for unsafe content using Google Cloud Vertex AI's Generative Model.

    Args:
        text: The text extracted from a document to be checked.

    Returns:
        A dictionary containing the safety ratings.
    """
    vertexai.init(project="YOUR_PROJECT_ID", location="YOUR_REGION")
    model = GenerativeModel("gemini-pro")

    response = model.generate_content(
        [text],
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        stream=False
    )

    safety_ratings = {}
    if hasattr(response, 'candidates') and response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, 'safety_ratings'):
                for rating in candidate.safety_ratings:
                    safety_ratings[rating.category.name] = rating.probability.name
    return safety_ratings

if __name__ == "__main__":
    # Example usage (replace with actual OCR extracted text)
    document_text = "This is an example document text that might contain some problematic content."
    
    # NOTE: Replace "YOUR_PROJECT_ID" and "YOUR_REGION" with your actual Google Cloud project ID and region.
    # e.g., "my-gcp-project", "us-central1"

    safety_report = check_unsafe_content(document_text)
    print("Safety Report:", safety_report)
