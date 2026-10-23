import google.generativeai as genai
import os

def check_log_text_safety(log_message: str) -> dict:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    # The Gemini API automatically includes safety attributes in its responses.
    # We are just calling the model with the log message and expecting the safety ratings.
    response = model.generate_content(log_message, 
                                      safety_settings=[
                                          {
                                              "category": "HARM_CATEGORY_HARASSMENT",
                                              "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                          },
                                          {
                                              "category": "HARM_CATEGORY_HATE_SPEECH",
                                              "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                          },
                                          {
                                              "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                              "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                          },
                                          {
                                              "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                                              "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                                          },
                                      ])
    
    # The response object contains prompt_feedback which includes safety_ratings
    safety_attributes = {
        "blocked": False,
        "categories": []
    }

    if response._chunks and response._chunks[0].safety_ratings:
        for rating in response._chunks[0].safety_ratings:
            if rating.blocked: # Check if any category was blocked
                safety_attributes["blocked"] = True
            safety_attributes["categories"].append({
                "category": rating.category.name, # Using .name to get string representation
                "probability": rating.probability.name # Using .name to get string representation
            })

    return safety_attributes
