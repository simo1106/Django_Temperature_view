from django.shortcuts import render
from django.http import HttpResponse
from django.forms.models import model_to_dict

def homepage(request):
    return HttpResponse("Hello world!")

from .models import temperature
def Temperature(request):
    resultList = temperature.objects.all().order_by('timestamp')
    for item in resultList:
        print(model_to_dict(item))
    data_count = len(resultList)
    print(f"Total data count:{data_count}")
    status = True
    errormessage = ""
    if not resultList:
        status = False
        errormessage = "No data found."
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
