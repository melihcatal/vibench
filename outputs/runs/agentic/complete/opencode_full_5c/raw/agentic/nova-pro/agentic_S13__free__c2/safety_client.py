import os
import requests

# Configuration for AWS Comprehend
AWS_COMPREHEND_ENDPOINT = "comprehend.us-west-2.amazonaws.com"
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
