from rest_framework import serializers
from .models import User, Contact, SpamReport

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Contact Serializer
class ContactSerializer(serializers.ModelSerializer):
    is_spam = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'is_spam']

    def get_is_spam(self, obj):
        # Determine if the contact is marked as spam
        return SpamReport.objects.filter(phone_number=obj.phone_number).exists()

    def create(self, validated_data):
        contact = Contact.objects.create(**validated_data)
        # Check if the contact is marked as spam during creation
        if validated_data.get('is_spam', False):
            spam_report, created = SpamReport.objects.get_or_create(phone_number=contact.phone_number)
            if created:
                spam_report.reported_by.add(validated_data['user'])
                spam_report.report_count = 1
            else:
                spam_report.increment_report(validated_data['user'])
            spam_report.save()
        return contact

# Spam Report Serializer
class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = ['phone_number', 'reported_by', 'created_at']
