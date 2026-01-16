from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import KYCUploadSerializer
from .models import KYCRecord
from .ocr_utils import extract_text
from .extraction_utils import (
    extract_aadhaar,
    extract_pan,
    extract_dob,
    extract_name,
    extract_address
)

class KYCUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = KYCUploadSerializer(data=request.data)
        if serializer.is_valid():
            record = serializer.save()

            aadhaar_text = extract_text(record.aadhaar_front.path) if record.aadhaar_front else ""
            pan_text = extract_text(record.pan_card.path) if record.pan_card else ""
            address_text = extract_text(record.aadhaar_back.path) if record.aadhaar_back else ""

            record.aadhaar_number = extract_aadhaar(aadhaar_text)
            record.pan_number = extract_pan(pan_text)
            record.date_of_birth = extract_dob(aadhaar_text)
            record.name = extract_name(aadhaar_text)
            record.address = extract_address(address_text)

            record.status = "extracted"
            record.save()

            return Response(
                {
                    "id": record.id,
                    "status": record.status,
                    "name": record.name,
                    "aadhaar_number": record.aadhaar_number,
                    "pan_number": record.pan_number,
                    "dob": record.date_of_birth,
                    "address": record.address
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
