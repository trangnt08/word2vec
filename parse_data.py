# -*- encoding: utf8 -*-
import os
import re
from bs4 import BeautifulSoup
import gensim
from pyvi.pyvi import ViTokenizer
from sklearn.externals import joblib
import numpy as np

import utils
from io import open

WORD_SIZE = 20

def clean_str_vn(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    """
    string = re.sub(r"[~`@#$%^&*-+]", " ", string)
    def sharp(str):
        b = re.sub('\s[A-Za-z]\s\.', ' .', ' '+str)
        while (b.find('. . ')>=0): b = re.sub(r'\.\s\.\s', '. ', b)
        b = re.sub(r'\s\.\s', ' # ', b)
        return b
    string = sharp(string)
    string = re.sub(r",","",string)
    string = re.sub(r"[()\"]", "", string)
    return string.strip().lower()

def parse_training_data(dataset, output):
    docs = []
    utils.mkdir(output)
    stack = os.listdir(dataset)
    print 'loading data in ' + dataset
    while (len(stack) > 0):
        file_name = stack.pop()
        file_path = dataset + '/' + file_name
        if (os.path.isdir(file_path)):  # neu la thu muc thi day vao strong stack
            utils.push_data_to_stack(stack, file_path, file_name)
        else:  # nguoc lai tien hanh readfile
            with open(file_path, 'r', encoding='utf-8') as ff:
                content = ff.read()
                bs = BeautifulSoup(content)
                docs.append([bs.text])
                # with open(output + '/' + file_name, 'w', encoding='utf-8') as f:
                #     f.write(bs.text)
    return docs

def docs_to_sentences(docs):
    sentenses = []
    for doc in docs:
        sens_in_doc = doc[0].split('\n')    # list cac cau cua 1 van ban
        sentenses.append(sens_in_doc)
    return sentenses # list chua list cac cau cua nhieu van ban
def getlist(sentences):
    list_sens = []
    for i in sentences: # i la 1 list cac cau cua 1 van ban
        for j in i: # j la 1 cau
            j = clean_str_vn(j)
            words = j.split(' ')    # word la 1 mang cac tu cua 1 cau
            words_clean = []
            for k in words:
                if k != '':
                    words_clean.append(k)
            # for k in words:
            #     if k != '':
            #         list_sens.append(k)    # list_sens la 1 list chua cac tu trong tat ca cac van ban
            if len(words_clean)>0:
                list_sens.append(words_clean) # list_sens la 1 list chua cac list tu da tach trong cau
    return list_sens

def load_model(model):
    print('loading model ...')
    if os.path.isfile(model):
        return joblib.load(model)
    else:
        return None


# def get_default_value:
#     return np.zeros((WORD_SIZE))

if __name__ == '__main__':

    # model = gensim.models.Word2Vec(list_sens, size=100, window=2, min_count=3, workers=4, sg=1)
    model = load_model('model/model.pkl')
    if model==None:
        docs = parse_training_data('data_raw', 'data_clean')
        sentences = docs_to_sentences(docs)
        list_sens = getlist(sentences)
        model = gensim.models.Word2Vec(min_count=1, size=WORD_SIZE, window=2, sg=1, iter=10)
        model.build_vocab(list_sens)
    # model.build_vocab([s.encode('utf-8').split() for s in sentences])
    # sentences = [s.encode('utf-8').split() for s in sentences]
        model.train(list_sens, total_examples=model.corpus_count, epochs=model.iter)
        joblib.dump(model,'model/model.pkl')


    while(1):
        ex = raw_input("Nhap 1 tu: ")
        if ex.lower()=='q':
            break
        ex = unicode(ex, encoding='utf-8')
        ex = ViTokenizer.tokenize(ex).lower()

        try:
            kq = model.most_similar(positive=[ex],topn=5)
            for i in range(len(kq)):
                print "a ", kq[i][0]
        except Exception as e:
            print e.message


    # kq1 = model.most_similar(positive=[u'công_an'], topn=5)
    # for i in range(len(kq1)):
    #     print " ", kq1[i][0]
    # kq2 = model.most_similar(positive=[u'kiểm_tra'], topn=5)
    # for i in range(len(kq2)):
    #     print kq2[i][0]
    # kq3 = model.most_similar(positive=[u'ngân_hàng'], topn=5)
    # for i in range(len(kq3)):
    #     print " ",kq3[i][0]

