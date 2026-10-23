import os
from google.cloud import aiplatform

# Initialize Vertex AI client for generative AI
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def check_corpus_safety(text: str) -> dict:
    """
    Checks the safety of corpus text before embedding using Google Cloud Vertex AI's `gemini-pro` model.
    This provides a general safety check. For more granular control, dedicated content safety APIs might be used.

    Args:
        text: The text content to check for safety.

    Returns:
        A dictionary indicating safety assessment, potentially with categories and scores.
        Note: The actual response structure depends on the generative model's safety attributes.
              This example directly uses `gemini-pro` which has built-in safety features.
    """
    model = aiplatform.GenerativeModel("gemini-pro") # Concrete model identifier

    # When using generate_content with Gemini, safety attributes are automatically checked.
    # We can craft a prompt to ask for an explicit safety assessment if needed,
    # but the API itself will often provide safety ratings in the response metadata.
    # For a direct check, we can just try to generate content and inspect safety_ratings.
    # Alternatively, for explicit review, we can ask the model:
    prompt = f"""Review the following text for any potentially unsafe content categories like hate speech, sexually explicit, harassment, or dangerous content. Provide a brief assessment.

Text:
'''
{text}
'''

Safety Assessment:
"""
    response = model.generate_content(prompt,
                                      safety_settings={
                                          # Example of enabling ALL safety settings to BLOCK responses if unsafe.
                                          # For checking, we might want to let it pass and inspect ratings.
                                          aiplatform.HarmCategory.HARM_CATEGORY_HATE_SPEECH: aiplatform.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                                          aiplatform.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: aiplatform.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                                          aiplatform.HarmCategory.HARM_CATEGORY_HARASSMENT: aiplatform.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                                          aiplatform.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: aiplatform.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                                      })

    safety_result = {"assessment": response.candidates[0].content.text.strip()}
    # The actual safety_ratings are typically found in response.prompt_feedback or candidate.safety_ratings
    # The structure might vary slightly based on SDK version and specific model.
    # This example focuses on the text assessment by the model.
    if hasattr(response.candidates[0], 'safety_ratings'):
        safety_result['api_safety_ratings'] = [
            {'category': str(s.category).split('.')[-1], 'probability': str(s.probability).split('.')[-1]}
            for s in response.candidates[0].safety_ratings
        ]
    elif hasattr(response, 'prompt_feedback') and hasattr(response.prompt_feedback, 'safety_ratings'):
         safety_result['api_safety_ratings'] = [
            {'category': str(s.category).split('.')[-1], 'probability': str(s.probability).split('.')[-1]}
            for s in response.prompt_feedback.safety_ratings
        ]

    return safety_result

if __name__ == '__main__':
    safe_text = "This is a perfectly normal and harmless sentence about science."
    unsafe_text = "I will harm you and destroy everything you love." # Example of potentially unsafe content

    print("Checking safe text:")
    safe_assessment = check_corpus_safety(safe_text)
    print(safe_assessment)

    print("\nChecking potentially unsafe text:")
    unsafe_assessment = check_corpus_safety(unsafe_text)
    print(unsafe_assessment)
