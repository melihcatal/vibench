class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password


class Token:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token


class PasswordResetTicket:
    def __init__(self, ticket):
        self.ticket = ticket
