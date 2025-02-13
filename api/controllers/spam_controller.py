from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.handlers.spam_handler import SpamHandler
from api.serializers import SpamMarkSerializer  

class SpamController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spam_handler = SpamHandler()
    
    def post(self, request):
        serializer = SpamMarkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        self.spam_handler.mark_number_as_spam(phone_number)
        return Response({"detail": "Number marked as spam."}, status=status.HTTP_201_CREATED)
