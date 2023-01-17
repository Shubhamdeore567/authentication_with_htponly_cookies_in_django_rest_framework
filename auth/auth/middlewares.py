# TODO middlewares yet to be finalise
import jwt
import time
from django.conf import settings
from rest_framework.response import Response
import re
from users.models import User
import datetime
import jwt
from django.conf import settings


def create_new_access_token(refresh_token):
    try:
        # Decode the refresh token to get the user's information
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        # Create a new access token using the same user information
        access_token = jwt.encode({'username': payload['username']}, settings.SECRET_KEY, algorithm='HS256').decode(
            'utf-8')
        return access_token
    except jwt.exceptions.DecodeError:
        return None


def is_token_expired(payload):
    if payload["exp"] < time.time():
        return True
    else:
        return False


def refresh_token(refresh_token):
    try:
        # decode the refresh token to get the payload
        refresh_token_payload = jwt.decode(refresh_token, "secret", algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        # if the refresh token is invalid or expired
        return None

    # create a new payload for the session token
    session_token_payload = {
        'id': refresh_token_payload['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
        "iat": datetime.datetime.utcnow()
    }

    # encode the payload with the secret key to create the session token
    session_token = jwt.encode(session_token_payload, "secret", algorithm='HS256')

    return session_token


class AutoUpdateAccessTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.EXEMPT_URLS = []
        if hasattr(settings, "LOGIN_EXEMPT_URLS"):
            self.EXEMPT_URLS = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

    # called before/after response method
    def __call__(self, request):
        path = request.path_info
        if any(url.match(path.lstrip("/")) for url in self.EXEMPT_URLS):
            return self.get_response(request)
        response = self.get_response(request)
        access_token = request.COOKIES.get('jwt')
        if access_token:
            try:
                payload = jwt.decode(access_token, "secret", algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                payload = jwt.decode(
                    access_token,
                    "secret",
                    algorithms=["HS256"],
                    options={"verify_signature": False},
                )

            user = User.objects.get(id=payload["id"])
            refresh_token_value = user.refresh_token
            if access_token:
                # Check if the access token has expired

                # if user.is_email_verified:
                #     return False
                if is_token_expired(payload):
                    # Refresh the access token
                    new_access_token = refresh_token(refresh_token_value)
                    # response = Response()
                    response = self.get_response(
                        request
                    )

                    # Update the access token in the response cookies
                    response.set_cookie(key="jwt", value=new_access_token, httponly=True)
                    # return response
                # else:
                #
        return response
