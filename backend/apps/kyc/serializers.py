from rest_framework import serializers
from .models import KYCRecord

class KYCUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCRecord
        fields = [
            'aadhaar_front',
            'aadhaar_back',
            'pan_card'
        ]
