from rest_framework.views import APIView
from common.utils.response import Response
from common.debug.log import Log
from common.auth.permissions import IsCustomerAuthenticated
from .services import CustomerAuthService
from constants.tokens import TokenExpiry, CookieToken


class CustomerAuth(APIView):
    permission_classes = [IsCustomerAuthenticated]
    
    def post(self, request):
        try:
            tokens = CustomerAuthService.generate_auth_token()
            res = Response.success({'ct': tokens['ct']})
            res.set_cookie(
                CookieToken.REFRESH_TOKEN, 
                tokens['rt'], 
                secure=True, 
                httponly=True, 
                expires=TokenExpiry.REFRESH_EXPIRE_SECONDS
            )
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()
