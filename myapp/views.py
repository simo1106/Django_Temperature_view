from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict

def homepage(request):
    return HttpResponse("Hello world!")

from .models import temperature
def Temp(request):
    resultList = temperature.objects.all().order_by('timestamp') # 時間戳擺在最上面
    # 搜尋功能
    search_keyword= request.GET.get('site_search')
    if search_keyword:
        resultList = resultList.filter(sensor_id__icontains=search_keyword)
    
    #總筆
    data_count = resultList.count()
    status = True if data_count > 0 else False
    errormessage = "找不到" if not status else ""

    # return HttpResponse("Hello, this is the index page.")
    return render(request, 'Temperature_v1.html', {'resultList': resultList,
                                             'status': status,
                                             'errormessage': errormessage,
                                             'data_count': data_count})
# 'resultList': resultList,'status': status,'errormessage': errormessage,'data_count': data_count
# 上面是傳遞給html的參數, 可在html{{ 變數名稱 }}訪問。
# status 通常是一個布林值（True/False），它的作用是控制網頁的顯示切換。
# errormessage 是字串, 用來儲存錯誤訊息, 當status為false時, 使用者可以在網頁上面看到錯誤代碼。
# data_count 是整數, 用來計算資料庫有多少筆資料, 網頁上可以顯示資料總筆數。

from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def post(request):
    if request.method == 'POST':
        myid= request.POST.get('myid')
        sensor_id= request.POST.get('sensor_id')
        temperature= request.POST.get('temperature')
        humidity= request.POST.get('humidity')
        timestamp= request.POST.get('timestamp')
        print(f"Received POST data: myid={myid}, sensor_id={sensor_id}, temperature={temperature}, humidity={humidity}, timestamp={timestamp}")
        add = temperature(myid=myid, sensor_id=sensor_id, temperature=temperature, humidity=humidity, timestamp=timestamp)
        add.save()        

        return redirect('Temp')
    else:
        return render(request, 'post.html')
    
def delete(request, id):
    print(id)
    # 成功
    obj_data = temperature.objects.get(myid=id)
    if request.method == 'POST':
        obj_data.delete()
        return redirect('Temperature')
    # 失敗
    else:
        obj_data = temperature.objects.get(myid=id)
        print(model_to_dict(obj_data))
        return render(request, 'delete.html', {'obj_data': obj_data})

# web API 加入Json格式
from django.http import JsonResponse
@csrf_exempt
def API_Temperature(request):
    All_data= temperature.objects.all().order_by('myid')
    list_data= list(All_data.values()) #將 querySet 轉為 list；物件變成字典
    return JsonResponse(list_data, safe=False) # 與允許dict

def API_post(request, id):
    try:
        obj= temperature.objects.get(myid=id)
        # print(model_to_dict(obj))
        list_data= model_to_dict(obj) # object 打包成 python字典 (key, value) 之後才能繼續打包Jsone純文字格式
        return JsonResponse(list_data) #預設safe= False
    except:
        # return HttpResponse("False")
        return JsonResponse({"message": "data not found"}, status=404)

@csrf_exempt    
def updateList(request, id):
    print(f"id:{id}")
    if request.method   != "POST":
        return HttpResponse("這個 API 只接受 POST", status=404)

    try:
        myid = request.POST.get('myid')
        sensor_id = request.POST.get('sensor_id')
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        timestamp = request.POST.get('timestamp')

        print(f"Received POST data: myid={myid}, sensor_id={sensor_id}, temperature={temperature}, humidity={humidity}, timestamp={timestamp}")

        temperature.objects.create(
            myid=myid,
            sensor_id=sensor_id,
            temperature=temperature,
            humidity=humidity,  
            timestamp=timestamp
        )

        return HttpResponse("資料已寫入資料庫")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)