
import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.preview.generative_models import GenerativeModel

# TODO(developer): Replace the project and location with your actual values
PROJECT_ID = "your-gcp-project-id"  # e.g., "my-gcp-project"
LOCATION = "us-central1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

def stream_gemini_content(prompt: str):
    """Streams content from the Gemini model."""
    model = GenerativeModel("gemini-pro")
    responses = model.generate_content(
        contents=[prompt],
        stream=True,
    )

    print(f"Streaming response for prompt: '{prompt}'")
    for response in responses:
        print(response.text)
        # You can access other parts of the response object if needed,
        # e.g., response.candidates, response.usage_metadata, etc.
        # For example, to print the raw response object:
        # print(response)

if __name__ == "__main__":
    test_prompt = "Tell me a story about a magical cat."
    stream_gemini_content(test_prompt)
