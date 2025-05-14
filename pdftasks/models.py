from django.db import models


class  EmployeeDetails(models.Model):
    employeid=models.AutoField(primary_key=True)
    employename=models.CharField(max_length=255)
    designation=models.CharField(max_length=255)
    dateofjoining=models.DateTimeField(auto_now_add=True)
    workingproject=models.CharField(max_length=500)
    

    def __str__(self):
        return self.employename




