from django.contrib import admin
from .models import Food,Unit,User,Daily,FoodRecord,SportsRecord

# Register your models here.
admin.site.register(Food)
admin.site.register(Unit)
admin.site.register(Daily)
admin.site.register(FoodRecord)
admin.site.register(SportsRecord)
admin.site.register(User)