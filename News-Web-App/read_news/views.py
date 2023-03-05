from django.shortcuts import render,redirect
from newsapi import NewsApiClient
from GoogleNews import GoogleNews
from django.http import HttpResponse
from news import settings
from .newsgator import final_file

def home(request):
    
    if request.method == 'GET':
        return render(request, 'test.html')

    elif request.method == 'POST':
        keywords = request.POST['keywords'].strip().split(',')
        i = 0
        while i < len(keywords):
            keywords[i] = keywords[i].strip()
            if(len(keywords[i]) == 0):
                keywords.pop(i)
                i = i-1
            i = i+1
            
        print(keywords)
        
        
        result = final_file.main(keywords)
        page={"others" : [],
              "keywords" : request.POST['keywords']}
        
        for i in result:
            page["others"].append({
                "title": i['title'],
                "des"  : i['text'],
                "url"  : i['link'],
            })

        page["main"] = page["others"][0]
        page["others"].pop(0)
        return render(request,'index.html',page)

