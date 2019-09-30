import requests
from bs4 import BeautifulSoup
from konlpy.tag import Twitter
from collections import Counter
from wordcloud import WordCloud

def get_titles(start, end):
    title_list = []
    start = start
    end = end+1
    for i in range(start,end):
        page_no = str(i)
        r = requests.get("http://www.jbnu.ac.kr/kor/?menuID=139&pno="+page_no)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        titles = soup.select('.page_list .ta_bo .left > span > a')
        for title in titles:
            text = title.text.replace('\r\n\t\t\t\t\t\t\t','')
            text = text.replace('\n','')
            title_list.append(text)
    return title_list

def make_wordcloud(title_list, word_count):
    twitter = Twitter()

    sentences_tag = []
    for sentence in title_list:
        morph = twitter.pos(sentence)
        sentences_tag.append(morph)
        print(morph)
        print('-'*30)

    print(sentences_tag)
    print('\n'*3)

    noun_adj_list = []

    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun', 'Adjective']:
                noun_adj_list.append(word)
    counts = Counter(noun_adj_list)
    common_word_list = counts.most_common(word_count)

    return common_word_list


if __name__=='__main__':
    title_list = get_titles(1, 200)

    noun_adj_list = make_wordcloud(title_list, 30)
