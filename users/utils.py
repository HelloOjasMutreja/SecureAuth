from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.mail import send_mail
from django.conf import settings

signer = TimestampSigner()

def generate_token(user):
    return signer.sign(user.pk)

def verify_token(token, max_age=86400):
    try:
        user_id = signer.unsign(token, max_age=max_age)
        return user_id
    except (BadSignature, SignatureExpired):
        return None

def send_verification_email(user):
    token = generate_token(user)
    url = f"{settings.SITE_URL}/verify-email/{token}/"
    send_mail(
        subject="Verify your Email",
        message=f"Click here to verify: {url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
