# -*- coding: utf-8 -*-
import csv
from os.path import dirname, abspath, join

from django.core.exceptions import ObjectDoesNotExist, ValidationError


from 臺灣言語平臺.項目模型 import 平臺項目表
from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音相容教會羅馬字音標 import 臺灣閩南語羅馬字拼音相容教會羅馬字音標
from 臺灣言語工具.基本物件.公用變數 import 分字符號
from 臺灣言語工具.音標系統.閩南語.臺灣閩南語羅馬字拼音 import 臺灣閩南語羅馬字拼音


def 走台華():
    公家內容 = {
        '來源': {'名': '台文華文線頂辭典'},
    }
    for 第幾筆, (華語, 漢字, 臺羅) in enumerate(xls資料()):
        if 第幾筆 % 10 == 0:
            print('匯到第 {} 筆'.format(第幾筆))
        外語內容 = {
            '外語資料': 華語.strip()
        }
        外語內容.update(公家內容)
        閩南語內容 = {
            '文本資料': 漢字,
            '屬性': {'音標': 臺羅},
        }
        閩南語內容.update(公家內容)
        try:
            外語平臺項目 = 平臺項目表.加外語資料(外語內容)
            外語平臺項目編號 = 外語平臺項目.編號()
        except ValidationError as 錯誤:
            外語平臺項目編號 = 錯誤.平臺項目編號
        try:
            平臺項目表.揣編號(外語平臺項目編號).外語.翻譯文本.get(
                文本__文本資料=漢字, 文本__音標資料=臺羅
            )
        except ObjectDoesNotExist as s:
            pass
        else:
            print(華語, 漢字, 臺羅, '出現過矣！！')
            continue
        文本平臺項目 = 平臺項目表.外語翻母語(外語平臺項目編號, 閩南語內容)
        文本平臺項目.設為推薦用字()


def xls資料():
    這馬所在 = dirname(abspath(__file__))

    with open(join(這馬所在, 'Taihoa楊允言老師提供資料庫-漢字.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        for 這筆資料 in reader:
            台語羅馬字 = 這筆資料['台語羅馬字'].strip()
            台語羅馬字2 = 這筆資料['台語羅馬字2'].strip()
            if 台語羅馬字2 == '':
                音標 = (
                    拆文分析器
                    .建立句物件(台語羅馬字)
                    .轉音(臺灣閩南語羅馬字拼音相容教會羅馬字音標)
                    .轉音(臺灣閩南語羅馬字拼音, '轉閏號調')
                    .看型(物件分字符號=分字符號)
                )
            else:
                音標 = '{}/{}'.format(
                    拆文分析器.建立句物件(台語羅馬字)
                    .轉音(臺灣閩南語羅馬字拼音相容教會羅馬字音標)
                    .轉音(臺灣閩南語羅馬字拼音, '轉閏號調')
                    .看型(物件分字符號=分字符號),
                    拆文分析器.建立句物件(台語羅馬字2)
                    .轉音(臺灣閩南語羅馬字拼音相容教會羅馬字音標)
                    .轉音(臺灣閩南語羅馬字拼音, '轉閏號調')
                    .看型(物件分字符號=分字符號)
                )
            for 華語 in 這筆資料['華語對譯'].strip(';').split(';'):
                yield (華語, 這筆資料['台語漢字'].strip(), 音標)
