import requests
import os
from time import sleep
import concurrent.futures


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


def req_url(dl_file, max_retry=5):
    """Download file"""
    url = dl_file[0]
    save_path = dl_file[1]

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
            exception = e
            # print('file request exception (retry {}): {} - {}'.format(i, e, save_path))
            sleep(0.4)
    return 'File request exception (retry {}): {} - {}'.format(i, exception, save_path)


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


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Download Anonymous Github repo')
    parser.add_argument('--url', type=str, help='Anonymous Github repo url')
    parser.add_argument('--save_dir', type=str, default='.', help='Save directory')
    parser.add_argument('--max_conns', type=int, default=10, help='Max connections')
    parser.add_argument('--max_retry', type=int, default=5, help='Max retries')
    args = parser.parse_args()
    download_repo(args.__dict__)