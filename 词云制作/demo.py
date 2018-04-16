#!/usr/bin/env python
#-*- coding: utf-8 -*-
from os import path
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random
import os

font = path.join(path.dirname(__file__), 'DroidSansFallbackFull.ttf')

def grey_color_func(word, font_size, position, orientation, random_stata=None, **kwargs):
    return 'hsl(0, 0%%, %d%%)' % random.randint(60, 100)



d = path.dirname(__file__)


mask = np.array(Image.open(path.join(d, '3.png')))


text = open(u'1.txt').read()

text = text.replace(u"程心说", u"程心")
text = text.replace(u"程心和", u"程心")
text = text.replace(u"程心问", u"程心")

stopwords = set(STOPWORDS)
stopwords.add("int")
stopwords.add("ext")

wc = WordCloud(font_path=font, max_words=2000, mask=mask, stopwords=stopwords, margin=10,
               random_state=1).generate(text)

default_colors = wc.to_array()
plt.title("Custom colors")
plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3))
wc.to_file('a_new_hope.png')
plt.axis("off")
plt.figure()
plt.title(u"三体-词频统计")
plt.imshow(default_colors)
plt.axis("off")
plt.show()

