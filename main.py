from ins import Ins
from weibo import Weibo
import time

def main():
    ins = Ins()
    weibo = Weibo()
    ins.user = "jaychou"

    while True:
        ins.checkUpdate()
        time.sleep(5)
        weibo.checkNewDirs()
        time.sleep(1200)


main()