from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking


@shared_task
def send_booking_confirmation_email(booking_id):
    """
    Send a booking confirmation email to the guest.
    This task is executed asynchronously using Celery.
    """
    try:
        booking = Booking.objects.get(id=booking_id)
        subject = f'Booking Confirmation - {booking.listing.name}'
        message = f"""
        Dear {booking.guest_name},

        Your booking has been confirmed!

        Booking Details:
        - Listing: {booking.listing.name}
        - Location: {booking.listing.location}
        - Check-in: {booking.check_in}
        - Check-out: {booking.check_out}
        - Price per night: ${booking.listing.price_per_night}

        Thank you for choosing ALX Travel App!

        Best regards,
        ALX Travel Team
        """

        recipient_email = f"{booking.guest_name.lower().replace(' ', '.')}@example.com"

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )

        return f"Email sent successfully to {recipient_email}"

    except Booking.DoesNotExist:
        return f"Booking with ID {booking_id} not found"
    except Exception as e:
        return f"Error sending email: {str(e)}"
