
import os
from google.cloud import aiplatform
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def answer_question_with_context(question: str, context: str) -> str:
    """
    Calls a hosted LLM (Google Cloud Vertex AI) to answer a question using provided context.

    Args:
        question: The question to be answered.
        context: The context to use for answering the question.

    Returns:
        The answer from the LLM.
    """
    # Initialize Vertex AI
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using `gcloud auth application-default login`
    # or specify project and location explicitly
    # aiplatform.init(project="your-gcp-project-id", location="us-central1")
    # For simplicity, assuming default authentication and location from environment/gcloud config

    # Use a specific model ID, e.g., 'gemini-pro'
    model_id = "gemini-pro"
    
    # Initialize the GenerativeModel
    model = aiplatform.preview.generative_models.GenerativeModel(model_id)

    # Construct the prompt
    prompt = f"""
    Context: {context}

    Question: {question}

    Answer:
    """

    # Generate content
    response = model.generate_content(
        contents=[prompt],
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }
    )
    
    return response.text.strip()

if __name__ == "__main__":
    # Example usage:
    # Set your GCP project ID and location before running
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"
    # aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location="us-central1")

    example_context = (
        "The capital of France is Paris. Paris is also the most populous city in France. "
        "The Eiffel Tower is a famous landmark in Paris. It was completed in 1889."
    )
    example_question = "What is the capital of France and what is a famous landmark there?"

    try:
        # Note: You need to have authenticated with Google Cloud and have access to Vertex AI
        # For example, by running `gcloud auth application-default login`
        answer = answer_question_with_context(example_question, example_context)
        print(f"Question: {example_question}")
        print(f"Answer: {answer}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have authenticated with Google Cloud and enabled the Vertex AI API.")
        print("You might need to set your GCP project ID and location, for example:")
        print("aiplatform.init(project='your-gcp-project-id', location='us-central1')")
