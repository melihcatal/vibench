import os

CLIENT_ID = os.getenv('CLIENT_ID')
AUTHORITY = os.getenv('AUTHORITY', 'https://login.microsoftonline.com/common')
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/oauth_callback')
SCOPES = os.getenv('SCOPES', 'User.Read').split(',')