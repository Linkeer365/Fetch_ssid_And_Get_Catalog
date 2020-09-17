import os
import requests
from lxml import etree
import time
import sys

import faulthandler

from openSQwindow import save_catalog_from_ss



target_dir=r"D:\AllDowns\newbooks"

catalog_dir=r"D:\AllDowns\newbooks\catalogs"

error_dir=r"D:\AllDowns\newbooks\catalogs\errors"

ct_dir=r"D:\刺头书\ucdrs无书签"

if not os.path.exists(catalog_dir):
    os.makedirs(catalog_dir)


template_url="http://book.ucdrs.superlib.net/search?Field=all&channel=search&sw="

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"}



# def get_namesIsbns_dict():
#     names_isbns={each:each.split("isbnisbn")[1].strip(".pdf") for each in os.listdir(target_dir) if each.endswith(".pdf")}
#     # for name,isbn in names_isbns.items():
#     #     print(f"name:{name};\t\tisbn:{isbn}")
#     return names_isbns

def get_ssid(some_isbn):
    url=f"{template_url}{some_isbn}"
    page_text=requests.get(url,headers=headers).text
    time.sleep(1)
    html=etree.HTML(page_text)
    patt="//input[@type='hidden' and starts-with(@id,'ssid')]//@value"
    ssids=html.xpath(patt)
    print("ssids:\t",ssids)
    if any(ssids):
        print("Fetched!")
        ssids=[each for each in ssids if bool(each)!=0]
        ssids_s = ",".join(ssids)
    else:
        print("Not fetched!")
        ssids_s="NIL"
    return ssids_s

def write_name_ssid(some_name,some_ssid,delim):
    assert not os.sep in some_name
    with open(f"{target_dir}{os.sep}all_ssids.txt","a",encoding="utf-8") as f:
        f.write(f"{some_ssid}{delim}{some_name}\n")
    print("one done.")

def write_catalog(some_name,some_ssid,some_text):
    pass

def main():
    books=[each for each in os.listdir(target_dir) if each.endswith(".pdf")]
    books=sorted(books,key=lambda x: os.path.getmtime(os.path.join(target_dir, x)),reverse=False)
    delim="\t\t\t"
    flag=0
    if os.path.exists(f"{target_dir}{os.sep}all_ssids.txt"):
        with open(f"{target_dir}{os.sep}all_ssids.txt","r",encoding="utf-8") as f:
            already_len=len(f.readlines())
            if already_len>=len(books):
                flag=1
    for each in books:
        if not flag:
            name,isbn=each,each.split("isbnisbn")[1].strip(".pdf")
            ssid=get_ssid(isbn)
            if ssid=="NIL":
                os.rename(f"{target_dir}{os.sep}{each}",f"{ct_dir}{os.sep}{each}")
            else:
                write_name_ssid(name,ssid,delim)
        else:
            print("already done.")
            break
    print("Phase 1: done.")
    # sys.exit(0)

    lines=[]
    with open(f"{target_dir}{os.sep}all_ssids.txt","r",encoding="utf-8") as f:
        lines=f.readlines()
        lines=[each.strip("\n") for each in lines]
    catalogs = []
    checkers=set([each[0:16] for each in os.listdir(catalog_dir) if each.endswith(".txt") and "ssidssid" in each])
    for line in lines:
        ssid_s,name=line.split(delim)
        print("ssids:\t",ssid_s)
        if len(ssid_s)>=8:
            ssids=ssid_s.split(",")
            for each_ssid in ssids:
                phobe_str=f"{each_ssid}ssidssid"
                if phobe_str in checkers:
                    continue
                faulthandler.enable()
                save_catalog_from_ss(each_ssid,target_dir2=catalog_dir,filename=name.strip(".pdf"),error_dir=error_dir)
    print("Phase 2: done.")

    print("all done.")






if __name__ == '__main__':
    main()