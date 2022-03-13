import requests
import struct
import xml.etree.ElementTree as ET
from tqdm import tqdm
import os
#function to check windows version using struct
def check_windows_version():
    windows_version = struct.calcsize("P") * 8
    if windows_version == 64:
        return "64"
    elif windows_version == 32:
        return "32"
    else:
        return "Unknown"


#function to get xml
def get_xml(url):
    r = requests.get(url)
    with open('data.xml',"wb") as f:
        f.write(r.content)
    f.close()
#function to load xml
def load_xml():
    tree = ET.parse('data.xml')
    root = tree.getroot()
    f = root.findall('./channel/item/link')[0].text
    filename = f.split("/")[-2]
    #os.remove("data.xml")
    return filename
#download mpv executable file using requests
def download_mpv(url,f):
    r = requests.get(url,stream=True)
    total_size_in_bytes= int(r.headers.get('content-length', 0))
    block_size = 1024 #1 kilobyte data
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(f, 'wb') as ft:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            ft.write(data)
    ft.close()
    progress_bar.close()

#function to download 7z    
def download_7z():
    url = "https://www.7-zip.org/a/7z1804.exe"
    r = requests.get(url,stream=True)
    total_size_in_bytes= int(r.headers.get('content-length', 0))
    block_size = 1024 #1 kilobyte data
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open("7z.exe", 'wb') as ft:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            ft.write(data)
    ft.close()
    progress_bar.close()
    os.system("7z.exe")
#function to extract 7z
def extract_7z(f,p):
    os.chdir(os.environ["ProgramFiles(x86)"]+"\\7-Zip")
    os.system("7z.exe x "+p+"\\"+f+" -o" + p+"\\mpv")
    try:
        os.remove("7z.exe")
    except:
        pass
    #os.remove("7z.exe")
    os.remove(p+"\\"+f)


def main():
    if check_windows_version() == "64":
        link = "https://sourceforge.net/projects/mpv-player-windows/rss?path=/64bit"
        url = "https://sourceforge.net/projects/mpv-player-windows/files/64bit/"
    elif check_windows_version() == "32":
        link = "https://sourceforge.net/projects/mpv-player-windows/rss?path=/32bit"
        url = "https://sourceforge.net/projects/mpv-player-windows/files/32bit/"
    else:
        print("[*]unknown windows version")
        exit()
    get_xml(link)
    f = load_xml()
    print("[*]Latest mpv version: " + f)
    print("[*]Downloading mpv")
    url = url +f+"/download"
    #print(url)
    download_mpv(url,f)
    os.system("del data.xml")
    print("[*]Downloading 7z")
    download_7z()
    print("[*]Extracting")
    p = os.getcwd()
    extract_7z(f,p)
    mpv_path = p+"\\mpv\\mpv.exe"
    os.system("move "+mpv_path+" "+p)
    os.system("rmdir /s /q " +p+"\\mpv")
    print("[*]mpv installed successfully")

main()