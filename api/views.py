from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from .models import Contact, SpamReport
from .serializers import ContactSerializer, UserSerializer, User
from django.contrib.auth import authenticate

@login_required
def add_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        form = ContactForm()
    return render(request, 'add_contact.html', {'form': form})

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        contact = serializer.save(user=self.request.user)
        if contact.is_spam:
            spam_report, created = SpamReport.objects.get_or_create(phone_number=contact.phone_number)
            if not created:
                spam_report.increment_report(self.request.user)
            else:
                spam_report.reported_by.add(self.request.user)
                spam_report.report_count = 1
                spam_report.save()

class MarkSpam(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        contact = Contact.objects.filter(phone_number=phone_number).first()

        if not contact:
            SpamReport.objects.create(phone_number=phone_number, reported_by=request.user)
        else:
            contact.is_spam = True
            contact.save()
            spam_report, created = SpamReport.objects.get_or_create(phone_number=phone_number)
            if not created:
                spam_report.increment_report(request.user)
            else:
                spam_report.reported_by.add(request.user)
                spam_report.report_count = 1
                spam_report.save()

        return Response({'status': 'success'}, status=status.HTTP_200_OK)

class ContactPagination(PageNumberPagination):
    page_size = 10

class Search(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ContactPagination

    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({'error': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if query.isdigit():
            results = Contact.objects.filter(phone_number__icontains=query).order_by('phone_number')
        else:
            results = Contact.objects.filter(name__icontains=query).order_by('name')

        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(results, request)

        contacts = []
        for contact in paginated_results:
            is_spam = SpamReport.objects.filter(phone_number=contact.phone_number).exists()
            contacts.append({
                'name': contact.name,
                'phone_number': contact.phone_number,
                'is_spam': is_spam
            })

        return paginator.get_paginated_response(contacts)

class SearchContactsView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ContactPagination

    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({'error': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if query.isdigit():
            results = Contact.objects.filter(phone_number__icontains=query)
        else:
            results = Contact.objects.filter(name__icontains=query)

        paginator = self.pagination_class()
        paginated_results = paginator.paginate_queryset(results, request)

        contacts = []
        for contact in paginated_results:
            is_spam = SpamReport.objects.filter(phone_number=contact.phone_number).exists()
            contacts.append({
                'name': contact.name,
                'phone_number': contact.phone_number,
                'is_spam': is_spam
            })

        return paginator.get_paginated_response(contacts)
class AddContactView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = ContactSerializer(data=data)

        if serializer.is_valid():
            contact = serializer.save(user=request.user)
            return Response({'status': 'success', 'contact': ContactSerializer(contact).data}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
class ReportSpamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        phone_number = data.get('phone_number')

        if not phone_number:
            return Response({'status': 'error', 'message': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            contact = Contact.objects.get(phone_number=phone_number)
            spam_report, created = SpamReport.objects.get_or_create(phone_number=phone_number, defaults={'reported_by': [request.user]})
            if not created:
                spam_report.reported_by.add(request.user)
                spam_report.report_count += 1
                spam_report.save()
            return Response({'status': 'success'})
        except Contact.DoesNotExist:
            return Response({'status': 'error', 'message': 'Contact does not exist.'}, status=status.HTTP_404_NOT_FOUND)

def home(request):
    return render(request, 'index.html')
