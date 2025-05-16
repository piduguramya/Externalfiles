from .models import EmployeeDetails
from .serializers import EmployeeDetailsSerializer
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.views import View
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import fitz  # PyMuPDF



# pip install PyMuPDF
class UploadPDFView(APIView):
    def post(self, request):
        file = request.FILES.get('file')

        if not file or not file.name.endswith('.pdf'):
            return Response({'error': 'Upload a valid .pdf file'}, status=400)

        try:
            pdf_content = file.read()
            with fitz.open(stream=pdf_content, filetype="pdf") as doc:
                text = ""
                for page in doc:
                    text += page.get_text()

            lines = text.strip().split('\n')

            # print("Extracted Text:")
            # print(text)
            # print(lines)


            for line in lines:
                if "employename" not in line.lower():
                    parts = line.strip().split(',')

                    # Initialize with default values
                    employename = designation = dateofjoining = None

                    for part in parts:
                        key_value = part.strip().split(":", 1)
                        if len(key_value) != 2:
                            continue

                        key, value = key_value[0].strip().lower(), key_value[1].strip()

                        if key == "employename":
                            employename = value
                        elif key == "designation":
                            designation = value
                        elif key == "dateofjoining":
                            dateofjoining = value

                    # Only save if all required fields are present
                    if employename and designation and dateofjoining:
                        EmployeeDetails.objects.create(
                            employename=employename,
                            designation=designation,
                            dateofjoining=dateofjoining  # Assuming this is a DateTimeField
                        )

                        print(f"Saving: {employename}, {designation}, {dateofjoining}, {workingproject}")



            return Response({'message': 'PDF data saved to database'}, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=500)



class extractdata(APIView):
    def post(self,request):
        file=request.FILES.get('file')

        if not file:
            return Response('no file uploaded')

        try:
            if file.name.endswith(".csv"):
                convert_df=pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                convert_df=pd.read_excel(file)
            elif file.name.endswith('.txt'):
                content = file.read().decode('utf-8')
                convert_df = content.strip().split('\n')

                for line in convert_df:                             #for text files
                    employename, designation, dateofjoining, workingproject = line.strip().split(',')

                    EmployeeDetails.objects.create(
                       employename=employename,
                       designation=designation,
                       dateofjoining=dateofjoining,
                       workingproject=workingproject
                    )
                
                
            else:
                return Response("unsuported file format")

            # for _, row in convert_df.iterrows():         #for excel and csv  
                # EmployeeDetails.objects.create(
                    # employename=row['employename'],
                    # designation=row['designation'],
                    # dateofjoining=row['dateofjoining'],
                    # workingproject=row['workingproject']
                # )


            return Response('data uploaded successfully')
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class GeneratePDF(APIView):
    def get(self, request, *args, **kwargs):
        # Prepare PDF HTTP response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="data_report.pdf"'

        # Create PDF canvas
        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 50  # starting y position

        # Get data as dictionaries
        data = EmployeeDetails.objects.values()

        for record in data:
            line = ', '.join([f"{k}: {v}" for k, v in record.items()])
            p.drawString(50, y, line)
            y -= 20

            # Add new page if space is low
            if y < 50:
                p.showPage()
                y = height - 50

        p.save()
        return response


class convertto_excel(APIView):
    def get(self,request):
        querydata_asobj=EmployeeDetails.objects.all().values()
        convert_df=pd.DataFrame(querydata_asobj)
        response=HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=aaaa.xlsx'
        convert_df.to_excel(response, index=False)
        return response

class convertto_csv(APIView):
    def get(self,request):
        querydata=EmployeeDetails.objects.all().values()
        convert_df=pd.DataFrame(querydata)
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']='attachment; filename=csvfile.csv'
        convert_df.to_csv(response, index=False)
        return response









