from rest_framework import serializers



from converter.models import PDFConvertor


class PDFConvertorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFConvertor
        fields = ['id','file','upload_at']