import pandas as pd
from bs4 import BeautifulSoup
import xmltodict
import requests
import json
import re
import string
import numpy as np
import newspaper
import random
import requests
from bs4 import BeautifulSoup
import newscatcherapi
from newscatcherapi import NewsCatcherApiClient
from googleapiclient.discovery import build
import google.auth.credentials


def get_synonym_list(input_keywords):
    synonym_dict = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    for keyword in input_keywords:
        url = f'https://www.thesaurus.com/browse/{keyword}'
        r = requests.get(url, headers=headers)
        
        soup = BeautifulSoup(r.content, "html.parser")
        a = soup.find_all('a',{"class" : ["css-1kg1yv8 eh475bn0", "css-1n6g4vv eh475bn0"]})
        synonyms = [word.text for word in a]
        # synonyms.append(keyword)
        synonym_dict[keyword] = synonyms
        
    return synonym_dict

def get_from_newsapi(keywords, limit):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    urls = []

    # for keyword in keywords:
    word = "+".join(keywords)
    api_key = 'ecb1cd4140d14834b4ec6368c98676fc'
    url = f'https://newsapi.org/v2/everything?q={word}&apiKey={api_key}'
    
    response = requests.get(url, verify=False)
    json_obj = response.json()
   
    link_count = 0
    for news in json_obj["articles"]:
        urls.append(news["url"])
        link_count += 1
        if link_count > limit:
            break
    # print(news["title"], news["link"])
    return urls

def get_from_newscatcher(keywords, limit):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    urls = []

    word = " ".join(keywords)
    newscatcherapi = NewsCatcherApiClient(x_api_key='6shsM896iLiAGZBQoB5kCT9lf-M74S1kID6cSg7geXc')
    
    json_obj = newscatcherapi.get_search(q=word,
                                         lang='en',
                                         countries='CA',
                                         page_size=100)
    
    link_count = 0
    for news in json_obj["articles"]:
        urls.append(news["link"])
        link_count += 1
        if link_count > limit:
            break
    # print(news["title"], news["link"])
    return urls

def get_from_youtube(keywords, limit):
    # content = []
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyA8UsMP3jlXBKylUsyfN4DAqH7ByG_mZes"

    youtube = build(api_service_name, api_version, developerKey = DEVELOPER_KEY)
    
    query = "+".join(keywords)
    order = "viewCount"

    request = youtube.search().list(
            part = "id,snippet",
            type = "video",
            q = query,
            maxResults = limit,
            order = order,
        )
    response = request.execute()
    
    # for item in response["items"]:
    #     content
    return response["items"]

def get_from_googlenews(keywords, limit):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    urls = []

    # for keyword in keywords:
    word = "+".join(keywords)
    url = 'https://news.google.com/rss/search?q='+ word +'&hl=en-US&gl=US&ceid=US:en' # crawl through google news   
    r = requests.get(url, headers=headers)
    xml_data = r.content
    dict_data = xmltodict.parse(xml_data)
    json_data = json.dumps(dict_data)
    json_obj = json.loads(json_data)
    # rj = r.json()
    link_count = 0
    for news in json_obj["rss"]["channel"]["item"]:
        urls.append(news["link"])
        link_count += 1
        if link_count > limit:
            break
    # print(news["title"], news["link"])
    return urls

def get_urls(keywords):
    limit = 5
    urls = []
    
    from_newsapi = get_from_newsapi(keywords, limit)
    from_newscatcher = get_from_newscatcher(keywords, limit)
    urls = get_from_googlenews(keywords, limit)
    
    urls.extend(from_newsapi)
    urls.extend(from_newscatcher)
    # print(news["title"], news["link"])
    return urls

def get_text(urls):  
    text = []
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    
    
    for url in urls:
        # Extract web data
        # config = newspaper.Config()
        # config.browser_user_agent = random.choice(user_agent)
        try:
            url_i = newspaper.Article(url="%s" % (url), language='en', user_agent=user_agent)
            url_i.download()
            url_i.parse()
            # print(url_i)
            text.append({'title': url_i.title,
                         'text': url_i.text,
                         'link' : url})
        except Exception as e:
            print(e)
        # Display scrapped data
        # print(len(url_i.text))
        
    return text


def removePunctuations(news_list):
    # if len(news_list) == 1:
    #     news_text = news_list['text']
    #     news_list['text'] = re.sub(r'[^\w\s]', '', news_text)
    #     news_title = news_list['title']
    #     news_list['title'] = re.sub(r'[^\w\s]', '', news_title)
    #     news_list = [news_list]
    # print("len=",len(news_list))
    for i in range(len(news_list)):
        # print(i)
        # print(news_list[1])
        news_text = news_list[i]['text']
        news_list[i]['text'] = re.sub(r'[^\w\s]', '', news_text)
        news_title = news_list[i]['title']
        news_list[i]['title'] = re.sub(r'[^\w\s]', '', news_title)
    
    return news_list



def getScore(words, priority_score, threshold, priority, keywords_dict, keywords_list):
    score = 0
    frequency_map = {}
    for keyword in keywords_dict:
        frequency_map[keyword] = 0

    for i in range(len(words)):
        for j in range(len(keywords_dict)):
            # keyword = list(keywords_dict.keys())[j]
            # lis = [keyword]+keywords_dict[keyword]
            for synonym in keywords_list[j]:
                #print(keywords_list)
                if len(synonym.split(' ')) < 2:
                    if words[i].lower() == synonym.lower():
                        frequency_map[keywords_list[j][0]] = min(threshold, frequency_map[keywords_list[j][0]] + 1)
                else:
                    l = 0
                    index = i
                    while(i < len(words) and l < len(synonym.split(' ')) and words[i].lower() == synonym.split(' ')[l].lower()):
                        i += 1
                        l += 1
                    if(l == len(synonym.split(' '))):
                        frequency_map[keywords_list[j][0]] = min(threshold, frequency_map[keywords_list[j][0]] + 1)
                    else:
                        i = index 
    
    index = 0
    for val in frequency_map.values():
        score += priority[index]*val
        index += 1
    score += priority_score*sum(list(frequency_map.values()))

    return score

def sort_list(list1, list2):
 
    zipped_pairs = zip(list2, list1)
 
    z = [x for _, x in sorted(zipped_pairs, key = lambda x : x[0],reverse=True)]
    # from collections import OrderedDict

    # sorted_dict = OrderedDict([(el, list1[el]) for el in list2])
    
    return z

# Assign url
def main(input_keywords):
    
    heading_priority = 10
    content_priority = 8
    keywords_list = []
    news_scores = []
    threshold = 10
    
    # input_keywords = ['theft', 'atm']
    urls = get_urls(input_keywords)
    print("urls exctracted")
    articles = get_text(urls)
    print(articles)
    print("text exctracted")

    news_list = articles
    news_list = removePunctuations(news_list)
    keywords_dict = get_synonym_list(input_keywords)
    priority = list(np.arange(len(keywords_dict))[::-1]+1)
    print("synonyms exctracted")
    # keywords_dict = {
    #     'atm': ['any time money', 'automatic teller machine'],
    #     'Machine Learning' : ['ml', 'ai'],
    #     'theft': ['robbery', 'steal', 'larceny'],
    #     'party': ['political', 'bjp', 'congress']
    # }  

    for j in range(len(keywords_dict)):
        keyword = list(keywords_dict.keys())[j]
        keywords_list.append([keyword]+keywords_dict[keyword])
        
    for news in news_list:
        score = 0
        score += getScore(news['text'].split(' '), content_priority, threshold, priority, keywords_dict, keywords_list)
        score += getScore(news['title'].split(' '), heading_priority, threshold, priority, keywords_dict, keywords_list)   
        news_scores.append(score)

    index = news_scores.index(max(news_scores))
    news_list = sort_list(news_list, news_scores)
    # print(news_scores)
    print('final')
    print(news_list[index])
    
    return news_list