from identity_client import okta_client
from flask import Flask, request, session, jsonify

app = Flask(__name__)

@app.route('/callback')
def callback():
    """
    Handles the OAuth callback from Okta, exchanges the code for tokens.
    """
    try:
        # The token is fetched from the Okta token endpoint
        token = okta_client.authorize_access_token()
        session['user_token'] = token
        
        # In a real app, you would likely redirect the user to a profile page
        return jsonify(token)
    except Exception as e:
        # Handle exceptions, e.g., if the user denies the consent.
        return str(e), 400

if __name__ == '__main__':
    app.run(port=5001, debug=True)
