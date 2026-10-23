import google.generativeai as genai
import os
from typing import List, Dict, Any

def visual_safety_text(texts: List[str]) -> Dict[str, Any]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    safety_results = {}
    for i, text in enumerate(texts):
        prompt = f"Analyze the following text for unsafe content categories such as toxicity, harassment, hate speech, sexually explicit, and dangerous content. Indicate if it is safe or unsafe in each category: {text}"
        response = model.generate_content(prompt)
        safety_results[f"text_{i}"] = response.text

    return safety_results
