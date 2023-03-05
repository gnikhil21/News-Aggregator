from django.shortcuts import render,redirect
from newsapi import NewsApiClient
from GoogleNews import GoogleNews
from django.http import HttpResponse
from news import settings

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

        googlenews = GoogleNews(lang='en', period='1d')

        googlenews.search(keywords[0])
        results = googlenews.results(sort=True)
        page={"others" : [],
              "keywords" : request.POST['keywords']}

        for i in results:
            page["others"].append({
                "title": i["title"],
                "des"  : i["desc"]+'DENVER — Preauthorize the Denver Police Department to track your vehicle in case it\'s ever stolen: That is the gist of the department\'s new "DenverTrack" program, as Colorado leads the entire nation for car thefts per capita. During the program\'s reveal Friday, Lieuetant Ryan Harris addressed the first question that probably popped into everyone\'s mind.\"No. \nIf your car is not reported stolen, we will not, we cannot track you,\" he said Anyone who lives in Denver and has a tracking device in their vehicle — like OnStar, Bluelink, an Apple AirTag, etc., — can participate in the program by registering on Denver PD\'s website. There, you will be asked to provide your vehicle information, proof that you are the registered owner, and preauthorize the department to access the device.',
                "img"  : i["img"],
                "url"  : i["link"],
            })

        page["main"] = page["others"][0]
        return render(request,'index.html',page)

