from typing import Dict, Any

class UserRegistrationPayload:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class UserLoginPayload:
    def __init__(self, email, password):
        self.email = email
        self.password = password

class RefreshTokenPayload:
    def __init__(self, refresh_token):
        self.refresh_token = refresh_token

class PasswordResetPayload:
    def __init__(self, email):
        self.email = email

class UserProfile:
    def __init__(self, user_id, display_name, bio, locale):
        self.user_id = user_id
        self.display_name = display_name
        self.bio = bio
        self.locale = locale

class OnboardingSummary:
    def __init__(self, user_id, status, last_activity, pending_actions):
        self.user_id = user_id
        self.status = status
        self.last_activity = last_activity
        self.pending_actions = pending_actions

class ProfileNote:
    def __init__(self, user_id, note_content, created_by, created_at):
        self.user_id = user_id
        self.note_content = note_content
        self.created_by = created_by
        self.created_at = created_at
