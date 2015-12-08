# note on actual stats
# review url 199
# non_review url 365

import csv
import lxml
from xgoogle.search import GoogleSearch, SearchError
from amazonproduct import API



# key_words used for crawling non_review pages via Search Library built upon Google
# products_info used for feeding Amazon API and get review pages 
non_review_urls=[]
key_words=["Thatcher","Burma ethnics","Nepal Religion","slovakia population","NASA mission MARS","satellite retirement","dinosaur fossils","Amazon River","Mount Everest Base Camp","Marrianna trench","earth day","environmentalist campaign","climate changes","news terrorists","global financial crisis","marathon support","crime rate Austin","ocd symptoms","neural network failure","intellectual property violation","hydro equipment manufacturing","california tax regulation"]
review_urls=[]
products_info=[['Appliances','vacuum cleaner'],['Appliances','light'],['Appliances','fridge'],['Apparel','shirt'],['Apparel','dress'],['Baby','car seat'],['Beauty','perfume'],['Electronics','Sony'],['Electronics','Lenovo'],['Electronics','htc'],['Electronics','hp'],['Electronics','apple'],['Electronics','dell'],['Electronics','camera'],['GourmetFood','cake'],['GourmetFood','cookies'],['Music','soul'],['Music','rock'],['Music','pop'],['Music','classical'],['SportingGoods','shorts'],['SportingGoods','tank'],['Shoes','leather'],['Shoes','vans'],['Shoes','black'],['Watches','sports'],['Watches','steel']]


# crawl non-review-page-urls from google and store in list 'non_review_urls'
for i in range(len(key_words)):
    try:
         gs=GoogleSearch(key_words[i])
         gs.results_per_page=100
         results=gs.get_results()
         for res in results:
             print res.title.encode('utf8')
             print res.url.encode('utf8')
             non_review_urls.append(res.url.encode('utf8'))
    except SearchError,e:
         print "Search failed: %s" %e
    print i
     

# crawl review-page-urls from Amazon API
for i in range(len(products_info)):
    # search items via Amazon API
    for node in api.item_search(products_info[i][0], Keywords=products_info[i][0],ResponseGroup='Large',IncludeReviewsSummary=True):
        total_results = node.Items.TotalResults.pyval
        total_pages = node.Items.TotalPages.pyval
        try:
            current_page = node.Items.Request.ItemSearchRequest.ItemPage.pyval
            if current_page==10:
                print "\nNo more pages to show: " + "maximum number of pages is 10"
                break
        except AttributeError:
            current_page = 1
    
    # check if review exist and format review-page-urls for associated products         
    for product in node.Items.Item:
        print 'http://www.amazon.com/gp/product/'+ str(product.ASIN) + '\n',
        if product.CustomerReviews.HasReviews:
            review_urls.append(product.CustomerReviews.IFrameURL)    
    # keep track of the process
    i+=1
    print i


# store non-review-page-urls to 'cnr.csv'
with open('cnr.csv', 'wb') as csvfile:
    write_non_review_urls = csv.writer(csvfile, delimiter=',')
    for val in non_review_urls:
        write_non_review_urls.writerow([val])

# store review-page-urls to 'cr.csv'        
with open('cr.csv', 'wb') as csvfile:
    write_review_urls = csv.writer(csvfile, delimiter=',')
    for val in review_urls:
        write_review_urls.writerow([val])
