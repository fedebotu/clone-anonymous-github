import requests
import os
from time import sleep
import concurrent.futures
import math

from src.utils import get_dict_vals, dict_parse

def convert_size(size_bytes):
    """Convert bytes to human readable format"""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def req_url(dl_file, max_retry=5):
    """Download file"""
    url = dl_file[0]
    save_path = dl_file[1]
    save_dir = '/'.join(save_path.split('/')[:-1])
    if not os.path.exists(save_dir) and save_dir:
        try:
            os.makedirs(save_dir)
        except OSError:
            pass
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15"
    }
    for i in range(max_retry):
        try:
            r = requests.get(url, headers=headers)
            with open(save_path, "wb") as f:
                f.write(r.content)
            return 'Downloaded: ' + str(save_path)
        except Exception as e:
            # print('file request exception (retry {}): {} - {}'.format(i, e, save_path))
            sleep(0.4)
    return 'File request exception (retry {}): {} - {}'.format(i, e, save_path)


def download_repo(config):
    """Download Anonymous Github repo"""

    url = config['url']
    save_dir = config['save_dir']
    max_conns = config['max_conns']
    max_retry = config['max_retry']

    name = url.split('/')[4]
    save_dir = os.path.join(save_dir, name)
    
    print("=====================================")
    print("Cloning project:" + name)
    
    list_url = "https://anonymous.4open.science/api/repo/"+ name +"/files/"
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15"
    }
    resp = requests.get(url=list_url, headers=headers)
    file_list = resp.json()

    sizes = [s[1] for s in get_dict_vals(file_list, ['size'])]
    print("Downloading {} files, tot: {}:".format(len(sizes), convert_size(sum((sizes)))))
    print("=====================================")

    dl_url = "https://anonymous.4open.science/api/repo/"+ name +"/file/"
    files = []
    out = []
    for file in dict_parse(file_list):
        file_path = os.path.join(*file[-len(file):-2]) # * operator to unpack the arguments out of a list
        save_path = os.path.join(save_dir, file_path)
        file_url = dl_url + file_path
        files.append((file_url, save_path))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_conns) as executor:
        future_to_url = (executor.submit(req_url, dl_file) for dl_file in files)
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                out.append(data)
                print(data)
                # print(str(len(out)),end="\r")
    print("=====================================")
    print("Files saved to: " + save_dir)
    print("=====================================")