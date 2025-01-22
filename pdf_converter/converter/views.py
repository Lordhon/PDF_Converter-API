import os.path

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from converter.serializer import PDFConvertorSerializer

from reportlab.lib.pagesizes import letter
from reportlab.lib import fonts


class TxtToPdfConverter(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        # Получаем сериализатор и проверяем
        serializer = PDFConvertorSerializer(data=request.data)
        if serializer.is_valid():
            # Получаем файл и создаем путь для сохранения
            txt_file = serializer.validated_data['file']
            input_path = txt_file.name
            output_path = os.path.join(settings.MEDIA_ROOT, 'converted', f'converted_{os.path.basename(input_path)}.pdf')

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Конвертируем .txt в .pdf
            self.convert_txt_to_pdf(txt_file, output_path)

            return Response({
                "message": "File successfully converted",
                "download_url": f"{settings.MEDIA_URL}converted/converted_{os.path.basename(input_path)}.pdf"
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def convert_txt_to_pdf(self, txt_file, pdf_file_path):
        # Чтение текста
        text_content = txt_file.read().decode('utf-8')

        # Путь к шрифту Hack
        font_path = "/usr/share/fonts/truetype/hack/Hack-Regular.ttf"

        # Проверка наличия шрифта
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font not found at {font_path}")

        # Регистрация шрифта
        pdfmetrics.registerFont(TTFont('Hack', font_path))

        # Создание PDF файла
        c = canvas.Canvas(pdf_file_path, pagesize=letter)
        width, height = letter

        # Установка шрифта
        c.setFont("Hack", 10)

        # Настройка текста
        y_position = height - 40

        # Добавка текста в PDF
        for line in text_content.split("\n"):
            c.drawString(30, y_position, line)
            y_position -= 12  # Переход на новую строку

            # Новая страница
            if y_position < 40:
                c.showPage()
                c.setFont("Hack", 10)
                y_position = height - 40

        c.save()