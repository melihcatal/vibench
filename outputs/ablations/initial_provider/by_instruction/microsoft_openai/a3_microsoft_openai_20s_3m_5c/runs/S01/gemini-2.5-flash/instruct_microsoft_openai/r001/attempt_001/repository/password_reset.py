import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import uuid

def password_reset(email):
    """
    Initiates a password reset flow by sending a reset email using SendGrid.
    """
    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    if not sendgrid_api_key:
        raise ValueError("SENDGRID_API_KEY environment variable not set.")

    try:
        # In a real application, a password reset token would be generated and stored
        # in a database, associated with the user's email, and have an expiry.
        reset_token = str(uuid.uuid4())
        reset_link = f"https://your-app.com/reset-password?token={reset_token}&email={email}"

        message = Mail(
            from_email='no-reply@your-app.com',
            to_emails=email,
            subject='Password Reset Request',
            html_content=f'''
            <p>You have requested a password reset for your account.</p>
            <p>Please click on the following link to reset your password:</p>
            <p><a href="{reset_link}">{reset_link}</a></p>
            <p>If you did not request this, please ignore this email.</p>
            '''
        )
        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)

        if response.status_code == 202:
            return {"success": True, "message": f"Password reset email sent to {email}."}
        else:
            return {"success": False, "message": f"Failed to send email. Status Code: {response.status_code}, Body: {response.body}"}

    except Exception as e:
        return {"success": False, "message": str(e)}
