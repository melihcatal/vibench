import requests
import os

# Firebase Web API Key (required for Identity Toolkit REST API)
# Store this securely, e.g., in environment variables
FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY", "YOUR_FIREBASE_WEB_API_KEY")
FIREBASE_AUTH_DOMAIN = os.environ.get("FIREBASE_AUTH_DOMAIN", "YOUR_PROJECT_ID.firebaseapp.com")

def email_password_login(email: str, password: str) -> dict:
    """
    Signs in a user with email and password using Firebase Identity Toolkit REST API
    and returns ID and refresh tokens.
    """
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    try:
        response = requests.post(rest_api_url, headers=headers, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        
        return {
            "idToken": data.get("idToken"),
            "refreshToken": data.get("refreshToken"),
            "expiresIn": data.get("expiresIn"),
            "email": data.get("email"),
            "localId": data.get("localId"),
            "message": "Login successful"
        }
    except requests.exceptions.RequestException as e:
        error_message = e.response.json().get("error", {}).get("message", str(e)) if e.response else str(e)
        return {"error": error_message}
    except Exception as e:
        return {"error": str(e)}

if __name__ == 'main':
    # Example usage (replace with actual logic)
    # Ensure FIREBASE_WEB_API_KEY is set
    # result = email_password_login("test_user@example.com", "SecurePassword123!")
    # print(result)
    pass
