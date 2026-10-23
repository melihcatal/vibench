import json


def onboarding_summary(onboarding_data):
    summary = {
        "steps_completed": onboarding_data.get("steps_completed", []),
        "current_step": onboarding_data.get("current_step", ""),
    }
    return json.dumps(summary, indent=2)
