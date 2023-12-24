from rest_framework.views import APIView
from common.utils.response import Response
from common.debug.log import Log
from common.auth.permissions import IsCustomerValid
from .services import CustomerAuthService
from constants.tokens import TokenExpiry, CookieToken


class CustomerAuth(APIView):
    permission_classes = [IsCustomerValid]
    
    def get(self, request):
        try:
            token = CustomerAuthService.generate_auth_token(
                request.query_params.get('project_id'), 
                request.META.get('HTTP_ORIGIN')
            )
            # sending response
            res = Response.success({'message': 'Authenticated'})
            res.set_cookie(
                CookieToken.ACCESS_TOKEN, 
                token, 
                secure=True, 
                httponly=True, 
                expires=TokenExpiry.REFRESH_EXPIRE_SECONDS
            )
            return res
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()