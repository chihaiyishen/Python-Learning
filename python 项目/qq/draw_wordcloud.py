import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import io
import jieba

def draw_signature():
    with io.open('qq_word.txt', 'r', encoding='utf-8') as f:
        siglist = f.readlines()
        text = "".join(siglist)
        wordlist = jieba.cut(text, cut_all=True)
        word_space_split = " ".join(wordlist)
    coloring = np.array(Image.open('3.png'))
    my_wordcloud = WordCloud(background_color="white", max_words=2000,
                         mask=coloring, max_font_size=60, random_state=42, scale=10,
                         font_path="DroidSansFallbackFull.ttf").generate(word_space_split)
    image_colors = ImageColorGenerator(coloring)
    plt.imshow(my_wordcloud.recolor(color_func=image_colors))
    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    draw_signature()