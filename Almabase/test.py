import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Almabase.settings')

import django
import newspaper
import unicodedata
import nltk

django.setup()

from Classifer.models import *

def add_article(title,summary,url,author,keywords1):
    a=Article.objects.get_or_create(title=title,summary=summary,url=url,author=author)[0]
    a.save()
    articleid=a.id
    a=Keywords.objects.get_or_create(article=a)[0]
    print a
    print a.keywords
    for key in keywords1:
        k=KeywordList.objects.get_or_create(keyword=key)[0]
        k.save()
        if not k.keywords_set.filter(id=a.id):
            a.keywords.add(k)
            a.save()
    return articleid


def test_keywords(article,classifier):
    keys=Keywords.objects.get(article=article)
    print keys
    l=[k.keyword for k in keys.keywords.all()]
    test_set=[]
    keyset=[]
    for k in l:
        print k
        print classifier.prob_classify({'keyword':k}).logprob('keyword')
        test_set.append(({'keyword':k},classifier.classify({'keyword':k})))
    print nltk.classify.accuracy(classifier, test_set)

def testurl(url):
    a=newspaper.Article(url)
    a.download()
    a.parse()
    a.nlp()
    l1=a.keywords
    articleid=add_article(a.title,a.summary,url,a.authors[0],l1)
    art=Article.objects.get(id=articleid)


def article_keywords(article):
	keys=Keywords.objects.get(article=article)
	print keys
	l=[k.keyword for k in keys.keywords.all()]
	keyset=[]
	for k in l:
		keyset.append({'keyword':k})
	return keyset


if __name__ == '__main__':
    print "Starting testing of Bayes Classifer"
    labeled_articles = [(a, a.relevant) for a in Article.objects.all()[:(len(Article.objects.all())-1)]]
    print labeled_articles
    featuresets=[]
    for (article, relevant) in labeled_articles:
    	r=article_keywords(article)
    	for keys in r:
    		featuresets.append((keys,relevant))
    print featuresets
    train_set, test_set = featuresets[:(len(featuresets))], featuresets[(len(featuresets)-2):]
    print train_set
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    article=Article.objects.all()[(len(Article.objects.all())-2):]
    test_keywords(article[0],classifier)


