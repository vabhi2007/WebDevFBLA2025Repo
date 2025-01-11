from django.db import models

# Create your models here.

#Job posting model
class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

#Job application model 
class Application(models.Model):
    job_post = models.ForeignKey(JobPost, related_name="applications", on_delete=models.CASCADE)
    applicant_name = models.CharField(max_length=255)
    applicant_email = models.EmailField()
    resume = models.CharField(max_length=255)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant_name} - {self.job_post.title}"