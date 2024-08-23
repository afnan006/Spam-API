from django.contrib import admin
from django.urls import path, include
from api.views import home, UserCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include the API URLs
    path('', home),  # Serve index.html at the root URL
    path('users/', UserCreateView.as_view(), name='user-create'),

]
