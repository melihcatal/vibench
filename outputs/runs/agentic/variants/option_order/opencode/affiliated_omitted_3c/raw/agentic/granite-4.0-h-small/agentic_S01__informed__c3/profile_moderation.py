import os
from typing import List
from identity_models import UserAttribute, NormalizedUser
from alibabacloud_green import AcsClient
from alibabacloud_green.region import RegionId
from alibabacloud_green.models import CommonRequest


def moderate_profile(user: NormalizedUser) -> NormalizedUser:
    """Moderates profile text fields for a user before activation.

    Uses Alibaba Cloud Content Moderation (Green) to scan for disallowed content.
    Returns the sanitized user object with moderated fields replaced.
    """
    # Green client configuration (region = ap-southeast-1 as example)
    green_client = AcsClient(
        access_key_id=os.getenv("ALIBABA_ACCESS_KEY_ID"),
        access_key_secret=os.getenv("ALIBABA_ACCESS_SECRET"),
        region_id=RegionId.APSouthEast1,
    )

    # Example: moderate the 'nickname' attribute if present
    moderated_user = user.copy()
    nickname_attr = next(
        (a for a in user["Attributes"] if a["Name"] == "nickname"), None
    )
    if nickname_attr:
        request = CommonRequest(
            version="2018-12-12",
            product="green",
            action="TextModeration",
            region_id=RegionId.APSouthEast1.value,
        )
        request.add_body_params("Content", nickname_attr["Value"])
        request.set_accept_format("json")
        try:
            response = green_client.do_action_with_exception(request)
            result = response.json()
            # Green returns 'risk' and possibly modified content
            if result.get("risk") == "normal":
                moderated_user["Attributes"] = [
                    a for a in user["Attributes"] if a["Name"] != "nickname"
                ]
                moderated_user["Attributes"].append(
                    {"Name": "nickname", "Value": nickname_attr["Value"]}
                )
        except Exception as e:
            # On failure, keep original text but log
            print("Profile moderation error:", e)
    return moderated_user
