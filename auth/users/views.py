import uuid

from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from .utils import send_mail_token
from .models import User

'''
Python Django login and generate JWT Token using HttpOnly Cookies.
 We will Login using JWT( JSON Web Token ) which is the standard method for SPA Authentications. 
 We will not use the traditional "Bearer method" but 
 instead we will login using HttpOnly cookies which is a more secure authentication.
'''


class Register(APIView):
    def post(self, request):
        data = request.data
        token = str(uuid.uuid4())

        data.update({"email_token": token})
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        refresh_payload = {
            'id': serializer.data['id'],
            'type': 'refresh'
        }
        refresh_token = jwt.encode(refresh_payload, "secret", algorithm='HS256')
        user = User.objects.get(id=serializer.data["id"])
        user.refresh_token = refresh_token
        user.save()
        send_mail_token(request.data["email"], token)

        return Response({
            "success": True,
            "message": "successfully register",
            "data": serializer.data
        })


class VerifyEmail(APIView):
    def post(self, request):
        email_token = request.data["email_token"]
        payload = jwt.decode(request.COOKIES.get("jwt"), "secret", algorithms=["HS256"])
        obj = User.objects.get(id=payload["id"])
        if obj.email_token == email_token:
            obj.is_email_verified = True
            obj.save()
        else:
            return Response({
                "success": False,
                "message": "invalid token"
            })
        return Response({
            "success": True,
            "message": "Email Verified Successfully"
        })


class Login(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("user not found")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        payload = {
            'id': user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, "secret", algorithm='HS256')
        # Encode the payload with the secret key and an expiration time

        response = Response()
        response.data = {
            "success": True,
            "message": "Login successfully",
            "session_token": token}
        response.set_cookie(key="jwt", value=token, httponly=True)
        return response


class GetUser(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if not token:
            raise AuthenticationFailed("UnAuthenticated")
        payload = jwt.decode(token, "secret", algorithms=["HS256"], options={"verify_signature": False})
        user = User.objects.filter(id=payload["id"]).first()
        serializer = UserSerializer(user)
        response = {
            "success": True,
            "message": "user data fetched successfully",
            "data": serializer.data
        }
        return Response(response)


class LogOut(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "success": True,
            "message": "Log Out Successfully"
        }
        return response
