class OAuthCallbackModel:
    def __init__(self, code):
        self.code = code

class ProfileClaimsModel:
    def __init__(self, access_token):
        self.access_token = access_token