from rest_framework import serializers
from .models import KYCRecord

class KYCUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCRecord
        fields = '__all__'
