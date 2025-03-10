'''
This example shows how to read a paragraph in Wikipedia after a header
'''
import requests
from bs4 import BeautifulSoup
import time
import re

url_base = 'https://en.wikipedia.org/wiki/'

success = False
while True:
    topic = input('Which topic would you like to look for? ')

    start_time = time.time()
    topic = topic.split()
    for idx,word in enumerate(topic):
        topic[idx]= word.casefold()[0].capitalize()+word.casefold()[1:]
    topic ='_'.join(topic)
    
    response = requests.get(url_base+topic)

    # Check if the status code is 200, indicating a successful request
    if response.status_code == 200:
        print("\nPage: {0}".format(url_base+topic))
        print(f"fetched in {time.time() - start_time} seconds")
        success =True
    else:
        print("Unable to find the topic, try again\n")
    if success:
        break
soup = BeautifulSoup(response.text, 'html.parser')

# Extract all titles defined with header h2
h2_titles = soup.find_all('h2')

while True:
    print("\nWhich topic would you like to read: ")
    for idx, title in enumerate(h2_titles):
        if idx==0: continue
        print(str(idx)+'. ', title.text)
    out = False
    while True:
        idx = input('Which header do you want to read?(q+enter to quit) ')
        if idx=='q':
            print("Have a nice day, human!")
            out = True
            break
        elif re.match(r'^\d+$',idx)!=None:
            if len(h2_titles) > int(idx) and int(idx)>=0:
                break
            else:
                print("Wrong value, try again\n")
        else:
            print("Wrong value, try again\n")
    if out:
        break
    s = h2_titles[int(idx)]

    text = ''
    tmp  = s
    if int(idx)==len(h2_titles)-1:
        previous_p = None
    else:
        previous_p = h2_titles[int(idx)+1]

    print('\n'+idx+'. '+h2_titles[int(idx)].text+":\n")

    while True:
        tmp = tmp.find_next(["p","ul","h2"])
        if tmp==previous_p:
            break
        tmp_str = tmp.get_text().strip().replace('\n', ' ')
        
        reg_ppattern = r'\[\d+\]'
        cleaned_pragraph= re.sub(reg_ppattern,'',tmp_str)
        text += cleaned_pragraph
    print(text)