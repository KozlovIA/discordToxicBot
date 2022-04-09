import re, requests, urllib.parse, urllib.request
from bs4 import BeautifulSoup
    
    
def search_URL(music_name):
    """
    Функция ищет по имени песню на ютубе
    Входной параметр - имя
    Выходные clip2 - URL, concatMusic1['content'] - название на ютубе
    """

    query_string = urllib.parse.urlencode({"search_query": music_name})

    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())

    clip = requests.get("https://www.youtube.com/watch?v=" + "{}".format(search_results[0]))
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])


    inspect = BeautifulSoup(clip.content, "html.parser")
    yt_title = inspect.find_all("meta", property="og:title")

    for concatMusic1 in yt_title:
        pass

    return clip2, concatMusic1['content']
