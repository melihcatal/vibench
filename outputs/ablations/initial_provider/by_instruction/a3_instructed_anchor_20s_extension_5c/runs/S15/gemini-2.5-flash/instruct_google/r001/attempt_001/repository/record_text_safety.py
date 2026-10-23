import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.generative_models import HarmCategory, HarmBlockThreshold

def check_text_safety(text_content: str):
    vertexai.init(project="your-gcp-project-id", location="us-central1") # Replace with your GCP project ID
    model = TextGenerationModel.from_pretrained("text-bison") # Using a generative model for safety check

    # Although text-bison does not have direct safety attributes like gemini-pro,
    # we can simulate a safety check by asking the model to identify unsafe content.
    # For real safety, Google's Generative AI models often have built-in safety filters
    # that would block content directly, or you'd use a dedicated safety API if available.
    # This is a conceptual implementation for the purpose of the exercise.

    prompt = f"Analyze the following text for any unsafe content, such as hate speech, sexual content, harmful content, or harassment. Respond with 'safe' if no unsafe content is found, otherwise describe the unsafe content: {text_content}"

    response = model.predict(
        prompt=prompt,
        temperature=0.1,
        max_output_tokens=100,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
    )

    # A simplistic interpretation of the response for this exercise.
    # In a real scenario, you would parse the safety_attributes from the response if the model supported it explicitly,
    # or use a dedicated content moderation API.
    if "safe" in response.text.lower() and "unsafe" not in response.text.lower():
        return {"status": "success", "safety_status": "safe", "details": response.text}
    else:
        return {"status": "success", "safety_status": "unsafe", "details": response.text}
