Spam Checker API
Description
The Spam Checker API allows users to register, log in, manage contacts, and report spam. It features a user interface for registration and login, as well as a search function to check whether a number is marked as spam.

Project Structure
Outline the main directories and files in your project, especially focusing on the structure of the spam_checker project and api app. This will help users navigate the project.

Features
List the core features of your API, such as:

User Registration and Login
Contact Management
Spam Reporting
Search Functionality
API Endpoints
Provide a detailed list of all available API endpoints, including the method (GET, POST), URL, and a brief description of what each does. For example:

POST /api/register/ - Register a new user.
POST /api/login/ - Log in an existing user.
POST /api/contacts/ - Add a new contact.
POST /api/spam/ - Mark a phone number as spam.
GET /api/contacts/ - Search contacts by name or phone number.

Installation

Create a Virtual Environment:
python -m venv venv

On Windows:
venv\Scripts\activate

On macOS/Linux:
source venv/bin/activate

Install Dependencies:
pip install -r requirements.txt


Usage
Run Migrations:
python manage.py migrate

Create a Superuser (optional, for admin access):
python manage.py createsuperuser

Run the Development Server:
python manage.py runserver


Access the API:

Use Postman or similar tools to test the API endpoints:

Register User: POST /api/register/
Login: POST /api/login/
Add Contact: POST /api/contacts/
Mark as Spam: POST /api/spam/
Search Contacts: GET /api/contacts/



Testing
To test the application using the Django ORM shell, follow these steps:

Create Users: Start by creating two users with the following commands:

from api.models import User

user1 = User.objects.create(username='testuser003', phone_number='1231231234', email='testuser003@example.com')
user1.set_password('password003')
user1.save()

user2 = User.objects.create(username='testuser004', phone_number='4321432143', email='testuser004@example.com')
user2.set_password('password004')
user2.save()


Create Contacts: Next, create several contacts associated with these users:

from api.models import Contact

contact1 = Contact.objects.create(user=user1, name='Sample Contact 1', phone_number='5555555555', is_spam=True)
contact2 = Contact.objects.create(user=user1, name='Sample Contact 2', phone_number='6666666666', is_spam=False)

contact3 = Contact.objects.create(user=user2, name='Sample Contact 3', phone_number='7777777777', is_spam=True)
contact4 = Contact.objects.create(user=user2, name='Sample Contact 4', phone_number='8888888888', is_spam=False)


Verify Spam Reports: To ensure the spam reports are correctly associated with the contacts:

from api.models import SpamReport

spam_report1, created1 = SpamReport.objects.get_or_create(phone_number='5555555555')
spam_report2, created2 = SpamReport.objects.get_or_create(phone_number='7777777777')

print(spam_report1.phone_number, spam_report1.report_count, spam_report1.reported_by.all())
print(spam_report2.phone_number, spam_report2.report_count, spam_report2.reported_by.all())


Update Contacts: If needed, update the spam status of a contact and verify the update:

contact1.is_spam = False
contact1.save()

updated_contact1 = Contact.objects.get(phone_number='5555555555')
print(updated_contact1.is_spam)


Delete Contacts: To test the deletion functionality, delete a contact and confirm its removal:

contact_to_delete = Contact.objects.get(phone_number='6666666666')
contact_to_delete.delete()

try:
    deleted_contact = Contact.objects.get(phone_number='6666666666')
except Contact.DoesNotExist:
    print("Contact deleted successfully.")


Check Spam Report after Contact Deletion: Ensure that the spam report for a deleted contact no longer exists:

try:
    spam_report_after_deletion = SpamReport.objects.get(phone_number='6666666666')
except SpamReport.DoesNotExist:
    print("SpamReport for deleted contact does not exist.")


Test Relationships: To verify relationships, check the contacts associated with a user and the users who reported a specific contact as spam:


user1_contacts = user1.contacts.all()
print(user1_contacts)

reported_users = spam_report1.reported_by.all()
print(reported_users)


Filter Contacts: Use filtering to find contacts marked as spam or those with a specific phone number prefix:

spam_contacts = Contact.objects.filter(is_spam=True)
print(spam_contacts)

contacts_with_prefix = Contact.objects.filter(phone_number__startswith='555')
print(contacts_with_prefix)


Test Invalid Data: Attempt to retrieve a spam report for a non-existent phone number to handle invalid data:

try:
    non_existent_report = SpamReport.objects.get(phone_number='0000000000')
except SpamReport.DoesNotExist:
    print("SpamReport does not exist for the given phone number.")


Verify Password Hashing: Finally, confirm that user password hashing and authentication work as expected:

from django.contrib.auth import authenticate

user_authenticated = authenticate(username='testuser003', password='password003')
if user_authenticated:
    print("User authentication successful.")
else:
    print("User authentication failed.")


About Me
Afnan Ahmed
Email: afnan006cs@gmail.com
Phone: +91 82966 35241
Location: Jayanagar, Bengaluru

I am a recent graduate with a Bachelor's degree in Computer Science and Engineering. My academic background, combined with hands-on experience in full-stack development, has equipped me with the skills to design and develop efficient software solutions. I am passionate about coding, problem-solving, and continuously learning new technologies to enhance my capabilities in the software development field.
