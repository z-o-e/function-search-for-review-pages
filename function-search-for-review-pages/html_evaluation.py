# note on html request stats
# non_review html request fail 29 (including error 303,401,403,500 and other unknown)

import lxml
import nltk
import re
import urllib2
import sys
import BaseHTTPServer
import csv
import unicodedata
from xgoogle import BeautifulSoup

# load non-review-page urls
non_review_urls=[]
with open('cnr.csv') as csvfile:
     nr = csv.reader(csvfile, delimiter=',')
     for row in nr:
         non_review_urls.append(row[0])

# load review-page urls
review_urls=[]
with open('cr.csv') as csvfile:
     r = csv.reader(csvfile, delimiter=',')
     for row in r:
         review_urls.append(row[0])



# def retrieve_html()
# input:
#       addr---target url
# output:
#       web_handle---handle to for retrieve html file 
#
def retrieve_html(addr):
    try:
        web_handle=urllib2.urlopen(addr)
    # deal with error 3**
    except urllib2.HTTPError,e:
        error_desc=BaseHTTPServer.BaseHTTPRequestHandler.responses[e.code][0]
        print "Cannot retrieve URL: HTTP Error Code", e.code
        return 0
        #sys.exit(1)
    # deal with error 4**
    except urllib2.URLError,e:
        print "Cannot retrieve URL:"+ e.reason[1]
        return 0
        #sys.exit(1)
    # notify other unknown errors
    except:
        print "Cannot retrieve URL: unknown error"
        return 0
        #sys.exit(1)
    return web_handle



# def html_tag_detect()
# input:
#       html---target html text
# outputs:
#       voting_link---indicator of voting link tag within target html text
#
def html_tag_detect(html):
    voting_link=0    
    links=[]
    # format original html text
    soup=BeautifulSoup.BeautifulSoup(html)
    # search div and grab only hyperlink tags
    for div in soup.findAll('div'):
        links.append(div.find('a'))
    # detect whether a hyperlink is a voting link by keywords
    for i in range(len(links)):
        detect=str(links[i])
        if 'rate' in detect or 'rating' in detect or 'vote' in detect or 'voting' in detect:
            voting_link=1
    return voting_link
    
        
    
# def html_filter()
# input:
#       element---html element
# output:
#       bool--- stripping indicator
#
def html_filter(element):
    if element.parent.name in ['style','script','[document]','head','title']:
        return False
    elif re.match(r'<!--.*-->', element):
        return False
    return True



# def clean_review(html)
# input:
#       html---html text
# output:
#       reviews---a list containing block of plain review texts
#   
def clean_review(html):
    reviews=[]
    # format raw html text
    soup=BeautifulSoup.BeautifulSoup(html)
    # strip invisible html elements
    raw_text=soup.findAll(text=True)
    semi_raw_text=filter(html_filter,raw_text)
    for i in range(len(semi_raw_text)):
        # encode and convert elements to str
        x=unicode(semi_raw_text[i])
        xx=unicodedata.normalize('NFKD',x).encode('ascii','ignore')
        # pick out blocks of text based on length limit
        # and strip uncleaned html exprs
        if len(xx)>50 and re.search(r'^<!|^http|^&nbsp;',xx)==None:
            reviews.append(xx.strip())
    return reviews



# def linguistic_count()
# input:
#       reviews---a list containing block of plain review texts
# output:
#       first_person---first_person frequencies of reviews
#       punctuation---punctuation frequencies of reviews
#       keywords---keywords frequencies of reviews
#
def linguistic_count(reviews):
    first_person_counter=0
    punctuation_counter=0
    keywords_counter=0
    total=0
    # word stats evaluation
    for item in reviews:      
        total=total+len(str(item))
        first_person_counter=first_person_counter+item.count('I ')+item.count('my ')
        punctuation_counter=punctuation_counter+item.count('!')
        keywords_counter=keywords_counter+item.count('recommend')+item.count('price')+item.count('value')+item.count('quality')+item.count('return')+item.count('poor')+item.count('happy')+item.count('best')+item.count('worst')+item.count('bad')+item.count('favorite')+item.count('like')+item.count('love')
    # frequencies calculation scaled
    if total:
        first_person=100*first_person_counter/total
        punctuation=1000*punctuation_counter/total
        keywords=1000*keywords_counter/total
    # in case of error
    else:
        first_person=None
        punctuation=None
        keywords=None
    return (first_person,punctuation,keywords)



# initiate predictors
# evaluate predictors for non_review-pages
non_review_voting_tag=[]
non_review_first_person=[]
non_review_punctuation=[]
non_review_keywords=[]
for i in range(len(non_review_urls)):
    addr=non_review_urls[i]
    if retrieve_html(addr):
        html=retrieve_html(addr).read()
        vote=html_tag_detect(html)
        non_review_voting_tag.append(vote)
        reviews=clean_review(html)
        paras=linguistic_count(reviews)
        non_review_first_person.append(paras[0])
        non_review_punctuation.append(paras[1])
        non_review_keywords.append(paras[2])
    else:
        non_review_first_person.append(None)
        non_review_punctuation.append(None)
        non_review_keywords.append(None)
        non_review_voting_tag.append(None)
    print i




# initiate predictors
# evaluate predictors for review-pages
review_voting_tag=[]
review_first_person=[]
review_punctuation=[]
review_keywords=[]
for i in range(len(review_urls)):
    addr=review_urls[i]
    if retrieve_html(addr):
        html=retrieve_html(addr).read()
        vote=html_tag_detect(html)
        review_voting_tag.append(vote)
        reviews=clean_review(html)
        paras=linguistic_count(reviews)
        review_first_person.append(paras[0])
        review_punctuation.append(paras[1])
        review_keywords.append(paras[2])
    else:
        review_first_person.append(None)
        review_punctuation.append(None)
        review_keywords.append(None)
        review_voting_tag.append(None)
    print i

# write predictors to csv files for review-pages and non-review-pages    
with open('r_html_eval.csv', 'wb') as csvfile:
    html_pred1 = csv.writer(csvfile, delimiter=',')
    for i in range(len(review_urls)):
        html_pred1.writerow([review_first_person[i],review_punctuation[i],review_keywords[i],review_voting_tag[i]])
        i+=1

with open('nr_html_eval.csv', 'wb') as csvfile:
    html_pred2 = csv.writer(csvfile, delimiter=',')
    for i in range(len(review_urls)):
        html_pred2.writerow([non_review_first_person[i],non_review_punctuation[i],non_review_keywords[i],review_voting_tag[i]])
        i+=1


