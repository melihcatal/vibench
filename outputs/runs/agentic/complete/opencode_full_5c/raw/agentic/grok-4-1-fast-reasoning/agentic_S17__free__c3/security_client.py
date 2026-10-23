import os
import base64

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_KMS_KEY_ID = os.getenv("AWS_KMS_KEY_ID")
AWS_KMS_SIGN_KEY_ID = os.getenv("AWS_KMS_SIGN_KEY_ID")
