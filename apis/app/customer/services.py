from common.auth.jwt_token import Jwt
from common.utils import generator
from common.debug.log import Log
from constants.tokens import TokenExpiry
from constants.headers import Header
from django.conf import settings


class CustomerAuthService:

    @staticmethod
    def generate_auth_token(host: str) -> dict:
        # TODO generate auth tokens
        pass