class Auth0Response:
    def __init__(self, json_data):
        self.json_data = json_data

    def get_access_token(self):
        return self.json_data.get("access_token")

    def get_id_token(self):
        return self.json_data.get("id_token")

    def get_refresh_token(self):
        return self.json_data.get("refresh_token")
