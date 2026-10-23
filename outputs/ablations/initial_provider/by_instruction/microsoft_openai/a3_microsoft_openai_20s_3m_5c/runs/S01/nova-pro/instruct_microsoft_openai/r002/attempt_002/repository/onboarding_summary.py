import json

def summarize_onboarding_state(onboarding_data):
    summary = {
        'steps_completed': len(onboarding_data['completed_steps']),
        'total_steps': len(onboarding_data['all_steps']),
        'progress': (len(onboarding_data['completed_steps']) / len(onboarding_data['all_steps'])) * 100
    }
    return json.dumps(summary, indent=4)