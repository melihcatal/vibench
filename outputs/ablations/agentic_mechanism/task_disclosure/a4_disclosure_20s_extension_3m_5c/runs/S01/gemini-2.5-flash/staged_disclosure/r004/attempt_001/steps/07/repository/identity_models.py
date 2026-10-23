
# Local request, response, and normalization helpers for Email/Password Account Lifecycle.

class EmailPasswordSignUpRequest:
    """
    Represents a request to sign up a new user with email and password.
    """
    def __init__(self, email, password):
        self.email = email
        self.password = password

class EmailPasswordSignUpResponse:
    """
    Represents the response after a successful email and password sign-up.
    """
    def __init__(self, user_id, email, message="Sign-up successful"):
        self.user_id = user_id
        self.email = email
        self.message = message

class EmailPasswordNormalizeRequest:
    """
    Represents a request to normalize an email address.
    Useful for ensuring consistent email formats before storage or comparison.
    """
    def __init__(self, email):
        self.email = email
