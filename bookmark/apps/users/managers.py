from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, password=None):

        if not password:
            raise ValueError('Users must have a pass')
        if not email:
            raise ValueError('Users must have an Email')

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.save(using=self._db)
        return user
