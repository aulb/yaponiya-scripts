"""
THIS CODE IS NO LONGER IN USE.
THIS CODE IS NO LONGER IN USE.
THIS CODE IS NO LONGER IN USE.
THIS CODE IS NO LONGER IN USE.
THIS CODE IS NO LONGER IN USE.
"""

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import MeCab

### Constants
MECAB_MODE = 'mecabrc'
PARSE_TEXT_ENCODING = 'utf-8'

### Functions
def main():
    sample_u = u"ライ麦畑のつかまえ役、そういったものに僕はなりたいんだよ。馬鹿げてることは知ってるよ。でも、ほんとうになりたいものといったらそれしかないね。"
    words_dict = parse(sample_u)
    print("All:", ",".join(words_dict['all']))
    print("Nouns:", ",".join(words_dict['nouns']))
    print("Verbs:", ",".join(words_dict['verbs']))
    print("Adjs:", ",".join(words_dict['adjs']))
    return


def parse(unicode_string):
    tagger = MeCab.Tagger(MECAB_MODE)
    node = tagger.parseToNode(unicode_string)

    words = []
    nouns = []
    verbs = []
    parts = []
    adjs = []
    while node:
        pos = node.feature.split(",")[0]
        print(pos + ' ' + node.feature)
        # unicode 型に戻す
        word = node.feature.split(",")[-3]
        if pos == "名詞":
            nouns.append(word)
        elif pos == "動詞":
            verbs.append(word)
        elif pos == "形容詞":
            adjs.append(word)
        elif pos == "助詞":
            parts.append(word)
        words.append(word)
        node = node.next
    parsed_words_dict = {
        "all": words[1:-1], # 最初と最後には空文字列が入るので除去
        "nouns": nouns,
        "verbs": verbs,
        "parts": parts,
        "adjs": adjs
        }
    return parsed_words_dict

### Execute
if __name__ == "__main__":
    unicode_string = "ライ麦畑のつかまえ役、そういったものに僕はなりたいんだよ。馬鹿げてることは知ってるよ。でも、ほんとうになりたいものといったらそれしかないね。"
    b = parse(unicode_string)
