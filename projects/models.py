from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models import Avg
from datetime import datetime


# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=100)
    def projects(self):
        return self.projects_set.all()
    def __str__(self):
        return self.name


class ProjectTage(models.Model):
    tage = models.CharField(max_length=100, unique=True)

    def project_all(self):
        return self.projects_set.all()
    def __str__(self):
        return self.tage;


class Projects(models.Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE)
    totalTarget = models.IntegerField()
    tags = models.ManyToManyField(ProjectTage, null=True, blank=True)
    amountMoney = models.IntegerField(default=0)
    startCampaign = models.DateField()
    endcampaign = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def first_Projectphoto(self):
        return self.imageproject_set.all().first()
    def allImage(self):
        return self.imageproject_set.all()
    def rating(self):
        return self.rate_set.all().aggregate(Avg('rate'))
    def countrate(self):
        return self.rate_set.all().count()
    def comments(self):
        return self.comment_set.all()
    def commentcount(self):
        return self.comment_set.all().count()
    def get_date(self):
        time = datetime.now()
        if self.created.day == time.day:
            return str(time.hour - self.created.hour) + " hours ago"
        if self.created.month == time.month:
            return str(time.day - self.created.day) + " days ago"
        else:
            if self.created.year == time.year:
                return str(time.month - self.created.month) + " months ago"

        return self.created

    def __str__(self):
        return self.title


class ImageProject(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='pic_folder/projects/',
        default='pic_folder/None/no-img.jpg')

    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = ImageProject.objects.get(id=self.id)
        except ImageProject.DoesNotExist:
            # object is not in db, nothing to worry about
            return
        # is the save due to an update of the actual image file?
        if obj.image and self.image and obj.image != self.image:
            # delete the old image file from the storage in favor of the new file
            obj.image.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.image.delete()
        return super(ImageProject, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(ImageProject, self).save(*args, **kwargs)


class Rate(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(1)
        , MaxValueValidator(10)])

class FeatureProjects(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        if FeatureProjects.objects.count() == 5:
            FeatureProjects.objects.all()[0].delete()

        super(FeatureProjects, self).save(*args, **kwargs)

class Supplier(models.Model):
    supplierName = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    quanty = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class ReportProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


class ReportComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
