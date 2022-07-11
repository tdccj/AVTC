# coding = utf-8
# 录播自动转封装v2.0 @tdccj

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import time
from ffmpy3 import *
import os

cwd = os.getcwd()

try:
    zm = open(cwd + "\\录播自动转封装设置.zm", "r")
    The_Path = zm.readline()
    print(The_Path)
    zm.close()

except FileNotFoundError:
    zm = open(cwd + "\\录播自动转封装设置", "w")
    The_Path = input("输入路径")
    zm.write(The_Path)
    zm.close()

print("监控中")

Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

lu_jing = "创建变量"


def zhuan_ma(lu_jing):  # 用来执行转码操作
    lu_jing_out = lu_jing[:-3] + "mp4"
    ff = FFmpeg(
        inputs={lu_jing: None},
        outputs={lu_jing_out: None}
    )
    ff.run()
    print("转码完毕")


class Watch(FileSystemEventHandler):  # 用来接受events的反馈
    def on_modified(self, event):
        print(f'文件修改:{event.src_path}', Time)
        lu_jing = str(event.src_path)

        if lu_jing[-3:] == "flv":  # 判断是否为录播文件
            print("判断为TRUE")
            zhuan_ma(lu_jing)


if __name__ == "__main__":  # 用observe对目录进行检测
    path = The_Path
    event_handler = Watch()
    observer = Observer()
    try:
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
    except FileNotFoundError:
        zm = open(cwd + "\\录播自动转封装设置.zm", "w")
        The_Path = input("输入路径2")
        zm.write(The_Path)
        zm.close()
        try:
            path = The_Path
            event_handler = Watch()
            observer = Observer()
            observer.schedule(event_handler, path, recursive=True)
            observer.start()
        except FileNotFoundError:
            print("路径仍然错误，请重启")
    try:
        while True:  # 用来保证程序持续执行
            time.sleep(1)

    except KeyboardInterrupt:  # 除了程序被用户中断
        observer.stop()
