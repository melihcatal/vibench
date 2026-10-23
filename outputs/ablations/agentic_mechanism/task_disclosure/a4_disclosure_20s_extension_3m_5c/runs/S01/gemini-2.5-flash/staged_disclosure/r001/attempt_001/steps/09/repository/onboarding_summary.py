import requests

class AcmeOnboardingClient:
    BASE_URL = "https://api.acmeonboarding.com/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_onboarding_status(self, user_id: str) -> dict:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(f"{self.BASE_URL}/users/{user_id}/onboarding", headers=headers)
        response.raise_for_status()
        return response.json()

def summarize_onboarding_state(user_id: str, api_key: str) -> str:
    client = AcmeOnboardingClient(api_key)
    try:
        status_data = client.get_onboarding_status(user_id)
        summary = f"Onboarding Summary for User {user_id}:
"
        summary += f"  Status: {status_data.get('status', 'N/A')}
"
        summary += f"  Last Step Completed: {status_data.get('last_step', 'N/A')}
"
        summary += f"  Progress: {status_data.get('progress_percentage', 0)}%
"
        summary += f"  Pending Actions: {', '.join(status_data.get('pending_actions', ['None']))}
"
        return summary
    except requests.exceptions.RequestException as e:
        return f"Error fetching onboarding status for user {user_id}: {e}"

