import re
import csv

# load non-review-urls
non_review_urls=[]
with open('cnr.csv') as csvfile:
     nr = csv.reader(csvfile, delimiter=',')
     for row in nr:
         non_review_urls.append(row[0])

# load review-urls
review_urls=[]
with open('cr.csv') as csvfile:
     r = csv.reader(csvfile, delimiter=',')
     for row in r:
         review_urls.append(row[0])


# def evaluate_url()
# input:
#       addr_list---a list containing the urls
# outputs:
#       domain_indicator---a list containing the labels indicating  
#                          whether urls contain certain domains
#       key_word_indicator---a list containing the labels indicating 
#                          whether urls contain keyword 'review' 
#
def evaluate_url(addr_list):
    N=len(addr_list)
    domain_indicator=[0]*N
    keyword_indicator=[0]*N   
    for i in range(N):
        # domain names/sufix '.org', '.edu', '.gov', '.pdf'
        # likely to associate to non-review pages
        if re.search(r'\.org|\.edu|\.gov|\.pdf',str(addr_list[i])):
            domain_indicator[i]=1
        # urls include keyword 'review'
        # likely to associate to review pages
        if re.search(r'review',str(addr_list[i]),flags=re.IGNORECASE):
            keyword_indicator[i]=1
    return (domain_indicator,keyword_indicator)


# evaluate url predictor for non_review_urls and review_urls
# store resulting predictors to vectors
non_review_url_evaluations=evaluate_url(non_review_urls)
review_url_evaluations=evaluate_url(review_urls)
nr_domain=non_review_url_evaluations[0]
nr_keyword=non_review_url_evaluations[1]
r_domain=review_url_evaluations[0]
r_keyword=review_url_evaluations[1]


# write domain indicators and url keyword indicators to csv files 
with open('nr_url_eval.csv', 'wb') as csvfile:
    url_pred0 = csv.writer(csvfile, delimiter=',')
    for i in range(len(non_review_urls)):
        url_pred0.writerow([nr_domain[i],nr_keyword[i]])
        i+=1

with open('r_url_eval.csv', 'wb') as csvfile:
    url_pred1 = csv.writer(csvfile, delimiter=',')
    for i in range(len(review_urls)):
        url_pred1.writerow([r_domain[i],r_keyword[i]])
        i+=1

