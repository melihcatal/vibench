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
        html_content=f"Hello,<br><br>You have requested to reset your password. Please click on the following link to reset your password: <a href=\"{reset_link}\">{reset_link}</a><br><br>If you did not request a password reset, please ignore this email.<br><br>Regards,<br>Your Application Team"
    )
    try:
        sendgrid_client = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sendgrid_client.send(message)
        print(f"Email sent successfully to {to_email}. Status Code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    # Example usage (replace with actual user email and generated reset link)
    user_email = "user@example.com"
    generated_reset_link = "https://your-app.com/reset-password?token=some_secure_token"

    print("Attempting to send password reset email...")
    success = send_password_reset_email(user_email, generated_reset_link)
    if success:
        print(f"Password reset email initiated for {user_email}.")
    else:
        print(f"Failed to send password reset email for {user_email}. Check environment variables and network connection.")

