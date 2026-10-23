import firebase_admin
from firebase_admin import auth


def start_password_reset(email, config=None):
    config = config or {}
    try:
        app = firebase_admin.get_app()
    except ValueError:
        app = firebase_admin.initialize_app(options={"projectId": config["project_id"]})
    action_code_settings = auth.ActionCodeSettings(
        url="https://yourapp.com/reset_password?email=" + email,
        handle_code_in_app=True,
        ios_bundle_id="com.yourcompany.ios",
        android_package_name="com.yourcompany.android",
        dynamic_link_domain="yourapp.page.link"
    )
    auth.generate_password_reset_link(email, action_code_settings, app=app)
    return {"message": "Password reset link sent to your email."}