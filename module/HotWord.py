# coding: utf-8

from gensim.models import TfidfModel
from gensim.corpora import Dictionary
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import jieba.posseg as pseg
from functools import reduce

class TextsAnalyse:
    def __init__(self, corpus):
        self.__corpus = corpus
        self.__tokenCorpus = None
        self.__filteredTokenCorpus = None
        self.__normalCorpus = None
        self.__dictionary = None
        self.__frequency = None
        self.__stopWordsSet = None
        self.__validFlag = ['an','b','i','j','l','ng','n','nr','nt','nz','vn','un']
        jieba.load_userdict("../data/myWordDict.txt")
       
    def get_key_words(self, topK):
        if not self.__frequency:
            self.get_frequency()
        items = list(self.__frequency.items())
        items.sort(key=self.__takeSecond, reverse = True)
        keyWords = [each[0] for each in items[0:topK]]
        return keyWords
    
    def get_original_corpus(self):
        return self.__corpus
    
    def get_tokenCorpus(self):
        if not self.__tokenCorpus:
            return self.cut_with_tag()
        else:
            return self.__tokenCorpus
    
    def get_cut(self, mode='accuracy', HMM=False):
        if mode == 'accuracy':
            return [list(jieba.cut(stc, HMM)) for stc in __corpus]
        elif mode == 'all':
            return [list(jieba.cut(stc, cut_all=True, HMM=HMM)) for stc in __corpus]
        else:
            return [list(jieba.cut_for_search(stc, HMM)) for stc in __corpus]
        
    def cut_with_tag(self, HMM=False):
        stcTokenList = [jieba.posseg.cut(each, HMM) for each in self.__corpus]
        self.__tokenCorpus = [[(pair.word, pair.flag) for pair in stcToken] for stcToken in stcTokenList]
        return self.__tokenCorpus
            
    def __filter_stop_words(self, token):
        word, flag = token
        if word in self.__stopWordsSet:
            return False
        if flag not in self.__validFlag:
            return False
        return True
        
    def filter_corpus(self, stopWords = None):
        if not self.__stopWordsSet:
            with open("stop_word.txt", "r", encoding="utf-8") as stop_word_file:
                stopWords = [line.replace('\n', '') for line in stop_word_file]
            self.__stopWordsSet = set(stopWords)
        if not self.__tokenCorpus:
            self.get_tokenCorpus()
        self.__filteredTokenCorpus = [list(filter(self.__filter_stop_words, each)) for each in self.__tokenCorpus]
        self.__normalCorpus = [ [w[0] for w in eachList] for eachList in self.__filteredTokenCorpus]
        
    def get_dictionary(self):
        if not self.__normalCorpus:
            self.filter_corpus()
        self.__dictionary = Dictionary(self.__normalCorpus)
        return self.__dictionary
    
    def get_normalCorpus(self):
        if not self.__normalCorpus:
            self.filter_corpus()
        return self.__normalCorpus
    
    def get_frequency(self):
        if not self.__dictionary:
            self.get_dictionary()
        corpusBow = [self.__dictionary.doc2bow(line) for line in self.__normalCorpus]
        model = TfidfModel(corpusBow, normalize=True)  # fit model
        vector = model[self.__dictionary.doc2bow(reduce(lambda x,y:x+y, self.__normalCorpus, []))]
        self.__frequency = dict([(self.__dictionary[w[0]], w[1]) for w in vector])
    
    def __takeSecond(self, elem):
        return elem[1]
    
    def show_word_cloud(self, num):
        if not self.__frequency:
            self.get_frequency()
        my_wordcloud = WordCloud(font_path="../data/font/simhei.ttf", max_words=num, background_color='white', width=800, height=600, max_font_size=100)
        my_wordcloud.generate_from_frequencies(self.__frequency)
        plt.imshow(my_wordcloud)
        plt.axis("off")
        plt.show()
        items = list(self.__frequency.items())
        items.sort(key=self.__takeSecond, reverse = True)
        print(items[0:num])
