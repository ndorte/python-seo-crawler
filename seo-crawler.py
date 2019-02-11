from requests import get
from bs4 import BeautifulSoup

tarananlar = list()
taranacaklar = list()
dortYuzDort = list()
disLinkler = list()

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

url = ""
linkuzunlugu = (len(url))

def ilksayfa(url):
    cek = get(url, headers=header)
    soup = BeautifulSoup(cek.text, "html.parser")
    linkler = soup.findAll('a')
    for link in linkler:
        if link.has_attr("href"):
            if link["href"][:linkuzunlugu] == url:
                taranacaklar.append(link["href"])
            elif link["href"][:linkuzunlugu+1] != "/" and link["href"][:4] == "http":
                disLinkler.append(link["href"])
            elif link["href"][:linkuzunlugu+1] != "/":
                taranacaklar.append(url+"/"+link["href"])
            else:
                print("Ne oldugu tespit edilemedi. Lütfen manuel kontrol edin: "+link["href"])
        else:
            continue
    tarananlar.append(url)
    print("İlk Sayfa Taraması Bitti.")

ilksayfa(url)

for tara in taranacaklar:
    if tara not in tarananlar:
        print("Sayfa Taranıyor: " + tara)
        cek = get(tara, headers=header)
        soup = BeautifulSoup(cek.text, "html.parser")
        linkler = soup.findAll('a')
        for link in linkler:
            if link.has_attr("href"):
                if link["href"][:linkuzunlugu] == url:
                    if link["href"] in taranacaklar:
                        continue
                    else:
                        if link["href"][-4:] == ".jpg" or link["href"][-4:] == ".png" or link["href"][-4:] == ".pdf":
                            continue
                        else:
                            taranacaklar.append(link["href"])
                elif "//" in link["href"] or "///" in link["href"]:
                    continue
                elif link["href"] == "/":
                    continue
                elif link["href"]== "#" or link["href"][:8] == "#respond":
                    continue
                elif link["href"][:7] == "mailto:" or link["href"][:4] == "tel:":
                    continue
                elif link["href"][:linkuzunlugu + 1] != "/" and link["href"][:4] == "http":
                    if link["href"][:30] == "https://www.facebook.com/share" or link["href"][:30] == "https://web.whatsapp.com/send?" or link["href"][:30] == "http://www.facebook.com/sharer" or link["href"][:30] == "https://twitter.com/share?text" or link["href"][:30] == "https://twitter.com/intent/twe" or link["href"][:30] == "http://www.linkedin.com/shareA" or link["href"][:30] == "http://reddit.com/submit?url=h" or link["href"][:30] == "http://vk.com/share.php?url=ht" or link["href"][:30] == "http://www.tumblr.com/share/li" or link["href"][:30] == "http://linkedin.com/shareArtic" or link["href"][:30] == "http://pinterest.com/pin/creat" or link["href"][:30] == "https://plus.google.com/share?":
                        continue
                    else:
                        if link["href"] in disLinkler:
                            continue
                        else:
                            disLinkler.append(link["href"])
                            print("Dış link: " + link["href"] + " Bulunan Sayfa: "+ tara)
                            with open("dislink.txt", "a", encoding="utf-8") as file:
                                file.writelines(link["href"] + " Bulunan Sayfa: "+ tara +"\n")
                                file.close()
                elif link["href"][:linkuzunlugu + 1] != "/":
                    if url + "/" + link["href"] in taranacaklar:
                        continue
                    else:
                        taranacaklar.append(url + "/" + link["href"])
                else:
                    print("Ne oldugu tespit edilemedi. Lütfen manuel kontrol edin: " + link["href"])
                    continue
            else:
                continue
        tarananlar.append(tara)
    elif tara in tarananlar:
        continue

with open("taranansayfalar.txt", "a", encoding="utf-8") as fil:
    for i in tarananlar:
        fil.writelines(i + "\n")
    fil.close()
