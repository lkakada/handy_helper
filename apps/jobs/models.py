from django.db import models
from ..users.models import User

# Create your models here.


class JobManager(models.Manager):
    def jobValidation(self, postData):
        errors = []
        if len(postData['title']) < 1:
            errors.append("Title field is required!")
        elif len(postData['title']) < 3:
            errors.append("Title must be greater than three characters long!")
        if len(postData['description']) < 1:
            errors.append("Description field is required!")
        elif len(postData['description']) < 10:
            errors.append(
                "Description must be greater than ten characters long!")
        if len(postData['location']) < 1:
            errors.append("Location field is required!")

        return errors


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="jobs")
    users_add = models.ManyToManyField(User, related_name="add_jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def updatedJob(self, postData):
        self.title = postData['title']
        self.description = postData['description']
        self.location = postData['location']
        self.save()

    objects = JobManager()
