import os

TISANE_API_KEY = os.getenv("TISANE_API_KEY")

import requests

headers = {"Authorization": f"Bearer {TISANE_API_KEY}"}
