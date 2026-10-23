import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_password_reset_email(to_email, reset_link):
    """
    Sends a password reset email using SendGrid.
    """
    message = Mail(
        from_email=os.environ.get("SENDGRID_SENDER_EMAIL"),
        to_emails=to_email,
        subject="Password Reset Request",
        html_content=f'''
        <p>You have requested a password reset. Click the link below to reset your password:</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <p>If you did not request this, please ignore this email.</p>
        '''
    )
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sendgrid_client.send(message)
        print(f"SendGrid Status Code: {response.status_code}")
        print(f"SendGrid Response Body: {response.body}")
        print(f"SendGrid Response Headers: {response.headers}")
        return True
    except Exception as e:
        print(f"Error sending email via SendGrid: {e}")
        return False

if __name__ == "__main__":
    # Example usage (replace with actual values in a real application)
    recipient_email = "user@example.com"
    password_reset_link = "https://your-app.com/reset-password?token=some_secure_token"

    # Ensure to set SENDGRID_API_KEY and SENDGRID_SENDER_EMAIL environment variables
    # e.g., export SENDGRID_API_KEY='YOUR_SENDGRID_API_KEY'
    # e.g., export SENDGRID_SENDER_EMAIL='your_verified_sender@example.com'

    if os.environ.get("SENDGRID_API_KEY") and os.environ.get("SENDGRID_SENDER_EMAIL"):
        print(f"Attempting to send password reset email to {recipient_email}...")
        success = send_password_reset_email(recipient_email, password_reset_link)
        if success:
            print("Password reset email sent successfully (simulated).")
        else:
            print("Failed to send password reset email.")
    else:
        print("Please set SENDGRID_API_KEY and SENDGRID_SENDER_EMAIL environment variables.")
        print("Install sendgrid with: pip install sendgrid")
