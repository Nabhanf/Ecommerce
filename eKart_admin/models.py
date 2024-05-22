from django.db import models

class Admin_login(models.Model):
    username=models.CharField(max_length=150)
    password=models.CharField(max_length=10)

    class Meta:
        db_table='adminlogin_tb'

class Category(models.Model):
    categoryname=models.CharField(max_length=250)
    description=models.TextField()
    image=models.ImageField(upload_to='category/')

    class Meta:
        db_table='category_tb'
    