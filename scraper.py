import requests
from bs4 import BeautifulSoup
from user_agent import user_agent


headers = {'User-Agent': user_agent,
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}


def launch_request(url):
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return resp


def get_main_news():    
    url = 'https://www.infomed.hlg.sld.cu/'    
    resp = launch_request(url)    
    content = BeautifulSoup(resp.text, 'lxml')
    noticias = content.find_all('header', attrs={'class':'dmbs-post-header'})
        
    titulares = []
        
    for articulo in noticias:
        titulares.append({
            "titular": articulo.find('h2', attrs={'class':'dmbs-post-title'}).get_text(),
            "url": articulo.find('h2').a.get('href')
        })
    return titulares


def get_info_by_news(noticia):    
    print(f'Scrapping {noticia["titular"]}')
    
    resp = launch_request(noticia["url"])    
    content = BeautifulSoup(resp.text, 'lxml')    
    article = content.find('article', attrs={'class':'dmbs-post-single'})
    
    noticia['fecha'] = article.find('span', attrs={'class':'dmbs-post-date'}).get_text()    
    noticia['articulo'] = article.find('div', attrs={'class':'card-body dmbs-post-content'}).get_text()
    
    return noticia


if __name__ == '__main__':
    noticias = get_main_news()
    
    for noticia in noticias:
         news = get_info_by_news(noticia)
         print('=================================')
         print(news)
         print('=================================')