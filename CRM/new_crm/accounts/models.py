from django.db import models

class User(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leads')
    series = models.CharField(max_length=50)
    job_title = models.CharField(max_length=100)
    lead_owner = models.CharField(max_length=50)
    salutation = models.CharField(max_length=10, choices=[
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Others', 'Others'),
    ])
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ])
    status = models.CharField(max_length=20, choices=[
        ('Lead', 'Lead'),
        ('Opportunity', 'Opportunity'),
        ('Quotation', 'Quotation'),
        ('Converted', 'Converted'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"