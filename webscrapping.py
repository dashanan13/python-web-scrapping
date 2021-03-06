from urllib.request import urlopen
from datetime import datetime
from google.cloud import storage
import csv 

def parsehtml(parseURL, nameStr, priceStr):
    
    url = parseURL
    page = urlopen(url)                                      #Opens the URL for query
    
    html_bytes = page.read()                                 #reads the URL
    html = html_bytes.decode("utf-8")                        #decodes the read HTML
    
    html_list = html.split("\n")                             #splits the html into lines using \n
    
    tname = []
    tcost = []
    
    for htmlcount in range(len(html_list)):                              #loop through individual lines of HTML

        if (html_list[htmlcount].find(nameStr) != -1):      
            tname.append(((str(html_list[htmlcount])).strip())[len(nameStr): ((str(html_list[htmlcount])).strip()).find('</div>')])
            
        if (html_list[htmlcount].find(priceStr) != -1):      
            tcost.append((str(html_list[htmlcount+1])).strip().replace('\xa0', ' '))
            
    return(dict(zip(tname, tcost)))

def parseforURLs(parseURL, searchString, appendURL, filterSTR):
    
    fSTR = filterSTR if (len(filterSTR) > 0) else list('/')
    
    url = parseURL
    page = urlopen(url)                                      #Opens the URL for query
    
    html_bytes = page.read()                                 #reads the URL
    html = html_bytes.decode("utf-8")                        #decodes the read HTML
    
    html_list = html.split("\n")                             #splits the html into lines using \n
    
    product_catagories = []                                
    for htmlline in html_list:                              #loop through individual lines of HTML
        # search for specificed string
        if ((htmlline.find(searchString) != -1)):
            #filtering to avoid any other pages than products
            for sStr in fSTR:
                if ((htmlline.find(sStr) != -1)):
                    #making a list of avaiable URL
                    product_catagories.append(appendURL + htmlline.split('"')[1])

    return product_catagories

print("Parsing home URL")
product_catagories = parseforURLs("https://oda.com/no/products", "<a href=\"/", "https://oda.com", ['products', 'categories'])

print("Parsing for level 2 URL")
# Parsing all the URL to get any other sub URL etc
pcatagories= product_catagories
for catindex in range(len(pcatagories)):
    #print("Using URL: " + pcatagories[catindex] + " " + str(catindex))
    product_catagories.extend(parseforURLs(pcatagories[catindex], "<a href=\"/", "https://oda.com", ['products', 'categories']))

backup = product_catagories
#removing duplicates
backup = list(set(backup))
#print(len(backup))

product_catagories = backup

print("Parsing for level 3 URL")
# Parsing all the URL to get any other sub URL etc
pcatagories= product_catagories

for catindex in range(len(pcatagories)):
    #print("Using URL: " + pcatagories[catindex] + " " + str(catindex))
    product_catagories.extend(parseforURLs(pcatagories[catindex], "<a href=\"/", "https://oda.com", ['products', 'categories']))
#   print(len(product_catagories))


backup = product_catagories
#removing duplicates
backup = list(set(backup))
#print(len(backup))

product_catagories = backup

print("Assembling Data from each HTML page")
product_listings = []
for urlindex in range(len(product_catagories)):
    #print("URL : " + str(urlindex) + " >> " + product_catagories[urlindex])
    itemsnprices = parsehtml(product_catagories[urlindex],  "<div class=\"name-main wrap-two-lines\">", "<p class=\"price label label-price\">")
    
    for name, price in itemsnprices.items():
        product_listings.append([product_catagories[urlindex], name, price])
        
product_listings

#Writing to CSV
print("Writing to local file")

# field names 
fields = ['Product', 'Cost', 'URL'] 
    
# data rows of csv file 
rows = product_listings
    
# name of csv file 
filename = "product_listings.csv"
    
# writing to csv file 
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile)         
    # writing the fields 
    csvwriter.writerow(fields) 
    # writing the data rows 
    csvwriter.writerows(rows)

#Uploading to a GCP bucket
print("Uploading to a GCP Bucket")
storage_client = storage.Client.create_anonymous_client()

#!!!!! THIS BUCKET NAME IS FROM MY GCP SUBSCRIPTION, USE YOUR OWN BUCKET!!!!!
bucketname = 'webscrapeme'
targetblobfilename = "productlistings-" + (str(datetime.now()).replace(" ", "-").replace(":", "-").split("."))[0] + ".csv"

bucket = storage_client.bucket(bucketname)
blob = bucket.blob(targetblobfilename)

blob.upload_from_filename('product_listings.csv')

print("Report can be accessed at: " + str(blob.public_url))