# in this file is downloaded and flder is also created .
from csv import DictReader
import os
import requests  #to sent GET requests
from bs4 import BeautifulSoup  # pip install bs4 #to parse html(getting data out from html, xml or other markup languages)
import re

# user can input a search keyword and the count of images required
# download images from google search image
with open('good_reads_books_dataset.csv', 'r', encoding='utf-8') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for index, row in enumerate(csv_dict_reader):
        Google_Image = \
            'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

        # The User-Agent request header contains a characteristic string 
        # that allows the network protocol peers to identify the application type, 
        # operating system, and software version of the requesting software user agent.
        # needed for google search        
        u_agnt = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
        }

        a =  row['title']
        result = re.sub('[\W_]+', '', a)  #Remove all special characters, punctuation and spaces from string
        Image_Folder = 'Images_1'  +"/" +str(index) + result
        def main():     # it will check wether image folder is there if not it will create one 
            if not os.path.exists(Image_Folder):
                os.mkdir(Image_Folder)
            download_images()

        def download_images():
            d1 = row['title']
            data = row['title'] + " by" + row['authors'] + " isbn" + row['isbn'] + "publisher" + row['publisher']
            num_images = int(2)
            
            print('Searching Images....',index,row['bookID'], row['title'])
            
            search_url = Google_Image + 'q=' + data #'q=' because its a query
            
            # request url, without u_agnt the permission gets denied
            response = requests.get(search_url, headers=u_agnt)
            html = response.text  #To get actual result i.e. to read the html data in text mode
            
            # find all img where class='rg_i Q4LuWd'
            b_soup = BeautifulSoup(html, 'html.parser') #html.parser is used to parse/extract features from HTML files
            results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})
            
            #extract the links of requested number of images with 'data-src' attribute and appended those links to a list 'imagelinks'
            #allow to continue the loop in case query fails for non-data-src attributes
            count = 0
            imagelinks= []
            for res in results:
                try:
                    link = res['data-src']
                    imagelinks.append(link)
                    count = count + 1
                    if (count >= num_images):
                        break
                    
                except KeyError:
                    continue
            
            print(f'Found {len(imagelinks)} images')
            print('Start downloading...',index , row['bookID'], row['title'] )

            for i, imagelink in enumerate(imagelinks):
                # open each image link and save the file
                response = requests.get(imagelink)
                
                imagename = Image_Folder + '/' + result + str(i+1) + '.jpg'
                with open(imagename, 'wb') as file:
                    file.write(response.content)


        

        if __name__ == '__main__':
            main()