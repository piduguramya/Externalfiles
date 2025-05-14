from .models import EmployeeDetails
from rest_framework import serializers

class EmployeeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model:EmployeeDetails
        fields: "__all__"