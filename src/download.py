import requests
import os
from time import sleep
import concurrent.futures
from functools import partial
import threading



class RequestLimitReached(Exception):
    """Exception raised when the request limit is reached."""
    pass

def dict_parse(dic, pre=None):
    pre = pre[:] if pre else []
    if isinstance(dic, dict):
        for key, value in dic.items():
            if isinstance(value, dict):
                for d in dict_parse(value, pre + [key]):
                    yield d
            else:
                yield pre + [key, value]
    else:
        yield pre + [dic]


def get_dict_vals(test_dict, key_list):
   for i, j in test_dict.items():
     if i in key_list:
        yield (i, j)
     yield from [] if not isinstance(j, dict) else get_dict_vals(j, key_list)


def format_file_size(size, decimals=2, binary_system=False):
    if binary_system:
        units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']
        largest_unit = 'YiB'
        step = 1024
    else:
        units = ['B', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']
        largest_unit = 'YB'
        step = 1000
    for unit in units:
        if size < step:
            return ('%.' + str(decimals) + 'f %s') % (size, unit)
        size /= step
    return ('%.' + str(decimals) + 'f %s') % (size, largest_unit)


def check_file_authentic(save_path):
    """Check text file existed and authentic"""
    if not os.path.exists(save_path):
        return False

    # Jump up for these file types because we cannot determine these file types are downloaded correctly or not
    jump_list = ['.png', '.jpg', '.gif', '.mp4']
    if True in [save_path.endswith(x) for x in jump_list]:
        return True

    # Test file is downloaded okay
    try:
        with open(save_path, "rt") as f:
            if f.readline() != "You can only make 350 requests every 15min. Please try again later.":
                return True
            return False
    except Exception:
        return False


def req_url(dl_file, max_retry=5, headers=None, proxies=None, wait_event=None):
    """Download file"""
    url = dl_file[0]
    save_path = dl_file[1]

    if check_file_authentic(save_path):
        return f"File {save_path} existed & authentic"

    # Check Windows or Unix (Mac+Linux); nt is Windows
    if os.name == 'nt': 
        divider = '\\'
    else:
        divider = '/'
    save_dir = divider.join(save_path.split(divider)[:-1])
    if not os.path.exists(save_dir) and save_dir:
        try:
            os.makedirs(save_dir)
        except OSError:
            pass
    
    headers = headers if headers else {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15"
    }
    proxies = proxies if proxies else { "http": "", "https":"", }

    attempt = 0
    while attempt < max_retry:
        if wait_event.is_set():
            print(f"Waiting due to rate limit, attempt {attempt}")
            wait_event.wait()  # Wait until the event is cleared
        try:
            r = requests.get(url, headers=headers, proxies=proxies)
            if r.text.startswith("You can only make 350 requests every 15min"):
                wait_event.set() 
                print(f"Request limit reached, waiting for 15 minutes. Attempt {attempt}")
                sleep(15 * 60)  
                wait_event.clear()  # Clear the event to resume all threads
                attempt += 1
                continue
            with open(save_path, "wb") as f:
                f.write(r.content)
            return 'Downloaded: ' + str(save_path)
        except Exception as e:
            exception = e
            sleep(0.4)
        attempt += 1
    return 'File request exception (retry {}): {} - {}'.format(attempt, exception, save_path)




def download_repo(config):
    """Download Anonymous Github repo"""

    url = config['url']
    save_dir = config['save_dir']
    max_conns = config['max_conns']
    max_retry = config['max_retry']
    proxies = {"http": config['proxies'], "https": config['proxies']}
    verbose = config['verbose']

    name = url.split('/')[4]
    save_dir = os.path.join(save_dir, name)
    
    print("=====================================")
    print("Cloning project:" + name)
    
    list_url = "https://anonymous.4open.science/api/repo/"+ name +"/files/"
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15"
    }
    resp = requests.get(url=list_url, headers=headers, proxies=proxies)
    file_list = resp.json()

    sizes = [s[1] for s in get_dict_vals(file_list, ['size'])]
    print("Downloading {} files, tot: {}:".format(len(sizes), format_file_size(sum((sizes)))))
    print("=====================================")

    dl_url = "https://anonymous.4open.science/api/repo/"+ name +"/file/"
    files = []
    out = []
    for file in dict_parse(file_list):
        file_path = os.path.join(*file[-len(file):-2]) # * operator to unpack the arguments out of a list
        save_path = os.path.join(save_dir, file_path)
        file_url = os.path.join(dl_url, file_path).replace("\\","/") # replace \ with / for Windows compatibility
        files.append((file_url, save_path))

    partial_req = partial(req_url, max_retry=max_retry, headers=headers, proxies=proxies)
    wait_event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_conns) as executor:
        partial_req = partial(req_url, max_retry=max_retry, headers=headers, proxies=proxies, wait_event=wait_event)
        future_to_url = {executor.submit(partial_req, dl_file): dl_file for dl_file in files}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                data = future.result()
            except Exception as exc:
                data = str(type(exc))
            finally:
                out.append(data)
                if verbose or "existed & authentic" not in data:
                    print(data)
    print("=====================================")
    print("Files saved to: " + save_dir)
    print("=====================================")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Download Anonymous Github repo')
    parser.add_argument('--url', type=str, help='Anonymous Github repo url')
    parser.add_argument('--save_dir', type=str, default='.', help='Save directory')
    parser.add_argument('--max_conns', type=int, default=10, help='Max connections')
    parser.add_argument('--max_retry', type=int, default=5, help='Max retries')
    parser.add_argument('--proxies', type=str, default='', help='Proxies used for connection')
    parser.add_argument('--verbose', type=bool, default=False, help='Display skipped files or not')
    args = parser.parse_args()
    download_repo(args.__dict__)
