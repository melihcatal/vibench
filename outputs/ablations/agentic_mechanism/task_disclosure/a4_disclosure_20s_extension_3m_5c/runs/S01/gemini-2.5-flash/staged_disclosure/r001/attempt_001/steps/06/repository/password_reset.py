import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_password_reset_email(to_email, reset_link):
    """
    Starts a password reset flow by sending an email with a reset link
    using SendGrid.
    """
    message = Mail(
        from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
        to_emails=to_email,
        subject='Password Reset Request',
        html_content=f'Please click this link to reset your password: <a href="{reset_link}">{reset_link}</a>')
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(f"SendGrid email sent successfully. Status Code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending email via SendGrid: {e}")
        return False

if __name__ == "__main__":
    # Example usage (in a real application, these values would come from user input/database)
    recipient_email = "user@example.com"
    password_reset_link = "http://your-app.com/reset-password?token=some_secure_token"

    if send_password_reset_email(recipient_email, password_reset_link):
        print(f"Password reset email initiated for {recipient_email}")
    else:
        print(f"Failed to initiate password reset email for {recipient_email}")
