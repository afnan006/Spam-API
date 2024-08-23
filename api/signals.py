# api/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Contact, SpamReport

@receiver(post_save, sender=Contact)
def handle_spam_report(sender, instance, **kwargs):
    if instance.is_spam:
        spam_report, created = SpamReport.objects.get_or_create(phone_number=instance.phone_number)
        if created:
            spam_report.report_count = 1
        else:
            spam_report.increment_report(instance.user)
        spam_report.save()
    else:
        SpamReport.objects.filter(phone_number=instance.phone_number).delete()

@receiver(post_delete, sender=Contact)
def delete_spam_report(sender, instance, **kwargs):
    SpamReport.objects.filter(phone_number=instance.phone_number).delete()
