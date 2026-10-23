import os
import google.generativeai as genai

def ocr_safety(text, model_name="gemini-pro"): # gemini-pro for content moderation
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name)
    
    response = model.generate_content(
        f"Analyze the following text for safety and content policy violations. Categorize any issues. Text: {text}"
    )

    # The safety_ratings are part of the candidate, not directly on the response
    safety_ratings_output = []
    for candidate in response.candidates:
        if hasattr(candidate, 'safety_ratings'):
            for rating in candidate.safety_ratings:
                safety_ratings_output.append({
                    "category": rating.category.name,
                    "probability": rating.probability.name,
                })
    
    # Also include the text output from the model if available
    model_output_text = "No content generated due to safety concerns." 
    if response.candidates and hasattr(response.candidates[0], 'content') and response.candidates[0].content.parts:
        model_output_text = response.candidates[0].content.parts[0].text

    return {"safety_analysis": model_output_text, "safety_ratings": safety_ratings_output}
