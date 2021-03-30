from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email, password=None):
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email),)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password):
        if password is None:
            raise TypeError('Superusers must have password')

        user = self.create_user(email,password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user