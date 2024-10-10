import os
import subprocess as sb
import re
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def check_and_install_tools(araçlar):
    for araç in araçlar:
        try:
            tarama = sb.check_output(f"which {araç}", shell=True)
            print(f"{araç} yüklü")
            time.sleep(0.5)
        except sb.CalledProcessError:
            print(f"{araç} yükleniyor...")
            time.sleep(1)
            try:
                os.system(f"apt install {araç}")
            except Exception as e:
                print(f"Bilinmeyen bir hata oldu: {e}")

def get_ip_from_url(url):
    try:
        cıktı = sb.check_output(f"ping -c 1 {url}", shell=True, universal_newlines=True)
        ip_adress = re.search(r'(\d+\.\d+\.\d+\.\d+)', cıktı).group(1)
        return ip_adress
    except sb.CalledProcessError:
        print("Bağlantıdan kaynaklanan bir hata oldu")
        return None

def perform_nmap_scan(ip_adress, numara):
    try:
        print(f"Nmap taraması başlıyor... IP: {ip_adress}, Detay seviyesi: {numara}")
        os.system(f"nmap -A -sS -v -sV -pN -T{numara} {ip_adress}")
        print("Nmap taramanız bitmiştir.")
        input("Devam etmek için [ENTER] basınız ")
    except Exception as e:
        print(f"Hata: {e}")

def perform_dirb_scan(url):
    try:
        os.system(f"dirb https://{url}")
        input("Devam etmek için [ENTER] basınız")
    except Exception as e:
        print(f"Dirb hatası: {e}")

def perform_sqlmap_scan(url):
    try:
        os.system(f"sqlmap -u https://{url} --level=5 --risk=3")
        input("Devam etmek için [ENTER] basınız")
    except Exception as e:
        print(f"SQLMap hatası: {e}")

def perform_enum4linux_scan(ip_adress):
    try:
        os.system(f"enum4linux {ip_adress}")
        input("Devam etmek için [ENTER] basınız")
    except Exception as e:
        print(f"Enum4Linux hatası: {e}")

def perform_hydra_attack(ip_adress, kullanıcıadı, passlist):
    try:
        if kullanıcıadı:
            os.system(f"hydra -l {kullanıcıadı} -P {passlist} 6667://{ip_adress}")
            input("Devam etmek için [ENTER] basınız")
    except Exception as e:
        print(f"Hydra hatası: {e}")

def check_beef_injection(url):
    try:
        resp = requests.get(f"https://{url}")
        html_soup = BeautifulSoup(resp.content, "html.parser")
        scripts = html_soup.find_all("script")
        for script in scripts:
            src_one = script.get("src")
            if script.string and ("beef" in script.string or "hook.js" in script.string):
                print("Beef enjeksiyonu yapılmış olabilir! Siteyi kapatın!")
                print(script.string)
            elif src_one:
                print(f"{src_one}  <-- Bu URL'ye yönlendiriyor, incelemeye devam ediliyor.")
                time.sleep(0.75)
                
                beefsrc = input("Src dosyasında arama yapmak ister misiniz? (y/n): ")
                hooksrc = input("Hook.js dosyasını taramak ister misiniz? (tavsiye edilir) (y/n): ")
                
                if beefsrc.lower() == "y":
                    full_url = urljoin(f"https://{url}", src_one)
                    js_resp = requests.get(full_url)
                    if "beef" in js_resp.text or "hook.js" in js_resp.text:
                        print("Beef açığı tespit edildi!")
                    else:
                        print("Beef açığı bulunamadı.")
                
                if hooksrc.lower() == "y":
                    current_directory = os.path.dirname(os.path.abspath(__file__))
                    js_file_path = os.path.join(current_directory, 'hook.js')
                    with open(js_file_path, 'r', encoding='utf-8') as file:
                        js_code = file.read()
                        if js_code in script.string:
                            print("Beef enjeksiyonu var!")
                        else:
                            print("Beef enjeksiyonu yok.")
    except Exception as e:
        print(f"Beef kontrolü sırasında bir hata oluştu: {e}")

def main():
    while True:
        input("Eğer root değilseniz Ctrl + C'ye basıp root olun, eğer rootsanız [ENTER] tuşuna basınız.")
        os.system("clear")

        print("1 - Açıkları aramak istiyorum")
        print("2 - Zararlı yazılım var mı?")
        try:
            sayıDegeri = int(input("Lütfen girmek istediğiniz sayıyı seçiniz: "))
        except ValueError:
            print("Lütfen geçerli bir sayı giriniz.")
            continue

        url = input("Lütfen siteyi giriniz: ")
        araçlar = ["nmap", "dirb", "sqlmap", "enum4linux", "hydra"]

        if sayıDegeri == 1:
            toolDownload = input("Araç taraması yapılacak ve yüklü olmayan araçlar yüklenecek, kabul ediyor musunuz? (y/n): ")
            if toolDownload.lower() == "y":
                check_and_install_tools(araçlar)

                ip_adress = get_ip_from_url(url)
                if ip_adress:
                    try:
                        numara = int(input("Tarama detayı için numara giriniz (0-5): "))
                        if 0 <= numara <= 5:
                            perform_nmap_scan(ip_adress, numara)
                            perform_dirb_scan(url)
                            perform_sqlmap_scan(url)
                            perform_enum4linux_scan(ip_adress)

                            kullanıcıadı = input("Kullanıcı adı bulunduysa giriniz, bulunmadıysa [ENTER] tuşuna basınız: ")
                            if kullanıcıadı:
                                passlist = input("Şifre listesi giriniz: ")
                                perform_hydra_attack(ip_adress, kullanıcıadı, passlist)
                        else:
                            print("Lütfen 0 ile 5 arasında bir numara giriniz.")
                    except ValueError:
                        print("Geçersiz numara girdiniz.")
                else:
                    print("IP adresi alınamadı, tarama yapılamıyor.")
            else:
                print("Araçlar yüklenmediği için işlem yapılamıyor.")
        elif sayıDegeri == 2:
            check_beef_injection(url)
        else:
            print("Lütfen geçerli bir seçenek giriniz.")

if __name__ == "__main__":
    main()
