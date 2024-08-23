from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.username

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    is_spam = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Save the contact instance first
        super().save(*args, **kwargs)

        # Handle spam report if the contact is marked as spam
        if self.is_spam:
            spam_report, created = SpamReport.objects.get_or_create(phone_number=self.phone_number)
            if created:
                # If the report was just created, set the initial report_count to 1
                spam_report.report_count = 1
            else:
                # If the report already exists, increment the report_count
                spam_report.increment_report(self.user)
            spam_report.save()

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

class SpamReport(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    reported_by = models.ManyToManyField(User, related_name='spam_reports')
    report_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def increment_report(self, user):
        # Add the user to the list of reporters if not already present
        if not self.reported_by.filter(id=user.id).exists():
            self.reported_by.add(user)
            self.report_count += 1
            self.save()

    def __str__(self):
        return f"SpamReport for {self.phone_number} (Reports: {self.report_count})"
