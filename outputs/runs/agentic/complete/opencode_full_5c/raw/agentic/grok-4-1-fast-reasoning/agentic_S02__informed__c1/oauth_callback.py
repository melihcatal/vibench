import sys
import urllib.parse
from identity_client import exchange_code
from identity_models import TokenResponse

if __name__ == "__main__":
    callback_url = (
        sys.argv[1] if len(sys.argv) > 1 else input("Paste the full callback URL: ")
    )
    parsed = urllib.parse.urlparse(callback_url)
    params = urllib.parse.parse_qs(parsed.query)
    code = params.get("code", [None])[0]
    state = params.get("state", [None])[0]
    if not code:
        print("No authorization code in callback.")
        sys.exit(1)
    print(f"State from callback: {state}")
    verifier = input("Enter PKCE code_verifier (leave empty if not PKCE): ").strip()
    verifier = verifier if verifier else None
    tokens: TokenResponse = exchange_code(code, verifier)
    print("Received tokens:")
    print(tokens)
