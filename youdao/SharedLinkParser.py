# -*- coding: utf-8 -*-
import urllib

import requests
from urllib.parse import urlparse
import yaml


# 根据 url 链接 获取id
def get_note_id_by_url(url):
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
    # 获取 id
    note_id = get_note_id_by_url(url)
    print(note_id)

