from common.auth.jwt_token import Jwt
from common.debug.log import Log
from constants.tokens import TokenExpiry, TokenType


class CustomerAuthService:

    @staticmethod
    def generate_auth_token(project_id: str, host: str) -> dict:
       # generating access token
        access_token = Jwt.generate(
            type=TokenType.CUSTOMER_AUTH,
            sub=project_id,
            data={'host': host},
            category=Jwt.ACCESS, 
            seconds=TokenExpiry.ACCESS_EXPIRE_SECONDS
        )

        return access_token