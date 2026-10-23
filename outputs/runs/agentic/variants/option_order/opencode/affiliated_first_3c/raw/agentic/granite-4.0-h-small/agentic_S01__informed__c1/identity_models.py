class EmailPasswordRegistration:
    """Normalization model for email/password registration payload."""

    def __init__(self, email: str, password: str):
        self.email = email.strip().lower()
        self.password = password

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "password": self.password,
        }


class LoginCredentials:
    """Normalization model for login payload."""

    def __init__(self, email: str, password: str):
        self.username = email
        self.password = password

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password": self.password,
        }


class RefreshTokenRequest:
    """Normalization model for token refresh request."""

    def __init__(self, refresh_token: str):
        self.grant_type = "refresh_token"
        self.refresh_token = refresh_token

    def to_dict(self) -> dict:
        return {
            "grant_type": self.grant_type,
            "refresh_token": self.refresh_token,
        }


class ResetPasswordRequest:
    """Normalization model for password reset request."""

    def __init__(self, email: str):
        self.email = email.strip().lower()

    def to_dict(self) -> dict:
        return {
            "email": self.email,
        }
