# Clone Anonymous Github

Easily clone/download Anonymous Github repositories from [anonymous.4open.science](anonymous.4open.science) with a GUI interface.

_No need for GUI interface? We support command line as well!_

> [!IMPORTANT] 
> Please take notice of [this Github issue](https://github.com/tdurieux/anonymous_github/issues/24), as it seems that the reason cloning is not implemented is because of server managing costs. Please do not abuse the service and if possible, support [Anonymous Github](https://github.com/tdurieux/anonymous_github)!

## Download
[![Latest release](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/fedebotu/clone-anonymous-github/releases/download/0.2.1/Clone-Anonymous-Github-WINDOWS.exe) [![Latest release](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white)](https://github.com/fedebotu/clone-anonymous-github/releases/download/0.2.1/Clone-Anonymous-Github-MAC.tar)

## Usage (GUI)
###  Windows and Mac
For Windows and Mac users: from the [Release Page](https://github.com/fedebotu/clone-anonymous-github/releases/), download and run files that fit your operating system.
**Notice about antivirus**: the executables may be detected as fake positives, so you need to temporarily disable your anti virus program 

### Linux
First clone the repository and install the requirements (optionally, create a virtual environment)
```shell
pip install -r requirements.txt
```
then, run

```shell
python run.py
```

## Usage (command line)
```shell
git clone https://github.com/fedebotu/clone-anonymous-github.git && cd clone-anonymous-github
python3 src/download.py --url [YOUR_ANONYMOUS_GITHUB_URL]
```

## Known "Bugs"

- The maximum number of downloads is exceeded: (also in [this PR](https://github.com/fedebotu/clone-anonymous-github/pull/5)), there are limitations on the number of downloads every 15 minutes from the same IP address. If this happens, either wait or change your IP (i.e., with a VPN). If you decide to wait: wait for 15 minutes and then start the download again to the same directory. Already downloaded files will be skipped, and 'bad' files will be downloaded.


## Contribute
Feel free to raise issues and submit pull requests! :D

## Acknowledgements
Thanks to the original [tdurieux's Anonymous Github project](https://github.com/tdurieux/anonymous_github), [ShoufaChen's Clone Anonymous Github](https://github.com/ShoufaChen/clone-anonymous4open), [kynehc's Clone Anonymous Github](https://github.com/kynehc/clone_anonymous_github) and [cbhua](https://github.com/cbhua) for testing in MacOS!
