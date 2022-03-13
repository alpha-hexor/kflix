import requests
from bs4 import BeautifulSoup


#some global things
headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
main_url = "https://asianembed.io"
links = []
drama_names=[]



def search_drama(name):
    '''
    function to search drama
    '''
    if len(name) > 1:
        name = name.replace(" ","-")
    
    search_url = main_url+"/search.html?keyword="+name
    r=requests.get(search_url,headers=headers)
    src = r.content
    soup=BeautifulSoup(src,'lxml')
    ul_block=soup.find("ul",attrs={'class':'listing items'})
    
    #extract all the hrefs
    for a in ul_block.find_all('a', href=True):
        links.append(str(a['href']))
    
    
    #extract all the names
    x=ul_block.find_all("div",attrs={"class":'name'})
    for name in x:
        drama_names.append(str(name.text).replace("\n","").strip(" "))
        
    return links,drama_names