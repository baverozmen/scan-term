import os
import subprocess as sb
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
while True:
    input("eger root degilsniz Ctrl + C'ye basıp root olun eger rootsanız [ENTER]a basınız")
    os.system("clear")

    print("1 - açıkları aramak istiyorum")
    print("2 - zararlı yazılım var mı")
    sayıDegeri = int(input("lütfen girmek isteediginiz sayıyı seçiniz: "))

    url=str(input("lütfen siteyi giriniz: "))
    #kullanılan araçlar nmap dirb beef  sqlmap netcat enum4linux veya smbclient hydra
    araçlar = ["nmap", "dirb", "sqlmap", "enum4linux", "hydra"]#"netcat", "smbclient"
    if sayıDegeri == 1:
        
        while True:
            os.system("clear")
            print(" !![BİLGİLENDİRME]!! ")
            print("öncelikle egitim amaçlı bir yazılımdır kullanılan araçlar ayrı ayrı kullanılmasın diye daha rahat şekilde tarama yapılsın diye yazılmıştır")
            print("kullanılan araçlar sırasıyla:nmap, dirb, beef, sqlmap, netcat")
            toolDownload=str(input("araç taraması yapılacak ve yükllü olmayan araçlar yüklenicek kabul ediyor musunuz(y/n): "))
            if toolDownload== "y" or "Y":
            
                for araç in araçlar:
                    try:
                        tarama=sb.check_output(f"which {araç}", shell=True)
                        print(f"{araç} yüklü")
                        time.sleep(0.5)
                        
                        
                    except sb.CalledProcessError:

                        print(f"{araç} yükleniyor...")
                        time.sleep(1)
                        try:
                            os.system(f"apt install {araç}")
                            
                        except Exception as e:
                            print("bilinmeyen bir hata oldu{}".format(e))

                
                try:

                    cıktı=sb.check_output(f"ping -c 1 {url}", shell=True, universal_newlines=True)
                    ip_adress=re.search(r'(\d+\.\d+\.\d+\.\d+)',cıktı).group(1)
                    print(ip_adress)
                    print("detaysız olarak adlandırılan seviye bile çok detaylıdır ve uzun sürer")
                    numara=int(input("tarama detayı için numara giriniz(0-5) 0 en detaylı ve güvenliklidir çok yavaştır 3 normal hızdır 5 hızlı daha güvenliksizdir: "))
                    nmap = os.system(f"nmap -A -sS -v -sV -pN -p -T{numara}  {ip_adress}")
                    print("nmap taramanız bitmiştir sonuçlar yukarıdadır ")
                    time.sleep(2)
                    str(input("devam etmek için [ENTER] basınız "))
                    time.sleep(3)
                except sb.CalledProcessError:

                    print("baglantıdan kaynaklanan bir hata oldu")

                dirb=os.system(f"dirb https://{url}")
                str(input("devam etmek için [ENTER] basınız"))
                #beef=os.system("beef ")
                str(input("devam etmek için [ENTER] basınız"))
                sqlmap=os.system(f"sqlmap -u https://{url} --level=5 --risk=3")
                str(input("devam etmek için [ENTER] basınız"))
                #netcat=os.system("netcat")
                enum4liux=os.system(f"enum4linux {ip_adress}")
                str(input("devam etmek için [ENTER] basınız"))
                kullanıcıadı=str(input("kullanıcı adı buunduysa kullanıcı adını yazınız bulunmadıysa [ENTER]a basınız"))
                passlist=str(input("sifre için liste giriniz"))
                if not kullanıcıadı == "":
                    hydra=os.system(f"hydra -l {kullanıcıadı} -p {passlist} 6667://{ip_adress}")
                str(input("devam etmek için [ENTER] basınız"))


            elif toolDownload == "n" or "N":
                print("üzgünüz araçlar yüklü olmadığı için işlem yapamıyoruz")
                break
            else:
                print("tekrar deneyiniz")
        break
    elif sayıDegeri == 2:
        
        resp=requests.get(f"https://{url}")
        html_soup=BeautifulSoup(resp.content,"html.parser")
        scripts=html_soup.find_all("script")
        for script in scripts:
            src_one=script.get("src")
            if script.string:
                if "beef" or "hook.js" in script.string:
                    print("beef enjeksiyonu yaplmış lütfen siteyi kapatınız muhtemel bir xss açığı veya site tarafından yapılan saldırı var")
                    print(script.string)
            elif src_one:
                

                print(f"{src_one}  <--- bu urllere yönlendiriyor beef enjeksiyonu hakkında açık kaynakta bi şey bulunamadı")
                time.sleep(0.75)
                beefsrc=str(input("srcler içerisinde aramak ister misiniz(y/n): "))
                hooksrc=str(input( "hook.js dosyasını alıp tarama yapılsn mı(tavsiye edilen yapılmasıdır)(y/n)" ))
                if beefsrc== "y" or "Y":
                    full_url =urljoin(f"https://{url},", src_one)
                    js_resp=requests.get(full_url)
                    if "beef" or "hook.js" in js_resp.text:
                        print("beef açıgı var")
                    
                    else:
                        break
                elif hooksrc== "y" or "Y":
                    current_directory = os.path.dirname(os.path.abspath(__file__))
                    js_file_path = os.path.join(current_directory, 'hook.js')

            
                    try:
                        with open(js_file_path, 'r', encoding='utf-8') as file:
                            js_code = file.read()
                            if js_code in script.string:
                                print("beef enjeksiyonu var")
                            else:
                                print("beef ejeksiyonu yok")
                                break
                            
                    except Exception as e:
                        print("bilinmeyen bir hata oldu hata: ---> {}".format(e))
    else:       
        print("lütfen degeri dogru giriniz")
