from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50,primary_key=True)
    password = models.CharField(max_length=50)
    time = models.DateField()

class Daily(models.Model):
    ID = models.AutoField(primary_key=True)
    username = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField()
    calorieLeft = models.IntegerField()
    class Meta:
        unique_together = (('username','date'))
    
class FoodRecord(models.Model):
    ID = models.AutoField(primary_key=True)
    recordID = models.ForeignKey(Daily,on_delete=models.CASCADE)
    meal = models.CharField(max_length=10,choices=[('breakfast','breafast'),('lunch','lunch'),('dinner','dinner'),('snacks','snack')])
    name = models.CharField(max_length=100)
    calorie = models.IntegerField()
    unitName = models.CharField(max_length=50)
    quantity = models.IntegerField()
    
class SportsRecord(models.Model):
    ID = models.AutoField(primary_key=True)
    recordID = models.ForeignKey(Daily,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    calorie = models.IntegerField()
    unitName = models.CharField(max_length=50)
    quantity = models.IntegerField()

class Food(models.Model):
    name = models.CharField(max_length=50,primary_key=True)
    caloriePer100Gram = models.IntegerField()
    food_type = models.CharField(max_length=10,choices=[('dinner','dinner'),('snacks','snacks'),('sports','sports')])

class Unit(models.Model):
    name = models.ForeignKey(Food,on_delete=models.CASCADE)
    unitName = models.CharField(max_length=50)
    gramPerUnit = models.IntegerField()
    upperLimit = models.IntegerField()
    step = models.IntegerField()
    class Meta:
        unique_together = (('name','unitName'))
