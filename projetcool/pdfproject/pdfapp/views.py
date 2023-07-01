from django.shortcuts import render

# Create your views here.

# pdfapp/views.py

from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError, APIException
from reportlab.pdfgen import canvas
import io

class PDFView(APIView):
    def get(self, request):
        # Obtenir le texte de la requête
        text = request.query_params.get('text')
        
        # Valider le texte
        if not text:
            raise ValidationError('A "text" query parameter is required.')

        # Créer un nouveau PDF avec ReportLab
        buffer = io.BytesIO()
        try:
            p = canvas.Canvas(buffer)

            # Ajouter du texte au PDF
            p.drawString(100, 100, text)

            # Fermer le PDF et obtenir le contenu
            p.showPage()
            p.save()
            pdf = buffer.getvalue()
            buffer.close()
        except Exception as e:
            raise APIException('An error occurred while generating the PDF: ' + str(e))

        # Retourner le PDF comme une réponse HTTP
        return FileResponse(io.BytesIO(pdf), content_type='application/pdf')
