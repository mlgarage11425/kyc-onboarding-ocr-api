from django.db import models

class KYCRecord(models.Model):
    SOURCE_CHOICES = (
        ('OCR', 'OCR'),
        ('MANUAL', 'Manual'),
    )
    
    aadhaar_front = models.ImageField(upload_to='aadhaar/front/', null=True, blank=True)
    aadhaar_back = models.ImageField(upload_to='aadhaar/back/', null=True, blank=True)
    pan_card = models.ImageField(upload_to='pan/', null=True, blank=True)

    name = models.CharField(max_length=255, null=True, blank=True)
    aadhaar_number = models.CharField(max_length=12, null=True, blank=True)
    pan_number = models.CharField(max_length=10, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default='OCR')
    status = models.CharField(max_length=50, default='extracted')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"KYCRecord {self.id}"
