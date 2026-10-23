import os
from typing import List, Dict, Any
from google import genai

def check_corpus_safety(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, Any]:
    config = config or {}
    texts_to_check = payload.get("texts", [])

    if not texts_to_check:
        raise ValueError("Payload must contain a 'texts' key with a list of strings.")

    api_key = config.get("api_key") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API Key not found. Please set GOOGLE_API_KEY environment variable or pass it directly.")

    model_name = "gemini-pro" # Using a generative model to check safety

    safety_results = []

    with genai.Client(api_key=api_key) as client:
        model = client.models.get(model_name)
        
        for text in texts_to_check:
            try:
                # Generate content, even if it's just the input text, to get safety feedback
                response = model.generate_content(text)
                
                # Check for safety attributes in the prompt_feedback or content_feedback
                # The genai library automatically includes safety ratings in the response
                # If the content is blocked, prompt_feedback will have a block_reason
                is_safe = True
                block_reason = None
                if response.prompt_feedback and response.prompt_feedback.block_reason:
                    is_safe = False
                    block_reason = str(response.prompt_feedback.block_reason)
                
                safety_results.append({"text": text, "is_safe": is_safe, "block_reason": block_reason})

            except Exception as e:
                safety_results.append({"text": text, "is_safe": False, "error": str(e)})

    return {"safety_checks": safety_results}
