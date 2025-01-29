import os
import uuid
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from .models import PDFSTORE
from .serializers import PDFSTORESERIALIZER
from django.conf import settings


class UPLOADPDFCHARTGPT(CreateAPIView):
    queryset = PDFSTORE.objects.all()
    serializer_class = PDFSTORESERIALIZER

    def create(self, request, *args, **kwargs):
        try:
            # Validate and save data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            upload_pdf = serializer.validated_data.get('upload_pdf')
            text = serializer.validated_data.get('text')

            # Check if the uploaded file is a PDF
            if upload_pdf.content_type != 'application/pdf':
                raise ValidationError({"upload_pdf": "Only PDF files are allowed."})

            # Define the directory for storing uploaded files
            upload_dir = os.path.join(settings.BASE_DIR, 'uploaded_files')
            os.makedirs(upload_dir, exist_ok=True)  # Create the directory if it doesn't exist

            # Generate a unique file name to prevent overwriting existing files
            unique_filename = f'{uuid.uuid4().hex}_{upload_pdf.name}'
            file_path = os.path.join(upload_dir, unique_filename)

            # Read the content of the PDF file as binary data
            binary_data = upload_pdf.read()
            #print(binary_data)

            # Save the file to the generated path
            with open(file_path, 'wb') as f:
                f.write(binary_data)

            # Save the data to the database
            pdf_instance = PDFSTORE.objects.create(
                file_path=file_path,
                binary_data=binary_data,
                file_type=upload_pdf.content_type
            )

            # Prepare the response with the question and answer
            response_data = {
                "question": text,
                "answer": "My name is Trupti Ranjan Lenka",
                "pdf_details": {
                    "id": pdf_instance.id,
                    "file_path": pdf_instance.file_path,
                    "file_type": pdf_instance.file_type,
                }
            }

            return Response({'message': 'success', 'data': response_data}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)