from django.utils.timezone import now
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField('RewardsAppUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('RewardsAppUsers', models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class RewardsAppAndroidapp(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    category = models.CharField(max_length=50)
    subcategory = models.CharField(max_length=50)
    points = models.IntegerField()
    created_on = models.DateField(default=now().date)
    deleted_on = models.DateField(blank=True, null=True)
    app_logo = models.ImageField(upload_to='app_logos/', blank=True, null=True)
    is_delete = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rewards_app_androidapp'



ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('user', 'User'),
)

class RewardsAppUsers(models.Model):
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Storing hashed password
    profilepic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_on = models.DateField(default=now().date, blank=True, null=True)
    deleted_on = models.DateField(blank=True, null=True)
    is_delete = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rewards_app_users'
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']
    is_anonymous = False
    is_authenticated = True


    def set_password(self, raw_password):
        """Hashes and sets the password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verifies the password."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email
    


class RewardsAppUsertask(models.Model):
    user = models.ForeignKey(RewardsAppUsers, on_delete=models.CASCADE)
    task = models.ForeignKey(RewardsAppAndroidapp, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    screenshot = models.ImageField(upload_to='screenshots/', blank=True, null=True)
    points_earned = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rewards_app_usertask'









# from django.db import models
# from django.utils.timezone import now
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.hashers import make_password, check_password

# ROLE_CHOICES = (
#     ('admin', 'Admin'),
#     ('user', 'User'),
# )

# class Users(models.Model):
#     name = models.CharField(max_length=20)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', blank=True, null=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)  # Storing hashed password
#     profilepic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#     created_on = models.DateField(default=now().date, blank=True, null=True)
#     deleted_on = models.DateField(blank=True, null=True)
#     is_delete = models.BooleanField(default=False, blank=True, null=True)

#     def set_password(self, raw_password):
#         """Hashes and sets the password."""
#         self.password = make_password(raw_password)

#     def check_password(self, raw_password):
#         """Verifies the password."""
#         return check_password(raw_password, self.password)

#     def __str__(self):
#         return self.email

# class Users(AbstractUser):
#     name = models.CharField(max_length=20)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', blank=True, null=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)  # Storing hashed password
#     profilepic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#     created_on = models.DateField(default=now().date, blank=True, null=True)
#     deleted_on = models.DateField(blank=True, null=True)
#     is_delete = models.BooleanField(default=False, blank=True, null=True)

#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='rewardsapp_users_groups',
#         blank=True,
#         help_text="The groups this user belongs to."
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='rewardsapp_users_permissions',
#         blank=True,
#         help_text="Specific permissions for this user."
#     )


# from django.db import models
# from django.utils.timezone import now
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.hashers import make_password, check_password

# ROLE_CHOICES = (
#     ('admin', 'Admin'),
#     ('user', 'User'),
# )

# class Users(AbstractUser):  # Make sure this is inheriting from AbstractUser
#     name = models.CharField(max_length=20)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', blank=True, null=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128)  # Storing hashed password
#     profilepic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#     created_on = models.DateField(default=now().date, blank=True, null=True)
#     deleted_on = models.DateField(blank=True, null=True)
#     is_delete = models.BooleanField(default=False, blank=True, null=True)

#     # last_login = models.DateTimeField(blank=True, null=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name', 'role']

#     # def set_password(self, raw_password):
#     #     """Hashes and sets the password."""
#     #     self.password = make_password(raw_password)

#     # def check_password(self, raw_password):
#     #     """Verifies the password."""
#     #     return check_password(raw_password, self.password)

#     def __str__(self):
#         return self.email


# class AndroidApp(models.Model):
    # name = models.CharField(max_length=100)
    # url = models.URLField()
    # category = models.CharField(max_length=50)
    # subcategory = models.CharField(max_length=50)
    # points = models.IntegerField()
    # created_on = models.DateField(default=now().date)
    # deleted_on = models.DateField(blank=True, null=True)
    # app_logo = models.ImageField(upload_to='app_logos/', blank=True, null=True)
    # is_delete = models.BooleanField(default=False, blank=True, null=True)


# class UserTask(models.Model):
#     user = models.ForeignKey(Users, on_delete=models.CASCADE)
#     task = models.ForeignKey(AndroidApp, on_delete=models.CASCADE)
#     is_completed = models.BooleanField(default=False)
#     screenshot = models.ImageField(upload_to='screenshots/', blank=True, null=True)
#     points_earned = models.IntegerField()


