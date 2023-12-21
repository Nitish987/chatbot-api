from common.auth.jwt_token import Jwt
from common.utils import generator
from common.debug.log import Log
from constants.tokens import TokenExpiry, TokenType
from constants.headers import Header
from django.conf import settings
from .models import CustomerState


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

        # generating refresh token if no session found for the user
        customer_state = CustomerState.objects.filter(project_id=project_id)
        if customer_state.exists() and Jwt.validate(customer_state[0].refresh_token, category=Jwt.REFRESH)[0]:
            refresh_token = customer_state[0].refresh_token
        else:
            session_id = generator.generate_identity()
            refresh_token = Jwt.generate(
                type=TokenType.CUSTOMER_AUTH,
                sub=session_id,
                data={'project_id': project_id, 'host': host},
                category=Jwt.REFRESH,
                seconds=TokenExpiry.REFRESH_EXPIRE_SECONDS
            )
            if customer_state.exists():
                lst = customer_state[0]
                lst.session_id = session_id
                lst.refresh_token = refresh_token
                lst.save()
            else:
                CustomerState.objects.create(project_id=project_id, session_id=session_id, refresh_token=refresh_token)

        return { 
            'ct': access_token,
            'rt': refresh_token
        }
    
    @staticmethod
    def refresh_auth_token(refresh_token: str) -> dict:
        is_valid, payload = Jwt.validate(refresh_token, category=Jwt.REFRESH)
        if is_valid:
            project_id = CustomerState.objects.get(session_id=payload['sub']).project_id

            # refreshing access token
            access_token = Jwt.generate(
                type=TokenType.CUSTOMER_AUTH,
                sub=project_id,
                category=Jwt.ACCESS, 
                seconds=TokenExpiry.ACCESS_EXPIRE_SECONDS
            )
            
            return { 
                'ct': access_token,
                'rt': refresh_token,
            }
        raise Exception('Unauthenticated! No Session Found.')