def summarize_onboarding_state(user_id, onboarding_steps):
    # Example summary: concatenate onboarding steps
    summary = f'User {user_id} has completed the following onboarding steps: ' + ', '.join(onboarding_steps)
    return summary