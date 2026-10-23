class OAuthTokenResponse:
    def __init__(self, response):
        self.access_token = response.get('access_token')
        self.refresh_token = response.get('refresh_token')
        self.id_token = response.get('id_token')
        self.expires_in = response.get('expires_in')


class UserProfile:
    def __init__(self, profile):
        self.id = profile.get('id')
        self.display_name = profile.get('displayName')
        self.mail = profile.get('mail')


def normalize_token_response(response):
    return OAuthTokenResponse(response)


def normalize_user_profile(profile):
    return UserProfile(profile)