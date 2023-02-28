import os
import re

import requests


class Crawler(requests.Session):

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }

    def __init__(self):
        super().__init__()
        self.headers.update(Crawler.header)

    def set_cookies(self, cookies):
        """传入一个字典，用于设置 cookies"""

        requests.utils.add_dict_to_cookiejar(self.cookies, cookies)

    def download_bin(self, url, file_path, stream=True, chunk_size=1024, **kw):
        """下载二进制文件"""

        res = self.get(url, stream=stream, **kw)
        tmp_path = file_path + ".t"
        try:
            with open(tmp_path, "wb") as f:
                if stream:
                    for chunk in res.iter_content(chunk_size=chunk_size):
                        if not chunk:
                            break
                        f.write(chunk)
                else:
                    f.write(res.content)
        except:
            os.remove(tmp_path)
            print("[warn] {} failed to download".format(file_path))
        if os.path.exists(file_path):
            with open(tmp_path, "rb") as fr:
                with open(file_path, "wb") as fw:
                    fw.write(fr.read())
            os.remove(file_path)
        else:
            os.rename(tmp_path, file_path)

    def download_text(self, url, file_path, **kw):
        """下载文本，以 UTF-8 编码保存文件"""

        res = self.get(url, **kw)
        res.encoding = res.apparent_encoding
        with open(file_path, 'w', encoding='utf_8') as f:
            f.write(res.text)


class BililiCrawler(Crawler):

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
        'Referer': 'https://www.bilibili.com',
        'cookie':"cookie: buvid3=E1C8F458-A50C-6DC7-A941-7777DCC8FA7F26653infoc; b_nut=1676622526; i-wanna-go-back=-1; _uuid=49CFCD58-2CD3-83F6-1010F1-74FA89CB941627185infoc; buvid4=F8909C7B-A578-1E9A-E825-186839F1B47428046-023021716-sXvDROX529rDGdn43rAdyw%3D%3D; header_theme_version=CLOSE; CURRENT_FNVAL=4048; DedeUserID=352695712; DedeUserID__ckMd5=340b2d85b5da6c31; rpdid=|(JY~uJR|lkY0J'uY~YYJuku|; b_ut=5; nostalgia_conf=-1; CURRENT_QUALITY=120; hit-new-style-dyn=0; hit-dyn-v2=1; fingerprint=4a54a45233b5a935db400a9589eb0627; buvid_fp_plain=undefined; buvid_fp=4a54a45233b5a935db400a9589eb0627; SESSDATA=28f5500a%2C1693112198%2C68107%2A21; bili_jct=1062755390a0a95b6799a4da3eb4eec1; sid=63ql8rpu; bp_video_offset_352695712=767691744704725000; b_lsid=81AEECA3_18697B47C12; home_feed_column=5; PVID=5; innersign=1",
    }

    def __init__(self):
        super().__init__()
        self.headers.update(BililiCrawler.header)
