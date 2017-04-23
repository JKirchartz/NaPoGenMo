#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 jkirchartz <me@jkirchartz.com>
#
# Distributed under terms of the NPL (Necessary Public License) license.

"""
Generate blackout poetry from a random newspaper article

"""

import random, re
import newspaper
from pattern.en import parsetree

papers = [u'http://nhgazette.com', u'http://post-gazette.com', u'http://cnn.com', u'http://nytimes.com', u'http://fox13news.com']
paper = newspaper.build(random.choice(papers))
print "pick one out of %s articles" % len(paper.articles);
articles = paper.articles[:]
article = random.choice(articles)
print "article url: %s" % article.url
article.download()
article.parse()

s = parsetree(article.text, relations=True, lemmata=True)

output = list()
for sentence in s:
    for chunk in sentence.chunks:
        sentence_fragment = ' '.join([(w.string) for w in chunk.words])
        sentence_fragment = sentence_fragment.decode()
        sentence_fragment = sentence_fragment.encode('ascii', 'ignore')
        if random.random() > 0.7:
            output.append(re.sub(r"\S", "█", sentence_fragment))
        else:
            output.append(sentence_fragment)

print ' '.join(output)
