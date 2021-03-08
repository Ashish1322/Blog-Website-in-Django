# Data base file
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Creating the Database for the Post
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default="")
    views = models.IntegerField(default=0)
    timestamp = models.DateField(blank=True)
    def __str__(self):
        return self.author+' by '+self.title

# Creating the Database for the Blog comments 
class BlogComments(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True) # For identify comment or reply in comment it is null while in reply it is sno of comment
    timestamp = models.DateField(default=now)
    def __str__(self):
        return self.comment[0:13] + '... by' + str(self.user)



