from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.handlers.search_handler import SearchHandler
from api.serializers import SearchResultSerializer

class SearchController(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_handler = SearchHandler()
    
    def get(self, request):
        name_query = request.query_params.get('name')
        phone_query = request.query_params.get('phone')
        if name_query:
            results = self.search_handler.search_by_name(name_query)
            serializer = SearchResultSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif phone_query:
            results = self.search_handler.search_by_phone(phone_query)
            serializer = SearchResultSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "A search parameter (name or phone) must be provided."},
                            status=status.HTTP_400_BAD_REQUEST)
