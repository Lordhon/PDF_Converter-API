from django.db import models

class PDFConvertor(models.Model):
    file = models.FileField(upload_to='uploads/')
    upload_at = models.DateTimeField(auto_now_add=True)

