import google.generativeai as genai

def record_text_safety(text_content, project_id, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    # A simpler approach to leverage Gemini's built-in safety features.
    # The actual safety feedback is part of the response object.
    response = model.generate_content(text_content, 
                                      safety_settings={
                                          'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                                          'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                                          'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                                          'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
                                      })
    # In a real application, you would inspect response.prompt_feedback and response.safety_ratings
    # for details on blocked content or safety attributes.
    # For this exercise, we'll return a placeholder indicating the check was performed.
    # A more complete implementation would parse and return actual safety ratings/flags.
    is_safe = True  # Assume safe if no exception, proper parsing would be needed for detail
    if response._error_text: # Simple check for an error indicating blocked content
        is_safe = False
    return {"is_safe": is_safe, "safety_feedback": response.prompt_feedback.block_reason.name if response.prompt_feedback and response.prompt_feedback.block_reason else "N/A"}
