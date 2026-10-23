def summarize_onboarding_state(user_id, onboarding_steps):
    completed_steps = [step for step in onboarding_steps if step['completed']]
    incomplete_steps = [step for step in onboarding_steps if not step['completed']]
    summary = {
        "user_id": user_id,
        "completed_steps": completed_steps,
        "incomplete_steps": incomplete_steps
    }
    return summary