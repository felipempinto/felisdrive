from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            # six.text_type(user.pk) + six.text_type(timestamp) +
            # six.text_type(user.is_active)
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.username)
        )
account_activation_token = TokenGenerator()