import os
from typing import List
from vision_client import get_generative_model

def check_text_for_safety(texts: List[str]):
    """Checks generated visual labels and descriptions for unsafe text using a Generative AI model."""
    model = get_generative_model('gemini-pro') # Using a text-only model for safety checks

    safety_results = {}
    for i, text in enumerate(texts):
        prompt = f"""Analyze the following text for any unsafe content (e.g., hate speech, sexually explicit, self-harm, harassment). Respond with 'SAFE' or 'UNSAFE' and a brief reason if UNSAFE.\nText: '{text}'"""
        try:
            response = model.generate_content(prompt)
            safety_results[f"text_{i}"] = {"text": text, "analysis": response.text.strip()}
        except Exception as e:
            safety_results[f"text_{i}"] = {"text": text, "analysis": f"Error during safety check: {e}"}
            
    return safety_results

if __name__ == '__main__':
    # This is a placeholder for demonstration.
    # Ensure GOOGLE_API_KEY is set.
    # example_labels = ["cat", "violence", "happy person"]
    # safety_checks = check_text_for_safety(example_labels)
    # print("Text safety checks:", safety_checks)
    pass
