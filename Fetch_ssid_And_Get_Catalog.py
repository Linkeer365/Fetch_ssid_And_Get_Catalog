import os
import requests
from lxml import etree
import time
import sys

import re

import faulthandler

# from openSQwindow2 import save_catalog_from_ss
from openSQwindow4 import save_catalog_from_ss



target_dir=r"D:\AllDowns\newbooks"

catalog_dir=r"D:\AllDowns\newbooks\catalogs"

error2_path=r"D:\AllDowns\newbooks\catalogs\error-notfetch.txt"

error_dir=r"D:\AllDowns\newbooks\catalogs\errors"
error_path=r"D:\AllDowns\newbooks\catalogs\errors\fetch-errors.txt"
if os.path.exists(error_path):
    open(error_path,"w").close()

if os.path.exists(error2_path):
    open(error2_path,"w").close()

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
    patt2="//span[@class='fc-green']//text()"
    ssids=html.xpath(patt)
    ssid_infos=html.xpath(patt2)

    print("ssid_infos_list:",ssid_infos)

    if any(ssids):
        print("Fetched!")

        ssid_infos2=[]
        # 这个数字可以设得很大...
        for each in range(1,100):
        # 注意这里是>=，逻辑细节！！
            if len(ssid_infos)>=8*each:
                ssid_info="".join(ssid_infos[8*(each-1):8*each])
                ssid_infos2.append(ssid_info)
            else:
                break
        ssid_infos=ssid_infos2

        ssids=[each for each in ssids if bool(each)!=0]

        # 这里可能会出现ssid_infos比ssids长的情况，于是

        ssid_infos=ssid_infos[0:len(ssids)]

        print("ssids:\t",ssids)
        print("ssid-infos:\t",ssid_infos)


        # 但这可能会有后续的bug，也就是类似于这样的 ['13243341', '', '','10421402', '13528633']
        # 这个东西''在前面这样的情况...

        if len(ssids)>1:
            for each_idx,each_info in enumerate(ssid_infos,1):
                if ssids[each_idx-1]:
                    print(each_info,"\t\t\t",each_idx)
            choice_idx=int(input("Your choice:"))-1
            ssids_s=ssids[choice_idx]
        elif len(ssids)==1:
            ssids_s = ssids[0]
        return ssids_s
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
            print(f"\nName:{name}\nISBN:{isbn}\n")
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

    for each in os.listdir(catalog_dir):
        if each.startswith("error"):
            with open(error2_path,"a",encoding="utf-8") as f:
                f.write(each+"\n")
    print("Phase 3: done.")

    print("all done.")


def waibao():
    one_one="9787108028938"
    multi="9787108016386"
    bad="978754424251"
    get_ssid(one_one)
    get_ssid(multi)
    get_ssid(bad)


if __name__ == '__main__':
    # main()
    waibao()