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
    extract_name_from_text,
    extract_name_from_aadhaar,
    extract_address,
    clean_name
)


class KYCUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = KYCUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        record = serializer.save()

        # OCR per document (isolation is important)
        aadhaar_text = extract_text(record.aadhaar_front.path) if record.aadhaar_front else ""
        pan_text = extract_text(record.pan_card.path) if record.pan_card else ""
        address_text = extract_text(record.aadhaar_back.path) if record.aadhaar_back else ""

        # Field extraction
        record.aadhaar_number = extract_aadhaar(aadhaar_text)
        record.pan_number = extract_pan(pan_text)
        record.date_of_birth = extract_dob(aadhaar_text)

        # Name: PAN > Aadhaar
        '''raw_name = extract_name_from_aadhaar(aadhaar_text)
        record.name = clean_name(raw_name)'''

        # Name: PAN > Aadhaar (priority)
        name_from_pan = extract_name_from_text(pan_text)
        name_from_aadhaar = extract_name_from_aadhaar(aadhaar_text)

        raw_name = name_from_pan or name_from_aadhaar
        record.name = clean_name(raw_name)

        # Address: Aadhaar back only
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
