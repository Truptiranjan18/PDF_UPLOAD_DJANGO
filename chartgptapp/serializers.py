from rest_framework import serializers


class PDFSTORESERIALIZER(serializers.Serializer):
    upload_pdf = serializers.FileField(allow_null=False)
    text= serializers.CharField(max_length=255,allow_null=True,allow_blank=True)

