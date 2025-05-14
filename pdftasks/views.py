from .models import EmployeeDetails
from .serializers import EmployeeDetailsSerializer
import pandas as pd
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.views import View
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas



class extractdata(APIView):
    def post(self,request):
        file=request.FILES.get('file')

        if not file:
            return response('no file uploaded')

        try:
            if file.name.endswith(".csv"):
                convert_df=pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                convert_df=pd.read_excel(file)
            else:
                return Response("unsuported file format")

            for _, row in convert_df.iterrows():
                EmployeeDetails.objects.create(
                    employename=row['employename'],
                    designation=row['designation'],
                    dateofjoining=row['dateofjoining'],
                    workingproject=row['workingproject']
                )
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









