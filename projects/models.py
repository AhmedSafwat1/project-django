from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Projects(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE)
    totalTarget = models.IntegerField()
    amountMoney = models.IntegerField(default=0)
    startCampaign = models.DateField()
    endcampaign = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ImageProject(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='pic_folder/',
        default='pic_folder/None/no-img.jpg')




class Rate(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1)
        , MaxValueValidator(10)])
    def __str__(self):
        return self.rate

class Supplier(models.Model):
    supplierName = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    quanty = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.supplierName,self.quanty)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return (self.user,self.content,self.project)
class ReportProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.user, self.content, self.project)

class ReportComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.user, self.content, self.comment)