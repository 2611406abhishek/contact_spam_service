from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.handlers.detail_handler import DetailHandler

class ContactDetailController(APIView):
    """
    Retrieves details for a person/contact based on its contact id.
    - If the person is a registered user, email is included **only if** the requester is in their contact list.
    - If the person is a contact, return the details without an email.
    - If no data is found, return a 404.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.detail_handler = DetailHandler()
    
    def get(self, request, contact_id):
        contact_details = self.detail_handler.get_contact_details(contact_id, request.user)
        if not contact_details:
            return Response({"detail": "Contact not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(contact_details, status=status.HTTP_200_OK)
