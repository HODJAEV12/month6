from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

User = get_user_model()


@shared_task
def send_welcome_email_task(email: str, username: str = ""):
    subject = "Добро пожаловать!"
    message = f"Привет, {username or email}! Регистрация прошла успешно."
    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )
    return f"Приветственное письмо отправлено на {email}"


@shared_task
def clean_inactive_users_task(days: int = 30):
    cutoff = timezone.now() - timedelta(days=days)
    inactive_users = User.objects.filter(
        is_active=False,
        date_joined__lt=cutoff,
    )
    count, _ = inactive_users.delete()
    return f"Удалено неактивных пользователей: {count}"


@shared_task
def send_daily_admin_report_task():
    roles = ["ADMIN", "MODERATOR", "USER"]
    stats = {role: User.objects.filter(role=role).count() for role in roles}
    print(
        f"Отчёт по ролям пользователей: "
        f"ADMIN={stats['ADMIN']}, MODERATOR={stats['MODERATOR']}, USER={stats['USER']}"
    )
    return stats