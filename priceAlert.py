from bs4 import BeautifulSoup
import requests
from fbchat import Client
from fbchat.models import *
import re
import time
import sys
from tqdm import tqdm

#### FACEBOOK CHAT BOT #####
def sjekk() :
    print("######### CHAT BOT ############ \n ")
    client = Client("FBMAIL@MAIL", "FB_PASSWORD")
    lars = 1288058845 #Example FB user ids that can be used to send a message to their profile
    cato = 525196495
    print("Own id: {}".format(client.uid))
    users = client.fetchAllUsers()
    #print(users) - Run this to see all IDs from the friendslist of the user you're logged into

######################################

    print("\n \n ########### ELKJØP DEMOVARE SJEKK ############# \n")

#Nettsiden for prishenting
    # quote_page er linken til produktet du vil overvåke
    #quote_page = "https://www.elkjop.no/product/data/ipad-og-nettbrett/15038/ipad-pro-11-2018-64-gb-wifi-cellular-solv#tab-refurbished-offers"
    quote_page = "https://www.elkjop.no/product/data/ipad-og-nettbrett/15068/ipad-pro-11-2018-64-gb-wifi-stellargra"
    page = requests.get(quote_page)
    print("\n Kobler til nettside...\n Status: "+ str(page.status_code))
    soup = BeautifulSoup(page.text, 'html.parser')

    # Finner tittel og pris
    title_box = soup.find('h1', attrs={'class': 'product-title'})
    title = title_box.text.strip()
    price_box = soup.find('div', attrs={'class': 'product-price-container'})
    price = price_box.text.strip()
    print(" Produkt: "+title+"\n Outlet Pris: "+price+" kr")




    ## FINNER UT OM DET ER TILBUD###
    offerclass = soup.find(class_="product-price align-left any-1-1 margin-1")
    seeMore = offerclass.find_all("a")
    if seeMore :
        global demovare
        demovare = True
        demo_price_box = soup.find('div', attrs={'class': 'product-price align-left any-1-1 margin-1'})
        demo_price_text = demo_price_box.text.strip()
        demo_price_half = demo_price_text #re.sub('[^0-9]', '', demo_price_text)
        demo_price =""
        for i in range(28,28+len(price)) :
            demo_price+=(demo_price_half[i])

        print("\n Demovare: Ja \n Demo pris: "+demo_price+"kr \n \n Sender varlsing på Facebook.")
        client.send(Message(text="Nå er det Demovare på "+title+"!\n\nOrdinærpris: "+price+" kr \nDemo pris: "+demo_price+"kr \n \n Link: "+quote_page), thread_id=lars, thread_type=ThreadType.USER)

        client.logout()
    else :
        demovare = False
        print(" Demovare: Nei \n \n Prøver på nytt om 2 timer..\n")
        when_to_stop = 7200
        """for i in tqdm(range(7200)):
            time.sleep(1)"""

        while when_to_stop > 0:
    		      m, s = divmod(when_to_stop, 60)
    		      h, m = divmod(m, 60)
    		      time_left = str(h).zfill(2) + ":" + str(m).zfill(2) + ":" + str(s).zfill(2)
    		      print(" "+time_left + "\r", end="")
    		      time.sleep(1)
    		      when_to_stop -= 1


        ##COUNTDOWN
        #for i in range(10,0,-1):
        #    sys.stdout.write(str(i)+' ')
        #    sys.stdout.flush()
        #    time.sleep(1)
        #    print("\n")
################################
demovare = False
while (not demovare) :
    sjekk()
