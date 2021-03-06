import win32con
import win32gui
import win32api
import time
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

import sys

qingtian_name="书签获取小工具2015.05.05  【晴天软件】"
target_dir=r"D:\All_SS_bookmarks"
qingtian_path=r"C:\Program Files\Shuqian\晴天软件_书签获取软件V0505.exe"

def get_hd_from_child_hds(father_hd,some_idx,expect_name):
    child_hds=[]
    win32gui.EnumChildWindows(father_hd,lambda hwnd, param: param.append(hwnd),child_hds)

    names=[win32gui.GetWindowText(each) for each in child_hds]
    hds=[hex(each) for each in child_hds]
    print("ChildName List:",names)
    print("Child Hds List:",hds)

    name=names[some_idx]
    hd=hds[some_idx]

    print("The {} Child.".format(some_idx))
    print("The Name:{}".format(name))
    print("The HD:{}".format(hd))

    if name==expect_name:
        return child_hds[some_idx]
    else:
        print("窗口不对！")
        return None

def save_catalog_from_ss(ss):
    # os.startfile(qingtian_path)
    startAt=time.time()
    SW_MINIMIZE = 6
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_MINIMIZE
    subprocess.Popen(qingtian_path, startupinfo=info)
    
    # 这里启动也需要停一阵子（至少2秒）

    time.sleep(2)
    ori_ss=ss
    qingtian_hd=None
    while not qingtian_hd:
        qingtian_hd=win32gui.FindWindowEx(None,0,0,qingtian_name)
    feedSS_hd=get_hd_from_child_hds(qingtian_hd,6,'')
    win32gui.SendMessage(feedSS_hd,win32con.WM_SETTEXT,0,ss)
    print("gg")

    # 这里有爬虫，需要停一阵子（至少1秒）...

    time.sleep(1)
    # huoquzhong_hd=get_hd_from_child_hds(qingtian_hd,5,"获取")
    # cnt=0
    # while cnt!=5:
    bookmark_hd=get_hd_from_child_hds(qingtian_hd,1,'')
    # time.sleep(0.5)
        # cnt+=1
        # time.sleep(0.5)
    # https: // blog.csdn.net / qq_41928442 / article / details / 88937337

    # https://stackoverflow.com/questions/53182704/python-memorybuffer-pywin32
    # 听人劝吃饱饭...

    # length = win32gui.SendMessage(bookmark_hd, win32con.WM_GETTEXTLENGTH)*2+2

    # 我终于知道我错在哪里了
    # https://blog.csdn.net/sinat_33384251/article/details/89444945
    
    # 这里有3个length！！！赋值的时候一定不要弄错！！！

    length = win32gui.SendMessage(bookmark_hd, win32con.WM_GETTEXTLENGTH)
    length2=length*2+2
    time.sleep(0.5)
    buf = win32gui.PyMakeBuffer(length2)
    #发送获取文本请求
    win32api.SendMessage(bookmark_hd, win32con.WM_GETTEXT, length2, buf)
    time.sleep(1)
    #下面应该是将内存读取文本
    address, length3 = win32gui.PyGetBufferAddressAndLen(buf[:-1])
    # time.sleep(0.5)
    text = win32gui.PyGetString(address, length3)[:length]

    print(text)

    time.sleep(0.5)
    error_line="没有查询到此SS的书签！"
    if error_line in text:
        ss="error_"+ss
    try:
        with open(target_dir+os.sep+ss+".txt","w",encoding="utf-8") as f:
            f.write(text)
        with open(target_dir+os.sep+"already_save.txt","a",encoding="utf-8") as f:
            f.write(ori_ss+"\n")
    except Exception:
        print(f"{ss} 无法写入！")
        pass
    win32gui.PostMessage(qingtian_hd,win32con.WM_CLOSE,0,0)
    time.sleep(0.5)
    endAt=time.time()
    run_time=endAt-startAt
    print(f"{ss} Run time:{run_time}")


# def main():
#     if os.path.exists(target_dir+os.sep+"already_save.txt"):
#         with open(target_dir+os.sep+"already_save.txt","r",encoding="utf-8") as f:
#             start_val=int(f.readlines()[-1].replace("\n",""))
#     else:
#         start_val=10**7
#     # some_ss=[10400487,12527673,12205452,12790775,12866829]
#     # some_ss2=[some_ss[0]]
#     pool=multiprocessing.Pool(processes=128)
#     for each in range(start_val,10**8):
#         if isinstance(each,int):
#             ss=str(each)
#         pool.apply_async(save_catalog_from_ss,args=(ss,))
#         # save_catalog_from_ss(ss)
#         print("one done")
#         # os.system("taskkill /F {}".format(qingtian_path))
#         time.sleep(1)
#     # thread_pool.shutdown(wait=True)
#     pool.close()
#     pool.join()
#     print("all done.")

save_catalog_from_ss("10400487")
sys.exit(0)

if __name__ == '__main__':
    if os.path.exists(target_dir+os.sep+"already_save.txt"):
        with open(target_dir+os.sep+"already_save.txt","r",encoding="utf-8") as f:
            start_val=int(f.readlines()[-1].replace("\n",""))
    else:
        start_val=10**7
    # some_ss=[10400487,12527673,12205452,12790775,12866829]
    # some_ss2=[some_ss[0]]
    # thread_pool=ThreadPoolExecutor(max_workers=4)
    for each in range(start_val,10**8):
        if isinstance(each,int):
            ss=str(each)
        # pool.apply_async(save_catalog_from_ss,args=(ss,))
        # future=thread_pool.submit(save_catalog_from_ss,ss)
        save_catalog_from_ss(ss)
        print("one done")
        # os.system("taskkill /F {}".format(qingtian_path))
        time.sleep(1)
    # thread_pool.shutdown(wait=False)
    # pool.close()
    # pool.join()
    print("all done.")