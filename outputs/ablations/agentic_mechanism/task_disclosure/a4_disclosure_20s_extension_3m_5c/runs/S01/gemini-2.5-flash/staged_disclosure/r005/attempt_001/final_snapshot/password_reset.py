import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_password_reset_email(to_email, reset_link):
    """
    Sends a password reset email using SendGrid.
    """
    message = Mail(
        from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
        to_emails=to_email,
        subject='Password Reset Request',
        html_content=f'Please click on the following link to reset your password: <a href="{reset_link}">{reset_link}</a>'
    )
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(f"Email sent to {to_email}. Status Code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    # Example usage (replace with actual user email and generated reset link)
    user_email = "user@example.com"
    generated_reset_link = "https://your-app.com/reset-password?token=some_secure_token"

    if send_password_reset_email(user_email, generated_reset_link):
        print("Password reset email successfully initiated.")
    else:
        print("Failed to initiate password reset email.")
