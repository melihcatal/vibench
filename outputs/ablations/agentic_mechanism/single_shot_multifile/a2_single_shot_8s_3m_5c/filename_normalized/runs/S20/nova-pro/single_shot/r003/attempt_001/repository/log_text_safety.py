import os
import perspective

perspective.api_key = os.getenv('PERSPECTIVE_API_KEY')

def check_safety(text):
    response = perspective.analyze(text, attributes=['TOXICITY'])
    return response.attribute_scores['TOXICITY'].summary_score.value

log_text = 'This is a safe log message.'
print(check_safety(log_text))