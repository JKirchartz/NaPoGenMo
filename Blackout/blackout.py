#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 jkirchartz <me@jkirchartz.com>
#
# Distributed under terms of the NPL (Necessary Public License) license.

"""
Generate blackout poetry from a random newspaper article

Ensuring common word using Dwyl's copy of the Infochimps 350,000 simple english
words from: https://github.com/dwyl/english-words
"""

# TODO: find rhyming words to keep from text, block out more unique words -- keep more common words (not just stopwords)
import random, re
import newspaper
import codecs
from pattern.en import parsetree


# import most common words
with codecs.open("words.txt", encoding='utf-8') as word_file:
    english_words = set(word.strip().lower() for word in word_file)

# blackout anything that isn't a space
def blackout(word):
    return re.sub(r"\S", u"█", word)

# blackout words _not_ in the list of common words
def blackout_hard_words(word):
    if word.lower() not in english_words:
        return blackout(word)
    else:
        return word;

def generate():
    papers = [u'http://usatoday.com', u'http://nhgazette.com', u'http://post-gazette.com', u'http://cnn.com', u'http://nytimes.com', u'http://fox13news.com', u'http://wired.com']
    paper = random.choice(papers)
    news = newspaper.build(paper)
    if len(news.articles) is 0:
      return
    articles = news.articles[:]
    article = random.choice(articles)
    article.download()
    article.parse()

    s = parsetree(article.text, relations=True, lemmata=True)

    output = list(u'')
    output.append(u'\n---\n\n')
    output.append(u'article:')
    output.append(article.url)
    output.append(u'\n---\n\n')
    for sentence in s:
        for chunk in sentence.chunks:
            sentence_fragment = u' '.join([(blackout_hard_words(w.string)) for w in chunk.words])
            sentence_fragments = sentence_fragment.split()
            # TODO: blackout random words in sentence fragment, blackout slightly less fragments
            if random.random() < 0.8:
                output.append(blackout(sentence_fragment))
            else:
                output.append(sentence_fragment)

    return u' '.join(output)

output = list(u'')
for i in range(0,10):
     tmp = generate()
     if tmp:
        output.append(tmp)


with codecs.open('poetry.txt', 'wa', encoding='utf-8') as f:
    f.write(u'\n\n'.join(output))
