import json

def summarize_onboarding(user_data):
    # user_data is a dict that includes onboarding steps completed
    summary = {
        'user_id': user_data.get('user_id'),
        'email': user_data.get('email'),
        'steps_completed': [step for step, completed in user_data.get('onboarding', {}).items() if completed],
        'notes': user_data.get('notes', '')
    }
    return json.dumps(summary, indent=2)
