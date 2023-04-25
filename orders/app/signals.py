from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal
from django.conf import settings
from django_rest_passwordreset.signals import reset_password_token_created
from celery import shared_task
from .models import ConfirmEmailToken, User

# new_user_registered = Signal(
#     providing_args=['user_id'],
# )
#
# new_order = Signal(
#     providing_args=['user_id'],
# )


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, **kwargs):
    """
    Отправляем письмо с токеном для сброса пароля
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param kwargs:
    :return:
    """
    print('test')
    msg = EmailMultiAlternatives(
        # title:
        f"Password Reset Token for {reset_password_token.user}",
        # message:
        reset_password_token.key,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
    msg.send()


# @receiver(new_user_registered)
# def new_user_registered_signal(user_id, **kwargs):
#     """
#     отправляем письмо с подтрердждением почты
#     """
    # send an e-mail to the user
    # token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
    #
    # msg = EmailMultiAlternatives(
    #     # title:
    #     f"Password Reset Token for {token.user.email}",
    #     # message:
    #     token.key,
    #     # from:
    #     settings.EMAIL_HOST_USER,
    #     # to:
    #     [token.user.email]
    # )
    # msg.send()


# @receiver(new_order)
# def new_order_signal(user_id, **kwargs):
#     """
#     отправяем письмо при изменении статуса заказа
#     """
#     # send an e-mail to the user
#     user = User.objects.get(id=user_id)
#
#     msg = EmailMultiAlternatives(
#         # title:
#         f"Обновление статуса заказа",
#         # message:
#         'Заказ сформирован',
#         # from:
#         settings.EMAIL_HOST_USER,
#         # to:
#         [user.email]
#     )
#
#     msg.send()
#
@shared_task()
def new_user_registered_(user_id, **kwargs):
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)
    msg = EmailMultiAlternatives(
        f'Токен подтверждения email для {token.user.email}',
        f'{token.key}',
        settings.EMAIL_HOST_USER,
        [token.user.email]
    )
    msg.send()


@shared_task()
def new_order_(user_id, **kwargs):
    user = User.objects.filter(id=user_id).first()

    msg = EmailMultiAlternatives(
        'Новый статус заказа',
        'Заказ передан поставщику',
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    msg.send()
