from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):
#it is used to add additional attributes directly using User class may cause errors in database
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    #additional classes or attributes
    portfolio_site=models.URLField(blank=True)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)
    def __str__(self):
        return self.user.username
        #username is the default attribute of the user that we created in line 7
#new part from here
class GithubUsers(models.Model):
    git_username=models.CharField(max_length=264)
    def __str__(self):
        return self.git_username
