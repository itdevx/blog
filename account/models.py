from django.contrib.auth.models import AbstractUser
from extentions.utils import jalali_converter
from django.utils import timezone
from django.db import models
import os



def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.username}{ext}'
    return f'profile/{instance.username}/{final_name}'



class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_author = models.BooleanField(default=False)
    image = models.ImageField(default="defualt/post-hover-image-03.jpg", null=True, blank=True, upload_to=upload_image_path)
    info = models.TextField(null=True, blank=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=300, null=True, blank=True)
    twitter = models.CharField(max_length=300, null=True, blank=True)
    instagram = models.CharField(max_length=300, null=True, blank=True)
    github = models.CharField(max_length=300, null=True, blank=True)
    telegram = models.CharField(max_length=300, null=True, blank=True)
    website = models.CharField(max_length=300, null=True, blank=True)

    def jlastlogin(self):
        return jalali_converter(self.last_login)
        
    def jdatejoin(self):
        return jalali_converter(self.date_joined)

    def sum_date_joined(self):
        time = timezone.now().date() - self.date_joined.date()
        time = str(time)
        time = time.replace('0:00:00', '')
        time = time.replace('days,', 'روز ')
        # if self.date_joined.date() <= timezone.now().date():
        #     test = 'امروز'
        #     return test
        #     # return self.date_joined.date()
        # elif self.date_joined.date() > 1:
        #     return time
        return time
        