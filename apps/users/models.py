from django.db import models
import re
import bcrypt

# Create your models here.


class UserManager(models.Manager):
    def validate_name(self, request, props=None):
        errors = ""
        NAME_REGEX = re.compile(r'[a-zA-Z]+')
        if len(request) < 2:
            errors = (str(props).title() +
                      " must be at least 2 characters long!")
        elif not NAME_REGEX.match(request):
            errors = (str(props).title() + " must contain letter only!")
        return errors

    def validate_email(self, request, props=None):
        errors = ""
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        existing_email = self.filter(email=request)
        if len(request) < 1:
            errors = (str(props).title() + " is required!")
        elif not EMAIL_REGEX.match(request):
            errors = (str(props).title() + " is invalid email!")
        if existing_email:
            errors = (str(props).title() + " already in use!")
        return errors

    def validate_password(self, request, props=None):
        errors = ""
        if len(request) < 8:
            errors = (str(props).title() +
                      " must be at least 8 characters long!")
        return errors

    def basic_validation(self, postData):
        errors = []
        name = self.validate_name(postData['first_name'], 'first name')
        alias = self.validate_name(postData['last_name'], 'last name')
        email = self.validate_email(postData['email'], 'email')
        password = self.validate_password(postData['password'], 'password')
        conf_pwd = self.validate_password(
            postData['confirm_pw'], 'confirm password')
        if name:
            errors.append(name)
        if alias:
            errors.append(alias)
        if email:
            errors.append(email)
        if password:
            errors.append(password)
        if conf_pwd:
            errors.append(conf_pwd)
        elif postData['password'] != postData['confirm_pw']:
            errors.append("Password doesn't match!")
        return errors

    def user_create(self, postData):
        pw_hash = bcrypt.hashpw(
            postData['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=pw_hash)
        return user

    def login(self, postData):
        # check for existance of email in db
        existing_users = User.objects.filter(email=postData['email'])
        if len(postData['password']) < 1 and len(postData['email']) < 1:
            return (False, "Please enter valid credentials in order to login")
        if existing_users:
            if bcrypt.checkpw(postData['password'].encode(), existing_users[0].password.encode()):
                return (True, existing_users[0].id)
            return (False, "Incorrect Email or Password!")
        else:
            return (False, "Incorrect Email or Password!")


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    objects = UserManager()
