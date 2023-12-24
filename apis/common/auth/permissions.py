import requests
from django.conf import settings
from rest_framework import permissions
from constants.tokens import CookieToken, TokenType
from constants.headers import Header
from .jwt_token import Jwt
from ..debug.log import Log


# Api Request valid permission
class IsCustomerValid(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            project_id = request.query_params.get('project_id')
            response = requests.get(
                f'{settings.EXTERNAL_SERVER_HOST_URL}/api/external/v1/import/project/?project_id={project_id}',
                headers={'ASAK': settings.EXTERNAL_SERVER_API_KEY}
            )
            r = response.json()
            return r['success'] and request.META.get('HTTP_ORIGIN') in r['data']['project']['host']['urls']
        except Exception as e:
            Log.error(e)
            return False



# Api Request valid permission
class IsCustomerTokenValid(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            ct = request.COOKIES.get(CookieToken.ACCESS_TOKEN)
            is_valid, payload = Jwt.validate(ct)
            return is_valid and payload['type'] == TokenType.CUSTOMER_AUTH
        except Exception as e:
            Log.error(e)
            return False