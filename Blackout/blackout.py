#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 jkirchartz <me@jkirchartz.com>
#
# Distributed under terms of the NPL (Necessary Public License) license.

"""
Generate blackout poetry from a random newspaper article

10,000 most common words: http://splasho.com/upgoer5/phpspellcheck/dictionaries/1000.dicin

"""

# TODO: find rhyming words to keep from text, block out more unique words -- keep more common words (not just stopwords)
import random, re
import newspaper
from pattern.en import parsetree


# import most common words
with open("1000.dicin") as word_file:
    english_words = set(word.strip().lower() for word in word_file)

# fix word encoding (Assuming everything is utf-8)
def fix(word):
    word = word.decode('utf-8', 'ignore')
    return word.encode('ascii', 'ignore')

# blackout anything that isn't a space
def blackout(word):
    return re.sub(r"\S", "█", fix(word))

# blackout words _not_ in the list of common words
def blackout_hard_words(word):
    word = fix(word)
    if word.lower() not in english_words:
        return blackout(word)
    else:
        return word;

def generate():
    papers = [u'http://nhgazette.com', u'http://post-gazette.com', u'http://cnn.com', u'http://nytimes.com', u'http://fox13news.com', u'http://medium.com', u'http://wired.com']
    paper = random.choice(papers)
    news = newspaper.build(paper)
    if len(news.articles) is 0:
      return "failed reading from %s" % paper
    print "pick one out of %s articles from %s" % (len(news.articles), paper);
    articles = news.articles[:]
    article = random.choice(articles)
    article.download()
    article.parse()

    s = parsetree(fix(article.text), relations=True, lemmata=True)

    output = list()
    output.append('\n---\n\n')
    output.append('article:')
    output.append(article.url)
    output.append('\n---\n\n')
    for sentence in s:
        for chunk in sentence.chunks:
            sentence_fragment = ' '.join([(blackout_hard_words(w.string)) for w in chunk.words])
            if random.random() < 0.8:
                output.append(blackout(sentence_fragment))
            else:
                output.append(fix(sentence_fragment))

    return ' '.join(output)

for i in range(0,10):
    print generate();

