import os
import google.generativeai as genai

def check_annotation_safety(payload):
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    
    annotation_text = payload.get('annotation_text', '')
    
    # The Generative AI API has built-in safety features. We can leverage it to check for unsafe content.
    # For a more explicit safety check, one might define a prompt that asks the model to evaluate safety.
    # For this example, we'll just send the text and assume the API's internal safety filters will flag issues.
    # The response will implicitly contain safety ratings.
    
    response = model.generate_content(annotation_text)
    
    # Extracting safety ratings from the response
    safety_attributes = []
    if hasattr(response, 'prompt_feedback') and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_attributes.append({
                'category': rating.category.name,
                'probability': rating.probability.name
            })
    
    return {'text': annotation_text, 'safety_ratings': safety_attributes}
