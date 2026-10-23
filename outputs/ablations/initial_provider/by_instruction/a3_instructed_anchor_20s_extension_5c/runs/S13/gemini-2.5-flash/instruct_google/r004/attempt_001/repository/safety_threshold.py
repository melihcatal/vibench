import google.generativeai as genai
import os
from typing import Dict, Any

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def safety_threshold(moderation_result: Dict[str, Any], thresholds: Dict[str, str]) -> Dict[str, Any]:
    model = genai.GenerativeModel('gemini-pro')
    # Convert moderation_result and thresholds to a string for the model to interpret
    input_prompt = (
        f"Given the following moderation result: {moderation_result} "
        f"and the following safety thresholds: {thresholds}. "
        f"Decide if the text should be allowed based on these thresholds. "
        f"Return 'allowed': True or False, and a 'reason'."
    )

    response = model.generate_content(input_prompt)

    # Attempt to parse the model's response. This is a simplified parsing.
    # In a real scenario, more robust parsing or a structured output from the model would be beneficial.
    decision = {"allowed": True, "reason": "No explicit block from policy agent."}
    if "false" in response.text.lower():
        decision["allowed"] = False
        decision["reason"] = response.text
    elif "true" in response.text.lower():
        decision["allowed"] = True
        decision["reason"] = response.text

    return decision
