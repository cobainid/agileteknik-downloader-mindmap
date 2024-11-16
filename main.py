import requests
import json
import time
import random
from colorama import Fore, Style
from pathlib import Path

url = "https://agileteknik.com/mindmap/download/{id}/{title}"

def print_error(message):
    print(f"{Fore.RED}Error: {message} {Style.RESET_ALL}")
    
def print_success(message):
    print(f"{Fore.GREEN}Success: {message} {Style.RESET_ALL}")

def check_file_size(response):
    # check file size
    if response.headers.get("Content-Length"):
        file_size = int(response.headers.get("Content-Length"))
        # if file size is less than 20bytes
        if file_size < 1024:
            print_error("Mindmap file is too small.")
            return False
    return True


def check_file_type(response):
    # check file size
    if response.headers.get("Content-Type")== "text/plain; charset=UTF-8":
        return 1
    elif response.headers.get("Content-Type")== "application/json":
        return 2
    else:
        print_error(f"Mindmap file is not in Text format: {response.headers.get("Content-Type")}")
        return 3
    
def save_response_to_file(id, content, tipe_file):
    json_mindmap = json.loads(content)
    # create folder
    folder_name = json_mindmap['root'][0]['content']
    folder_name = "output/" + folder_name
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    
    file_name = f"{tipe_file}_{id}.json"
    full_path=f"{folder_name}/{file_name}"
    
    f = open(full_path, "w")
    f.write(content.decode("utf-8"))
    f.close()
    return full_path

    

def get_mindmap_url(id, title):
    try:
        response = requests.get(url.format(id=id, title=title))
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # check file size
        if check_file_size(response) == False:
            return None
            
        # check content type
        tipe_file = check_file_type(response)
        if tipe_file == 3:
            return None
        
        # Download file and save to temp file.json
        file_name = save_response_to_file(id, response.content, tipe_file)
        print_success(f'Berhasil mendapatkan mindmap dengan id {id}, di save ke {file_name}')
    except requests.exceptions.RequestException as e:
        print_error(f"{e}")
        return None

# 12000 - 12100
# 12100 - 12200
# 12200 - 12300
# 12300 - 12400
# 12551 - 12600 - belum selesai

# 13000 - 13100
# 13100 - 13300
# 13300 - 13600

# 23000 - 23100

for i in range(23100, 23200):
    get_mindmap_url(i, i)
    sleep_in = random.randint(3,10)
    print(f"Sleep: {sleep_in}s")
    time.sleep(sleep_in)
    
# get_mindmap_url(419,419)