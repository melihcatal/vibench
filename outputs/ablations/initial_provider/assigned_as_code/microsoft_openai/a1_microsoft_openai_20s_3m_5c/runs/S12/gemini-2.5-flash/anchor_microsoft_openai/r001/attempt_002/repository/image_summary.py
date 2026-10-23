import google.generativeai as genai

def image_summary(analysis_results, config=None):
    config = config or {}
    genai.configure(api_key=config['gemini_api_key'])
    model = genai.GenerativeModel('gemini-pro')

    prompt = """Summarize the following image analysis results:
Labels: {}
Description: {}
Detected Text: {}
Safety Scores (Adult: {}, Racy: {}, Gory: {}, Violence: {}):
""".format(
        ", ".join([label['name'] for label in analysis_results['labels']]),
        analysis_results['description'],
        analysis_results['text_content'],
        analysis_results['safety_scores']['adult']['is_adult_content'],
        analysis_results['safety_scores']['adult']['is_racy_content'],
        analysis_results['safety_scores']['adult']['is_gory_content'],
        analysis_results['safety_scores']['violence']['has_violence']
    )

    response = model.generate_content(prompt)
    return {'summary': response.text}
