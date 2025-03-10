"""
Note: on Linux you need to run this as well: apt-get install portaudio19-dev

pip install -U kokoro-onnx sounddevice

wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python streamAudio.py
"""
import sounddevice as sd
from kokoro_onnx import Kokoro
import asyncio

import requests
from bs4 import BeautifulSoup
import time
import re

url = 'https://en.wikipedia.org/wiki/Unix'

start_time = time.time()
response = requests.get(url)

# Check if the status code is 200, indicating a successful request
if response.status_code == 200:
    print(f"Page fetched in {time.time() - start_time} seconds")
else:
    print("Unable to download the page")

soup = BeautifulSoup(response.text, 'html.parser')

# Extract the title and  paragraph
h2_title = soup.find_all('h2')

text = ''
tmp = h2_title[3]
# Read first four paragraphs after fourth h2 header
for i in range(4):
    tmp = tmp.find_next("p")
    tmp_str = tmp.get_text().strip().replace('\n', ' ')
    reg_ppattern = r'\[\d+\]'
    cleaned_paragraph= re.sub(reg_ppattern,'',tmp_str)
    text += '. '+ cleaned_paragraph

async def main():
    print("Loading model...")
    kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
    print("Model loaded")
    print("Creating stream...")
    stream = kokoro.create_stream(
        text,
        voice="af_sky",
        speed=1.0,
        lang="en-us",
    )

    count = 0

    async for samples, sample_rate in stream:
        count += 1
        print(f"Playing audio stream ({count})...")
        sd.play(samples, sample_rate)
        sd.wait()

asyncio.run(main())
