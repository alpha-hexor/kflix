import random
from termcolor import colored
import os
from tqdm import tqdm
from codebase.search import *
from codebase.get_link import *


#create download directory
if not os.path.exists('downloads'):
    os.mkdir('downloads')
    
mpv_executable = "mpv.exe" if os.name == "nt" else "mpv"

#clear screen
def clear():
    os.system("cls" if os.name=="nt" else "clear")

#function for color print
def colored_print(message):
    colors = ['red','green','blue','yellow','magenta','cyan']
    color = random.choice(colors)
    print(colored(message,color,attrs=["bold"]))

#function to get final links
def get_final_link(url):
    links,qualities = generate_links(url)
    for i in range(len(qualities)):
        colored_print("["+str(i+1)+"] "+qualities[i])
    opt = int(input("[*]Enter index: "))
    return links[opt-1]


#function to stream episode
def stream_episode(name,ep_num,last_ep):
    clear()
    
    colored_print("[*]Streaming Episode: "+name[8:]+": episode-"+ep_num)
    embade_url = get_embade_link(name,ep_num)
    link = get_final_link(embade_url)

    command = ' --referrer="https://asianembed.io" "'+link+'"'
    os.system(mpv_executable+command)
    
    if (int(ep_num) + 1 <= int(last_ep)):
        opt = input(("[*]Want to start next episode[y/n]: "))
        
        if opt == "n":
            exit()
        ep_num = int(ep_num)+1
        stream_episode(name,str(ep_num),last_ep)
        
    else:
        exit()
        
#download function
def download_episode(path,name,ep_num,last_ep):
    clear()
    colored_print("[*]Downloading Episode: "+name[8:]+": episode-"+ep_num)
    embade_url = get_embade_link(name,ep_num)
    link = get_final_link(embade_url)

    #download process
    r=requests.get(link,headers={'referer':"https://asianembed.io"},stream=True)
    total_size_in_bytes= int(r.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(path+"\\"+name[8:]+"_"+ep_num+".mp4", 'wb') as f:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    f.close()
    progress_bar.close()

    #for next episode
    if (int(ep_num) + 1 <= int(last_ep)):
        opt = input(("[*]Want to download next episode[y/n]: "))
        

        if (opt == "n"):
            exit()
                
        ep_num = int(ep_num)+1
        download_episode(path,name,str(ep_num),last_ep)
    else:
        exit()




def main():
    drama = input("[*]Enter drama name: ")
    drama_links,drama_names = search_drama(drama)

    for i in range(len(drama_names)):
        colored_print("["+str(i+1)+"] "+drama_names[i])
    
    s=int(input("[*]Enter index: "))
    drama_to_watch = drama_links[s-1]
    #print(drama_to_watch)
    first_ep = 1
    last_ep = int(drama_to_watch.split("-")[-1])
    
    colored_print("[*]Availabel Episodes[" + str(first_ep) +"-" + str(last_ep)+"]")
    ep_num = input("[*]Enter episode number: ")
    name = drama_to_watch.split("-episode-")[0]
    #print(name)
    if int(ep_num) >= 0 and int(ep_num) <= last_ep:
        clear()
        colored_print('[S]tream Episode')
        colored_print('[D]ownload Episode')
        x = input("[*]Enter your choice: ")
        
        if x == 'd' or x == 'D':
            path = "downloads\\" + name[8:]
            if not os.path.exists(path):
                os.makedirs(path)
            download_episode(path,name,ep_num,last_ep)
                
        else:
            stream_episode(name,ep_num,last_ep)
            
            





if __name__ == "__main__":
    main()