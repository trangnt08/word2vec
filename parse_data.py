# -*- encoding: utf8 -*-
import os
import re
from bs4 import BeautifulSoup
import gensim

import utils
from io import open

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
        print "aaa ", sens_in_doc
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
if __name__ == '__main__':
    docs = parse_training_data('data2', 'data_clean')
    sentences = docs_to_sentences(docs)
    print sentences
    list_sens = getlist(sentences)
    print "\n... ", list_sens
    # model = gensim.models.Word2Vec(list_sens, size=100, window=2, min_count=3, workers=4, sg=1)
    model = gensim.models.Word2Vec(min_count=1, size=20, window=2, sg=1, iter=10)
    model.build_vocab(list_sens)
    # model.build_vocab([s.encode('utf-8').split() for s in sentences])
    # sentences = [s.encode('utf-8').split() for s in sentences]
    model.train(list_sens, total_examples=model.corpus_count, epochs=model.iter)
    # print"a aaaaaaaaaaaa ",(model[u'UBND'])
    kq = model.most_similar(positive=[u'công_ty'],topn=5)
    for i in range(len(kq)):
        print "a ",kq[i][0]

    kq2 = model.most_similar(positive=[u'xây_dựng'], topn=5)
    for i in range(len(kq2)):
        print "b ", kq2[i][0]
    # print kq[i][1]
    # model.build_vocab([[u'zzz']], update=True)
    # model.train([[u'zzz']], total_examples=model.corpus_count, epochs=model.iter)
    # print(model[u'jumps'])
    # print(model[u'zzz'])
    # print model.similarity('em', 'tinh')
    # model.most_similar(positive=['woman', 'king'], negative=['man'])
    # print model.most_similar(positive=['woman'])