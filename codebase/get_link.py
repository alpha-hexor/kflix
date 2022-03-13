from email import header
import requests
import json
import yarl
import base64
from bs4 import BeautifulSoup
from Cryptodome.Cipher import AES


#some global things
headers = {"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
main_url = "https://asianembed.io"
s=b'93422192433952489752342908585752'
iv=b'9262859232435825'

def get_embade_link(name,ep_num):
    '''
    function to get embade url
    '''     
    link = main_url+name+'-episode-'+ep_num
    #print(link)
    r=requests.get(link,headers=headers)
    src = r.content
    soup = BeautifulSoup(src,'lxml')
    x=soup.find("iframe")
    url = "https:" + str(x['src'])
    
    return url


def decrypt(data):
    '''
    function to decrypt data
    '''
    return AES.new(s, AES.MODE_CBC, iv=iv).decrypt(base64.b64decode(data))


def pad(data):
    '''
    helper function
    '''
    length = 16-(len(data)%16)
    return data+chr(length)*length


def generate_links(url):
    '''
    function to generate streaminhg urls and get qualities
    '''
    qualities = []
    links = []
    
    ajax_url = main_url+"/encrypt-ajax.php"
    p_url = yarl.URL(url)
    id = p_url.query.get('id')
    
    encypted_ajax = base64.b64encode(
        AES.new(s,AES.MODE_CBC,iv=iv).encrypt(
            pad(id).encode()
        )
    )
    
    #send the request to the ajax_url
    r=requests.get(
        ajax_url,
        params={
            'id':encypted_ajax.decode(),
        },
        headers={
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
            
            
        }
    )
    
    
    #decrypt and get the final data
    x=decrypt(r.json().get("data")).decode()
    
    j=json.loads(x.replace(x[-1],""))
    
    #get max 4 links
    for i in range(4):
        try:
            link = j['source'][i]['file']
            links.append(link)
            q = j['source'][i]['label']
            qualities.append(q)
        except:
            pass
    
    return links,qualities