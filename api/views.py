from django.shortcuts import render
from .models import User,Daily,FoodRecord,SportsRecord,Food,Unit
from django.http import JsonResponse, HttpResponse
import requests
import json
import datetime
from requests import post
import base64

# Create your views here.

def test(request):
    '''Hello World!'''
    ret = "<p>Hello, world!</p>"
    return HttpResponse(ret)


def register(request):
    if request.method == 'POST':
        POST = json.loads(request.body)
        print(request.body,POST)
        username = POST.get('username')
        password = POST.get('password')
        time = POST.get('time')
        print(username,password,time)
        users = User.objects.filter(username__exact=username)
        if username and password and time and (not users):
            time = time.split('/')
            if len(time) == 3 and time[0].isdigit() and time[1].isdigit() and time[2].isdigit():
                year,month,day=int(time[0]),int(time[1]),int(time[2])
                date = datetime.date(year,month,day)
                user = User(username=username,password=password,time=date)
                user.save()
                return JsonResponse({'isSuccess':True})
        return JsonResponse({'isSuccess':False})
    return JsonResponse({'msg':'POST method only.'})


def log_in(request):
    if request.method == "POST":
        userExist = False
        isSuccess = False
        try:
            POST = json.loads(request.body)
            username = POST.get('username')
            password = POST.get('password')
            year = POST.get('year')
            month = POST.get('month')
            day=POST.get('day')
            date = {'year':year,'month':month,'day':day}
            if username and password:
                users = User.objects.filter(username__exact=username)
                if len(users) == 1:
                    userExist = True
                    if users[0].password == password:
                        isSuccess = True
                request.session['username'] = username
                request.session['date'] = date
        except:
            isSucess=False
        return JsonResponse({'userExist':userExist,'isSuccess':isSuccess})
    return JsonResponse({'msg':'POST method only.'})


def log_out(request):
    if not(request.method == "POST"):
        return JsonResponse({'msg':'POST method only.'})
    loggedIn = True
    try:
        request.session['username']
        del(request.session['username'])
        del(request.session['date'])
    except:
        loggedIn = False
    return JsonResponse({'loggedIn':loggedIn})


#600:not logged in
#601:invalid date
#602:invalid calorie
#603:invalid meals
#604:invalid sports
def save_daily_record(request):
    if not(request.method == 'POST'):
        return JsonResponse({'msg':'POST method only.'})
    #exception handling
    try:
        username = request.session['username']
        print(request.session)
    except:
        return JsonResponse({'status':'600','msg':'Not Logged In'})
    POST = json.loads(request.body)
    breakfast,lunch,dinner,snack,sports,calorieLeft,year,month,date = POST['breakfast'],POST['lunch'],POST['dinner'],POST['snacks'],POST['calorieLeft'],POST['year'],POST['month'],POST['day']
    #date
    try:
        date = datetime.date(year,month,day)
    except:
        return JsonResponse({'status':'601','msg':'Invalid Date'})
    
    #calorieLeft
    try:
        calorieLeft = int(calorieLeft)
    except:
        return JsonResponse({'status':'602','msg':'Invalid Calorie'})
    
    #meals
    try:
        breakfasts = []
        for dish in breakfast:
            name, calorie, unitName, quantity = dish['name'],dish['calorie'],dish['unitName'],dish['quantity']
            breakfasts.append([name,int(calorie),uniName,int(quantity)])
        lunches = []
        for dish in lunch:
            name, calorie, unitName, quantity = dish['name'],dish['calorie'],dish['unitName'],dish['quantity']
            lunches.append([name,int(calorie),uniName,int(quantity)])
        dinners = []
        for dish in dinner:
            name, calorie, unitName, quantity = dish['name'],dish['calorie'],dish['unitName'],dish['quantity']
            dinners.append([name,int(calorie),uniName,int(quantity)])
        snacks = []
        for dish in lunch:
            name, calorie, unitName, quantity = dish['name'],dish['calorie'],dish['unitName'],dish['quantity']
            snacks.append([name,int(calorie),uniName,int(quantity)])
    except:
        return JsonResponse({'status':'603','msg':'Invalid Meals'})
    
    #sports
    try:
        name,calorie,unitName,quantity = POST['sports']['name'],int(POST['sports']['calorie']),POST['sports']['unitName'],int(POST['sports']['quantity'])
    except:
        return JsonResponse({'status':'604','msg':'Invalid Sports'})
    
    #save records
    daily = Daily()
    daily.name,daily.date,daily.calorieLeft = username,date,calorieLeft
    daily.save()
    
    recordID = daily.ID
    sports_record = SportsRecord()
    sports_record.recordID,sports_record.name,sports_record.calorie,sports_record.unitName,sports_record.quantity = recordID,name,calorie,unitName,quantity
    sports_record.save()
    
    meals = ['breakfast','lunch','dinner','snacks']
    for (name, calorie, unitName, quantity),meal in zip(breakfasts,snacks):
        food_record = FoodRecord()
        food_record.recordID, food_record.meal, food_record.name, food_record.calorie, food_record.unitName, food_record.quantity = recordID, meal, name, calorie, unitName, quantity
        food_record.save()


def parse_image(request):
    if not (request.method == 'POST'):
        return JsonResponse({'msg':'POST method only.'})
    POST = json.loads(request.body)
    image = POST.get("image")#bytes with base24 encoding
    type_ = POST.get('type')
    if type_ == '正餐':
        #baidu dishes recognition
        #get access token
        client_id = "G9WMT75KgefElN5noRGprWdZ"
        client_secret = "d6xbeKOiY0r3nZNcPpgFUuzGeU9chk0L"
        url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id='+client_id+'&client_secret='+client_secret
        response = post(url)
        content = json.loads(str(response.content,encoding='utf-8'))
        access_token = content['access_token']
        #get calorie(per 100g)
        url = 'https://aip.baidubce.com/rest/2.0/image-classify/v2/dish'
        headers = {'Content-Type':"application/x-www-form-urlencoded"}
        data = {"access_token":access_token,"image":image,"top_num":"5"}
        response = post(url,data=data, headers=headers)
        response = json.loads(response.text)
        ret = []
        for record in response['result']:
            name,calorie,probability = record.get('name'),record.get('calorie'),float(record.get('probability'))
            if calorie:
                calorie = int(calorie)/100
            ret.append({'name':name,'caloriePerGram':calorie,'probability':probability,'unitList':[]})
        return JsonResponse(ret,json_dumps_params={'ensure_ascii':False},safe=False)
    elif type_ == '零食':
        #local model
        #Baidu OCR
        image = base64.b64decode(image)
        file = open('temp.jpg','wb')
        file.write(imgdata)
        file.close()
        #process with OCR
    else:
        return JsonResponse({'msg':'Unsupported meal.'})

def date_range(begin_date,end_date):
    date_list = []
    while begin_date <= end_date:
        date_list.append(begin_date)
        begin_date += datetime.timedelta(days=1)
    return date_list
    
#600:not logged in

def get_statistics(request):
    '''Get Statistics since Registration'''
    if request.method != 'GET':
        return JsonResponse({'msg':'GET method only.'})
    try:
        username = request.session['username']
    except:
        return JsonResponse({'status':'600','msg':'Not Logged In'})
    #iterate over the date to get the statistics
    start_date = User.objects.filter(username__exact=username)[0].time
    end_date = datetime.date.today()
    dates = date_range(start_date,end_date)
    print(start_date,end_date)
    username = User.objects.get(username=username)
    daily_records = Daily.objects.filter(username__exact=username)
    statistics = []
    for date in dates:
        daily_record = daily_records.filter(date__exact=date)
        MAX_CALORIE = 1730
        if len(daily_record) == 0:
            calorie = MAX_CALORIE
        else:
            calorie = daily_record[0].calorieLeft
        statistics.append([{
            'year':date.year,
            'month':date.month,
            'day':date.day
        }, calorie])
    return JsonResponse({'statistics':statistics})

#600:illegal type
def get_foodlist(request):
    #Get Food List for Initialization
    if request.method != 'GET':
        return JsonResponse({'msg':'GET method only.'})
    try:
        type_ = request.GET['type']
        assert type_ in ['正餐','零食','运动']
    except:
        return JsonResponse({'status':'600','msg':'Illegal Type'})
    types = {'正餐':'dinner','零食':'snacks','运动':'sports'}
    type_ = types[type_]
    foods = Food.objects.filter(food_type__exact=type_)
    foodlist = []
    for food in foods:
        name,caloriePer100Gram,unitList = food.name,food.caloriePer100Gram,[]
        units = Unit.objects.filter(name__exact=name)
        for unit in units:
            unitName,gramPerUnit,upperLimit,step = unit.unitName,unit.gramPerUnit,unit.upperLimit,unit.step
            unitList.append({'unitName':unitName,'gramPerUnit':gramPerUnit,'upperLimit':upperLimit,'step':step})
        foodlist.append({'name':name,'caloriePer100Gram':caloriePer100Gram,'unitList':unitList})
    return JsonResponse({'foodList':foodlist},json_dumps_params={'ensure_ascii':False})