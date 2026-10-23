import os
from model_client import get_vertex_ai_text_model
from model_models import ModelRequest, ModelResponse
import vertexai
from vertexai.preview.generative_models import HarmCategory, HarmBlockThreshold

def stream_vertex_ai_generation(project_id: str, location: str, prompt: str, model_name: str = "gemini-pro"):
    model = get_vertex_ai_text_model(project_id=project_id, location=location, model_name=model_name)
    
    # Configure safety settings for streaming
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    responses = model.generate_content(
        contents=[prompt],
        stream=True,
        safety_settings=safety_settings
    )
    
    for chunk in responses:
        # Each chunk is a GenerateContentResponse object
        # We can extract text and other metadata
        text_content = ""
        if chunk.candidates:
            for part in chunk.candidates[0].content.parts:
                if part.text:
                    text_content += part.text
        
        # Preserve the original provider response object in metadata
        yield ModelResponse(text=text_content, metadata={"provider_response_object": chunk})

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    test_prompt = "Tell me a long story about a space explorer."
    print("Streaming Vertex AI generation:")
    for response_chunk in stream_vertex_ai_generation(project_id=project_id, location=location, prompt=test_prompt):
        print(response_chunk.text, end="", flush=True)
        # Example of accessing metadata
        # if "provider_response_object" in response_chunk.metadata:
        #     print(f" (Metadata available for chunk)")
    print("
Streaming complete.")
