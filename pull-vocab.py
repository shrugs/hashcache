import io
import random
from bs4 import BeautifulSoup
import requests


# 1-indexed
TOTAL_LESSONS=23

BASE_URL='http://ohelo.org/japn/lang/genki_vocab_table.php?lesson='

HEADERS = ['kana', 'kanji', 'english']

def url_for_lesson(lesson_id):
    return '{}{}'.format(BASE_URL, lesson_id)


def build_vocab_list():
    vocabs = []
    for lesson_id in xrange(1, TOTAL_LESSONS + 1):
        r = requests.get(url_for_lesson(lesson_id))
        soup = BeautifulSoup(r.content, 'html.parser')
        # import ipdb; ipdb.set_trace()
        for tr in soup.find_all('tr'):
            vocab = {}
            tds = tr.find_all('td')
            vocab['kana'] = tds[0].text
            vocab['kanji'] = tds[1].text
            if len(tds) == 4:
                # we have romaji
                vocab['romaji'] = tds[2].text
                vocab['english'] = tds[3].text
            else:
                # no romaji
                vocab['english'] = tds[2].text

            vocabs.append(vocab)

    return vocabs

vocabs = build_vocab_list()

random.shuffle(vocabs)

with io.open('vocab.md', 'w', encoding='utf8') as f:
    f.write(u"""
---
title: Japanese Vocab from Genki I, II
date: October 22, 2017
---
    """)

    for vocab in vocabs:
        f.write(u"""
# {}
{}

- {}
        """.format(
            vocab['kanji'] if vocab['kanji'] else vocab['kana'],
            vocab['kana'] if vocab['kanji'] else '',
            vocab['english']
        ))

