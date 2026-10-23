import google.generativeai as genai

def visual_safety_text(text_to_check, config=None):
    config = config or {}
    genai.configure(api_key=config['gemini_api_key'])
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Analyze the following text for any unsafe, inappropriate, or policy-violating content. 
Return 'True' if unsafe, 'False' otherwise. Provide a brief reason if True.
Text: """{text_to_check}"""
"""

    response = model.generate_content(prompt)
    # Assuming the model returns a simple True/False and a reason if True
    # Further parsing might be needed depending on actual model output format.
    return {'safety_analysis': response.text}
