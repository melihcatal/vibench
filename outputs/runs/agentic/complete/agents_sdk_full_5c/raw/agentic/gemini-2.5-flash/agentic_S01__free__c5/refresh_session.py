import requests
import os

# Firebase Web API Key is NOT directly used for token refresh, but a project ID is typically needed
# The refresh token itself is exchanged with Google's Secure Token Service (STS)
# No direct 'Web API Key' for this endpoint, it's generally tied to the project.

def refresh_session(refresh_token: str) -> dict:
    """
    Refreshes an expired session or access token using the Firebase refresh token.
    This directly interacts with Google's Secure Token Service (STS).
    """
    sts_api_url = "https://securetoken.googleapis.com/v1/token"
    
    # The client ID is usually the Firebase Web API Key or implicitly derived.
    # For this specific endpoint, we typically send it as an API key query param.
    # Let's assume FIREBASE_WEB_API_KEY is the API key associated with the project
    # as required by the STS for public clients.
    FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY", "YOUR_FIREBASE_WEB_API_KEY")
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    
    try:
        # The API Key needs to be part of the URL for this specific endpoint
        response = requests.post(f"{sts_api_url}?key={FIREBASE_WEB_API_KEY}", headers=headers, data=payload)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        
        # The response structure differs slightly from sign-in
        return {
            "idToken": data.get("id_token"),
            "refreshToken": data.get("refresh_token"), # A new refresh token might be returned
            "expiresIn": data.get("expires_in"),
            "tokenType": data.get("token_type"),
            "user_id": data.get("user_id"),
            "project_id": data.get("project_id"),
            "message": "Session refreshed successfully"
        }
    except requests.exceptions.RequestException as e:
        error_message = e.response.json().get("error", {}).get("message", str(e)) if e.response else str(e)
        return {"error": error_message}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (replace with actual logic)
    # refresh_token = "your_refresh_token_here"
    # result = refresh_session(refresh_token)
    # print(result)
    pass
