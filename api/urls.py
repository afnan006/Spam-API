from django.urls import path
from .views import UserLoginView, RegisterUser, MarkSpam, Search, ReportSpamView, AddContactView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('register/', RegisterUser.as_view(), name='user_register'),
    path('mark_spam/', MarkSpam.as_view(), name='mark_spam'),
    path('report_spam/', ReportSpamView.as_view(), name='report_spam'),
    path('search/', Search.as_view(), name='search'),
    path('add-contact/', AddContactView.as_view(), name='add_contact'),  # Ensure this is correct
]
