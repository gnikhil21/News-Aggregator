import re
import string
import numpy as np
import newspaper

# Assign url
urls = get_urls(input_keywords)
articles = get_text(urls)
# urls = ['https://www.geeksforgeeks.org/top-5-open-source-online-machine-learning-environments/',
#         'https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjI56vC3MH9AhUP8zgGHbryB0sQvOMEKAB6BAgOEAE&url=https%3A%2F%2Fwww.thehindu.com%2Fnews%2Finternational%2Fquad-foreign-ministers-take-aim-at-russia-and-china%2Farticle66577074.ece&usg=AOvVaw3G125a3AJkzEiMjMpC3Tt_',
#         'https://www.thehindu.com/news/national/better-infrastructure-has-put-remote-indian-villages-on-tourist-map-pm-modi/article66575058.ece',
#         'https://www.thehindu.com/sci-tech/health/avoid-antibiotics-for-seasonal-cold-and-cough-says-indian-medical-association-amid-rising-cases/article66579326.ece',
#         ]

# Extract web data
# articles = []
# for url in urls:
#     article = newspaper.Article(url="%s" % (url), language='en')
#     article.download()
#     article.parse()
#     articles.append({
#         'title': article.title,
#         'text': article.text
#     })

# Display scrapped data
#articles[0]







news_list = articles
keywords_dict = get_synonym_list(input_keywords)
# keywords_dict = {
#     'atm': ['any time money', 'automatic teller machine'],
#     'Machine Learning' : ['ml', 'ai'],
#     'theft': ['robbery', 'steal', 'larceny'],
#     'party': ['political', 'bjp', 'congress']
# }  



def removePunctuations(news_list):
    for i in range(len(news_list)):
        news_text = news_list[i]['text']
        news_list[i]['text'] = re.sub(r'[^\w\s]', '', news_text)
        news_title = news_list[i]['title']
        news_list[i]['title'] = re.sub(r'[^\w\s]', '', news_title)
    
    return news_list


heading_priority = 10
content_priority = 8

priority = list(np.arange(len(keywords_dict))[::-1]+1)


def getScore(words, content_type):
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
                    while(l < len(synonym.split(' ')) and words[i].lower() == synonym.split(' ')[l].lower()):
                        i += 1
                        l += 1
                    if(l == len(synonym.split(' '))):
                        frequency_map[keywords_list[j][0]] = min(threshold, frequency_map[keywords_list[j][0]] + 1)
                    else:
                        i = index 
    
    if content_type == 'heading_priority':
        score += heading_priority*sum(list(frequency_map.values()))
    else:
        score += content_priority*sum(list(frequency_map.values()))

    return score


news_list = removePunctuations(news_list)
keywords_list = []
news_scores = []
threshold = 10

for j in range(len(keywords_dict)):
    keyword = list(keywords_dict.keys())[j]
    keywords_list.append([keyword]+keywords_dict[keyword])
    
for news in news_list:
    score = 0
    score += getScore(news['text'].split(' '), 'content_priority')
    score += getScore(news['title'].split(' '), 'heading_priority')   
    news_scores.append(score)

index = news_scores.index(max(news_scores))
# print(news_scores)
print(news_list[index])