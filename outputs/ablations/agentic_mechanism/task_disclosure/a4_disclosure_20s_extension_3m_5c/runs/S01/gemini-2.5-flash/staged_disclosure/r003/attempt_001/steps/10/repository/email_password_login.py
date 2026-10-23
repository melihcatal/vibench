import requests
import json

def sign_in_with_email_password(email, password, api_key):
    """
    Signs in a user with email and password using Firebase Authentication REST API
    and returns authentication tokens.
    """
    REST_API_ENDPOINT = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=" + api_key
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": True
    })

    try:
        response = requests.post(REST_API_ENDPOINT, headers=headers, data=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except requests.exceptions.ConnectionError as err:
        print(f"Error connecting to Firebase: {err}")
        return None
    except requests.exceptions.Timeout as err:
        print(f"Request timed out: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")
        return None

if __name__ == "__main__":
    # Replace with your Firebase project's API key
    # You can find this in your Firebase project settings under "Web API Key"
    FIREBASE_API_KEY = "YOUR_FIREBASE_API_KEY"

    # Replace with the user's email and password
    USER_EMAIL = "user@example.com"
    USER_PASSWORD = "your_password"

    if FIREBASE_API_KEY == "YOUR_FIREBASE_API_KEY":
        print("Please replace 'YOUR_FIREBASE_API_KEY' with your actual Firebase API key.")
    elif USER_EMAIL == "user@example.com" or USER_PASSWORD == "your_password":
        print("Please replace 'user@example.com' and 'your_password' with actual user credentials.")
    else:
        print(f"Attempting to sign in user: {USER_EMAIL}")
        tokens = sign_in_with_email_password(USER_EMAIL, USER_PASSWORD, FIREBASE_API_KEY)

        if tokens:
            print("Sign-in successful!")
            print(f"ID Token: {tokens.get('idToken')}")
            print(f"Refresh Token: {tokens.get('refreshToken')}")
            # Other tokens/information available in the 'tokens' dictionary
        else:
            print("Sign-in failed.")
