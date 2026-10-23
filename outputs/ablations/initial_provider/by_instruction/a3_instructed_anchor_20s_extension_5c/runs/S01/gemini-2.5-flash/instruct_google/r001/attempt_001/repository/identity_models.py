def create_user_request(email, password):
    """
    Helper to format user registration request payload.
    """
    return {"email": email, "password": password}

def create_user_response(uid, email, message):
    """
    Helper to format user registration response.
    """
    return {"uid": uid, "email": email, "message": message}

def login_request(email, password):
    """
    Helper to format login request payload for Firebase REST API.
    """
    return {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

def refresh_token_request(refresh_token):
    """
    Helper to format refresh token request payload for Firebase REST API.
    """
    return {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

def password_reset_request(email):
    """
    Helper to format password reset request payload for Firebase REST API.
    """
    return {
        "requestType": "PASSWORD_RESET",
        "email": email
    }
