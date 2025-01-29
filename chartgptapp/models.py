from django.db import models

# Create your models here.

class PDFSTORE(models.Model):
    # Field to store the file path
    file_path = models.CharField(max_length=255, unique=True)

    # Field to store the binary format of the PDF
    binary_data = models.BinaryField()

    # Field to store the file type
    file_type = models.CharField(max_length=50, default='application/pdf')

