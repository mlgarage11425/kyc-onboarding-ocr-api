from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import KYCUploadSerializer
from .models import KYCRecord

class KYCUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = KYCUploadSerializer(data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            return Response(
                {
                    "id": record.id,
                    "message": "Documents uploaded successfully"
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
