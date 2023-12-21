from rest_framework.views import APIView
from common.utils.response import Response
from common.debug.log import Log
from common.auth.permissions import IsCustomerAuthenticated
from .services import ChatbotService
from constants.tokens import TokenExpiry, CookieToken


class Chatbot(APIView):
    # TODO add permission for customer token authentication
    # permission_classes = [IsCustomerAuthenticated]

    def post(self, request):
        try:
            service = ChatbotService(
                project_id=request.query_params.get('project_id'),
                api_id=request.query_params.get('api_id')
            )
            service.initialize(apikey=request.META.get('HTTP_AUTHORIZATION'))
            if service.is_valid:
                answer = service.generate_response_accordingly(request.data.get('query'))
                return Response.success({'answer': answer})
            return Response.permission_denied()
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()