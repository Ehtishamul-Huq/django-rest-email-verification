from rest_framework import status, generics
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from user.serializers import UserRegistrationSerializer, UserLoginSerializer,UserSerializer, ChangePassSerializer, ForgotSerializer
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user_uuid = user_data['id']
        user = User.objects.get(email=user_data['email'])
        current_site = get_current_site(request).domain
        relativeLink = "/api/email-verify/"
        absurl = 'http://'+ current_site + relativeLink + user_uuid 
        email_body = 'Hi user use link below to verify your email \n' + absurl 
        data = {'email_body': email_body,'to_email': user.email, 'email_subject':'Verify Your Email'}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
	def get(self, request, pk):
		try:
			user = User.objects.get(id = pk)
			if user:
				user.is_verified = True
				user.save()
			return Response({'email':'Succesfully activated'}, status=status.HTTP_200_OK)
		except User.DoesNotExist:
			return Response({'Not a valid token'}, status=status.HTTP_400_BAD_REQUEST)

            
class UserLoginView(RetrieveAPIView):

    serializer_class = UserLoginSerializer    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        obj = User.objects.get(email=request.data['email'])
        user_serializer = UserSerializer(obj.profile)

        return Response({
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            "data": user_serializer.data,
             'token' : serializer.data['token'],
            }, 
            status=status.HTTP_200_OK)

class ForgotPassView(generics.GenericAPIView):
    def post(self, request):
        try:
            email = self.request.data['email']
            user_email = User.objects.get(email=email)
            serializer_class = ForgotSerializer(user_email)
            user_data = serializer_class.data
            user_uuid = user_data['id']
            current_site = get_current_site(request).domain
            relativeLink = "/api/change-pass/"
            absurl = 'http://'+ current_site + relativeLink + user_uuid 
            email_body = 'Hi user use link below to verify your email \n' + absurl 
            data = {'email_body': email_body,'to_email': user_email.email, 'email_subject':'Verify Your Email'}
            Util.send_email(data)
            return Response(user_data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response("User doesn't exist", status=status.HTTP_400_BAD_REQUEST)

class ChangePassView(generics.GenericAPIView):
    serializer_class = ChangePassSerializer
    def post(self,request,pk):
        user = self.request.data
        if user['password']!= user['confirm_password']:
            return Response({'Passwords must match.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_password = User.objects.get(id=pk)
            user_password.set_password(user['password'])
            user_password.save()
            return Response({'Password has been updated.'}, status=status.HTTP_200_OK)