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
from pattern.en import parsetree, mood


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

def blackout_random_word(words):
    for i,w in enumerate(words):
          if random.random() > 0.5:
              words[i] = blackout(w)
          else:
              words[i] = w
    return words

def generate():
    papers = [u'http://theonion.com', u'http://dailymail.co.uk', u'http://www.bbc.co.uk/', u'http://usatoday.com', u'http://nhgazette.com', u'http://post-gazette.com', u'http://cnn.com', u'http://nytimes.com', u'http://fox13news.com', u'http://wired.com']
    papers = papers + newspaper.popular_urls()
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
    output.append(u'title:')
    output.append(article.title)
    output.append(u'\narticle:')
    output.append(article.url)
    output.append(u'\n---\n\n')
    for sentence in s:
        if mood(sentence) not in set(['imperative', 'conditional', 'subjunctive']): # filter out definitive facts
            output.append(blackout(sentence.string))
        else:
            last_chunk = ''
            for chunk in sentence.chunks:
              if (chunk.type is last_chunk): # reduce repeating chunk types
                    output.append(u' '.join([(blackout(w.string)) for w in chunk.words]))
              else:
                # only use words in our dictionary (to avoid names, etc)
                sentence_fragment = u' '.join([(blackout_hard_words(w.string)) for w in chunk.words])
                # black out random words in sentence fragment
                sentence_fragment = u' '.join(blackout_random_word(sentence_fragment.split()))
                # black out random phrases
                if random.random() < 0.6:
                    output.append(blackout(sentence_fragment))
                else:
                    output.append(sentence_fragment)
            last_chunk = chunk.type

    return u' '.join(output)

output = list(u'')
for i in range(0,10):
     tmp = generate()
     if tmp:
        output.append(tmp)


with codecs.open('poetry.txt', 'a', encoding='utf-8') as f:
    f.write(u'\n\n'.join(output))
