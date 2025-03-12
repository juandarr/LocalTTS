'''
This example shows how to read a paragraph in Wikipedia after a header
'''
import requests
from bs4 import BeautifulSoup
import time
import re

import sounddevice as sd
from kokoro_onnx import Kokoro
import asyncio

# Removes warning logs
import onnxruntime as ort
ort.set_default_logger_severity(3)

async def main(txt: str):
    print("\nLoading model...")
    kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    print("Model loaded")
    print("Creating stream...")
    stream = kokoro.create_stream(
        txt,
        voice="af_bella",
        speed=1.0,
        lang="en-us",
    )

    count = 0
    print(f"Playing audio stream ...")
    async for samples, sample_rate in stream:
        count += 1
        print(f"               stream ({count})...")
        sd.play(samples, sample_rate)
        sd.wait()

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
    out = False
    if success:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title with header h1
        h1_title = soup.find_all('h1')
        # Extract all titles defined with header h2
        h2_titles = soup.find_all('h2')
        h2_titles[0]=h1_title[0]

        while True:
            print(f"\n{h1_title[0].text}")
            print("\nWhich chapter would you like to read: ")
            for idx, title in enumerate(h2_titles):
                print(str(idx)+'. ', 'Summary' if idx==0 else title.text)
            while True:
                idx = input('Which header do you want to read?[q:quit,n:another topic] ')
                if idx=='q':
                    out = True
                    break
                elif idx=='n':
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
                next_h2 = None
            else:
                next_h2 = h2_titles[int(idx)+1]

            print('\n'+idx+'. '+h2_titles[int(idx)].text+":\n")

            while True:
                filters = ["p","h4","h3","h2"]
                if int(idx)!=0:
                    filters.append("ul")
                tmp = tmp.find_next(filters)
                
                if tmp==next_h2:
                    break
                tmp_str = tmp.get_text().strip().replace('\n', ' ')

                reg_ppattern = r'\[\d+\]'
                cleaned_paragraph= re.sub(reg_ppattern,'',tmp_str)
                end = ' ' if (len(cleaned_paragraph)==0 or (cleaned_paragraph[-1]=='.')) else '. '
                text += cleaned_paragraph + end
            print(text)

            asyncio.run(main(text))
    if out:
        print("Have a nice day, human!")
        break
