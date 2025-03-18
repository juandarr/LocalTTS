"""
Note: on Linux you need to run this as well: apt-get install portaudio19-dev

pip install -U kokoro-onnx sounddevice

wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
python examples/with_stream.py
"""
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

ps = ''
tmp = h2_title[1]
for i in range(4):
    tmp = tmp.find_next("p")
    tmp_str = tmp.get_text().strip().replace('\n', ' ')
    reg_ppattern = r'\[\d+\]'
    cleaned_paragraph= re.sub(reg_ppattern,'',tmp_str)
    ps += '. '+ cleaned_paragraph

text = ps
import requests

response = requests.post(
    "http://localhost:8880/v1/audio/speech",
    json={
        "input": text,
        "voice": "af_bella",
        "response_format": "pcm"
    },
    stream=True
)

# Stream to speakers (requires PyAudio)
import pyaudio
player = pyaudio.PyAudio().open(
    format=pyaudio.paInt16, 
    channels=1, 
    rate=24000, 
    output=True
)

for chunk in response.iter_content(chunk_size=1024):
    if chunk:
        player.write(chunk)
