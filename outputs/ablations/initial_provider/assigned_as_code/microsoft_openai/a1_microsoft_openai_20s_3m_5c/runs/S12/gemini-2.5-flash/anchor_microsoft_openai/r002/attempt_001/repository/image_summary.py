import os
import google.generativeai as genai

def image_summary(payload, config=None):
    config = config or {}
    
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro')

    # Assuming payload contains analysis results from previous steps
    # For demonstration, let's construct a simple prompt based on hypothetical results
    # In a real scenario, you'd pass in the actual structured results.
    labels = payload.get('labels', [])
    description = payload.get('description', {})
    text_annotations = payload.get('text_annotations', [])
    safety_scores = payload.get('safety_scores', {})

    prompt = "Summarize the following image analysis results in a concise paragraph:\n"
    if description and description.get('text'):
        prompt += f"Description: {description['text']}.\n"
    if labels:
        prompt += f"Detected labels: {', '.join([label['name'] for label in labels])}.\n"
    if text_annotations:
        extracted_texts = [text['content'] for text in text_annotations]
        if extracted_texts:
            prompt += f"Extracted text: {'; '.join(extracted_texts)}.\n"
    
    # Add safety scores if available and relevant thresholds are met for concern
    if safety_scores:
        unsafe_categories = []
        for category, score in safety_scores.items():
            # Example threshold, adjust as needed
            if score > 0.7:  
                unsafe_categories.append(f"{category.replace('_', ' ')} with score {score:.2f}")
        if unsafe_categories:
            prompt += f"Potential safety concerns: {', '.join(unsafe_categories)}.\n"

    response = model.generate_content(prompt)
    return {'summary': response.text}
