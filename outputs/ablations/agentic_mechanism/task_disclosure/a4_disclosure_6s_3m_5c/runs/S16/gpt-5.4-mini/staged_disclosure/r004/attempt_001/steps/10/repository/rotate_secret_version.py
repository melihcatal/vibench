import os
import sys
import json
import argparse
import urllib.parse
import urllib.request
import urllib.error


def _env(name, default=None, required=False):
    value = os.getenv(name, default)
    if required and not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def read_secret_version(secret_name, version_name=None, staged=None):
    project_id = _env("GOOGLE_CLOUD_PROJECT", required=True)
    access_token = _env("GOOGLE_OAUTH_ACCESS_TOKEN", required=True)
    base = f"https://secretmanager.googleapis.com/v1/projects/{urllib.parse.quote(project_id, safe='')}/secrets/{urllib.parse.quote(secret_name, safe='')}"
    if staged:
        url = f"{base}/versions/{urllib.parse.quote(staged, safe='')}:access"
    elif version_name:
        url = f"{base}/versions/{urllib.parse.quote(version_name, safe='')}:access"
    else:
        url = f"{base}/versions/latest:access"
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(body or str(e))
    data = payload.get("payload", {}).get("data", "")
    if not data:
        return ""
    return urllib.parse.unquote(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("secret_name")
    parser.add_argument("--version", dest="version_name")
    parser.add_argument("--staged", choices=["latest", "disabled", "destroyed"])
    args = parser.parse_args()
    value = read_secret_version(args.secret_name, version_name=args.version_name, staged=args.staged)
    sys.stdout.write(value)


if __name__ == "__main__":
    main()
