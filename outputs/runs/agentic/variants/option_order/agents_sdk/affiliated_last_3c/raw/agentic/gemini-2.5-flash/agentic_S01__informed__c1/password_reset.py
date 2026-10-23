import os
import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_AUTH_CLIENT_ID = os.getenv("AUTH0_AUTH_CLIENT_ID") # Auth API client ID

def password_reset(email):
    url = f"https://{{AUTH0_DOMAIN}}/dbconnections/change_password"
    headers = {"Content-Type": "application/json"}
    payload = {
        "client_id": AUTH0_AUTH_CLIENT_ID,
        "email": email,
        "connection": "Username-Password-Authentication" # Use your database connection name
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        # Auth0's change_password endpoint returns a simple success message, no JSON by default
        return {"message": "Password reset email sent successfully.", "status_code": response.status_code}
    except requests.exceptions.RequestException as e:
        error_message = str(e)
        if e.response and e.response.content: # Check if response content exists
            try:
                error_details = e.response.json()
                error_message = error_details.get("error_description", error_details.get("message", error_message))
            except requests.exceptions.JSONDecodeError:
                error_message = e.response.text # Fallback to raw text if not JSON
        return {"error": error_message, "status_code": e.response.status_code if e.response else None}

if __name__ == '__main__':
    # Example usage (requires AUTH0_DOMAIN, AUTH0_AUTH_CLIENT_ID environment variables)
    # print(password_reset("test_user@example.com"))
    pass
