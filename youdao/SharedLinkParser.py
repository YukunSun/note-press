# -*- coding: utf-8 -*-
import urllib

import requests
from urllib.parse import urlparse
import yaml

# 笔记概要信息：title、ctime etc.
URL_SHARE_INFO = 'https://note.youdao.com/yws/public/note/{}'
# 笔记的具体
URL_DETAIL = "https://note.youdao.com/yws/api/personal/file/{}?method=download&read=true&shareKey={}&cstk=HncM6MEm"


# 根据 url 链接 获取id
def parse_note_id_by_shared_url(url):
    # 获取 id
    url_attr = urlparse(url)
    query_strings = url_attr.query
    query = urllib.parse.parse_qs(query_strings, keep_blank_values=False,
                                  strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None)
    return query.get('id')[0]


notes_dir = "../test/youdao/notes.yml"
notes = open(notes_dir, 'r')
notes_str = notes.read()
notes = yaml.load(notes_str, Loader=yaml.SafeLoader)
for note in notes:
    url = note['url']
    if url is None:
        continue
    # 截取 shareKey
    share_key = parse_note_id_by_shared_url(url)
    if share_key is None:
        continue
    # 获取 title 等信息
    url_share = URL_SHARE_INFO.format(share_key)
    shared_info = requests.get(url_share).json()
    p = shared_info.get('p')[1:]
    ctime = shared_info.get('ct')
    utime = shared_info.get('mt')
    title = shared_info.get('tl')
    url_detail = URL_DETAIL.format(p, share_key)
    # todo
    note_detail = requests.post(url_detail).json()
    print(note_detail)
