from rest_framework.views import APIView
from common.utils.response import Response
from common.debug.log import Log
from common.auth.permissions import IsCustomerTokenValid
from .services import ChatbotService


class Chatbot(APIView):
    permission_classes = [IsCustomerTokenValid]

    def get(self, request):
        try:
            service = ChatbotService(
                project_id=request.query_params.get('project_id'),
                api_id=request.query_params.get('api_id')
            )
            service.initialize(apikey=request.META.get('HTTP_AUTHORIZATION'))
            if service.is_valid:
                answer = service.generate_response_accordingly(request.query_params.get('query'))
                return Response.success({'answer': answer})
            return Response.permission_denied()
        except Exception as e:
            Log.error(e)
            return Response.something_went_wrong()