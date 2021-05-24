import win32con
import win32gui
import win32api
import time
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import sys

import win32clipboard
import chardet  # 八进制转中文


def getText():
    # 读取剪切板
    # https://www.wandouip.com/t5i58809/
    win32clipboard.OpenClipboard()  # 打开剪切板

    # 使用CF_UNICODETEXT可以直接得到中文
    d = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)  # 得到剪切板上的数据

    win32clipboard.CloseClipboard()  # 关闭剪切板

    return d



qingtian_name="书签获取小工具2015.05.05  【晴天软件】"
target_dir=r"D:\All_SS_bookmarks"
qingtian_path=r"C:\Program Files\Shuqian\晴天软件_书签获取软件V0505.exe"

# while True:
#     tempt = win32api.GetCursorPos() # 记录鼠标所处位置的坐标
# #     x = tempt[0]-choose_rect[0] # 计算相对x坐标
# #     y = tempt[1]-choose_rect[1] # 计算相对y坐标
#     print(tempt)
#     time.sleep(0.5) # 每0.5s输出一次



def click_on_pos(pos_list):
    btn_pos = pos_list
    win32api.SetCursorPos(btn_pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

# https://python3-cookbook.readthedocs.io/zh_CN/latest/c05/p15_printing_bad_filenames.html
def bad_filename(filename):
    temp = filename.encode(sys.getfilesystemencoding(), errors='surrogatepass')
    return temp.decode('utf-8')


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

def save_catalog_from_ss(ss,target_dir2=target_dir,filename=None,error_dir=None):
    # startAt=time.time()

    # os.startfile(qingtian_path)

    startAt=time.time()
    SW_MINIMIZE = 6
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_MINIMIZE
    subprocess.Popen(qingtian_path, startupinfo=info)

    # SW_MINIMIZE = 6
    # info = subprocess.STARTUPINFO()
    # info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    # info.wShowWindow = SW_MINIMIZE
    # subprocess.Popen(qingtian_path, startupinfo=info)

    # 这里启动也需要停一阵子（至少2秒）

    time.sleep(2)
    ori_ss=ss
    qingtian_hd=None
    while not qingtian_hd:
        qingtian_hd=win32gui.FindWindowEx(None,0,0,qingtian_name)
    feedSS_hd=get_hd_from_child_hds(qingtian_hd,6,'')
    win32gui.SendMessage(feedSS_hd,win32con.WM_SETTEXT,0,ss)
    time.sleep(2)
    print("gg")

    # 这里有爬虫，需要停一阵子（至少1秒）...

    # time.sleep(2)
    # huoquzhong_hd=get_hd_from_child_hds(qingtian_hd,5,"获取")
    # cnt=0
    # while cnt!=5:



    # bookmark_pos=(755, 378)
    # click_on_pos(bookmark_pos)

    # # 全选操作

    # win32api.keybd_event(17,0,0,0)  #ctrl键位码是17
    # win32api.keybd_event(65,0,0,0)  #A键位码是65
    # win32api.keybd_event(65,0,win32con.KEYEVENTF_KEYUP,0) #释放按键
    # win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)

    # # 复制操作

    # win32api.keybd_event(17,0,0,0)  #ctrl键位码是17
    # win32api.keybd_event(67,0,0,0)  #C键位码是67
    # win32api.keybd_event(67,0,win32con.KEYEVENTF_KEYUP,0) #释放按键
    # win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)

    # time.sleep(1)

    # text = getText()  # 得到剪切板上的数据
    # # byte_str_charset = chardet.detect(byte_str)  # 获取字节码编码格式
    # # print(byte_str_charset)
    # # byte_str = str(byte_str, byte_str_charset.get('encoding'))  # 将八进制字节转化为字符串

    bookmark_hd=get_hd_from_child_hds(qingtian_hd,1,'')

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

    error_line = "没有查询到此SS的书签！"
    # try:
    #     print("Text:\t",text)
    # except UnicodeEncodeError:
    #     print("Text:\t",bad_filename(text))
    # print("Text type:\t",type(text))
    print("Text len:", len(text))
    if error_line in text:
        ss = "error_" + ss
    try:
        with open(target_dir2 + os.sep + ss + ".txt", "w", encoding="utf-8") as f:
            if len(text) <= 10:
                raise Exception
            f.write(text)
        if filename != None:
            assert not filename.endswith(".pdf")
            os.rename(target_dir2 + os.sep + ss + ".txt", target_dir2 + os.sep + ss + "ssidssid" + filename + ".txt")
        with open(target_dir2 + os.sep + "already_save.txt", "a", encoding="utf-8") as f:
            f.write(ori_ss + "\n")
    except Exception:
        if os.path.exists(target_dir2 + os.sep + ss + ".txt"):
            os.remove(target_dir2 + os.sep + ss + ".txt")
        if error_dir != None:
            if not os.path.exists(error_dir):
                os.makedirs(error_dir)
            with open(f"{error_dir}{os.sep}fetch-errors.txt", "a", encoding="utf-8") as f:
                f.write(ss + "\t\t\t" + filename + "\n")
        print(f"{ss} 无法写入！")
        pass

    win32gui.PostMessage(qingtian_hd,win32con.WM_CLOSE,0,0)

    # 防止写到另一个框框里的文件...
    
    time.sleep(3)
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

# save_catalog_from_ss("10400487")
# sys.exit(0)

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