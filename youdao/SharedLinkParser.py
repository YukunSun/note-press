# -*- coding: utf-8 -*-
import urllib

import requests
from urllib.parse import urlparse
import yaml
from hashlib import blake2b
import logging
from enum import Enum

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('SharedLinkParser')


# the franchise which supported by now
class SupportedNote(Enum):
    YOUDAO_NOTE = 1


# 笔记概要信息：title、ctime etc.
URL_SHARE_INFO = 'https://note.youdao.com/yws/public/note/{}'
# 笔记的具体内容
URL_DETAIL = "https://note.youdao.com/yws/api/personal/file/{}?method=download&read=true&shareKey={}&cstk=HncM6MEm"


# generate article id by url
def aid(supported, url):
    h = blake2b(key=b'note-press-HsJ:JFDOIU)#$#$', digest_size=16)
    h.update(url.encode())
    if supported == SupportedNote.YOUDAO_NOTE:
        return 'yd-' + h.hexdigest()
    else:
        return h.hexdigest()


# 根据 url 链接 获取id
def parse_note_id_by_shared_url(url):
    # 获取 id
    url_attr = urlparse(url)
    query_strings = url_attr.query
    query = urllib.parse.parse_qs(query_strings, keep_blank_values=False,
                                  strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None)
    return query.get('id')[0]


FILE_NAME_NOTES_YML = "notes.yml"
notes_dir = "../test/youdao/" + FILE_NAME_NOTES_YML
notes = open(notes_dir, 'r')
notes_str = notes.read()
notes = yaml.load(notes_str, Loader=yaml.SafeLoader)
if notes is None:
    raise NameError('notes.yml\'s format is error.please check.')
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
    # <class 'dict'>: {'p': '/2A356BB5A34D4511B82AE2FD12E4E23B', 'ct': 1498141409, 'su': '', 'pr': 0, 'au': '', 'pv': 45, 'mt': 1505012633, 'sz': 204, 'domain': 1, 'tl': '我的后端知识体系.md'}
    shared_info = requests.get(url_share).json()
    p = shared_info.get('p')[1:]
    ctime = shared_info.get('ct')
    utime = shared_info.get('mt')
    title = shared_info.get('tl')
    # get note detail
    url_detail = URL_DETAIL.format(p, share_key)
    note_detail = requests.post(url_detail)

    # refresh notes.yml
    note_utime = note['utime']
    if note_utime is not None and note_utime >= utime:
        logger.warning('current article\'s version is up to date,ignore refresh,%s', url)
        continue
    note['utime'] = utime
    note['title'] = title[:-3]  # remove .md
    note['ctime'] = ctime
    note['aid'] = aid(SupportedNote.YOUDAO_NOTE, url)

    # update note
    text = note_detail.text
    print(text)
    """
    ---
    title:  "hello world "
    last_modified_at: 
    categories: 
      - 
    tags:
      - 
    toc: true
    toc_label: "Getting Started"
    ---
    article content...
    """

with open(notes_dir, "w") as f:
    yaml.dump(notes, f)
