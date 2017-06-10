import pymysql
from twkorean import TwitterKoreanProcessor
import pprint
import os

def makeDict(commentData):
    d = {}
    processor = TwitterKoreanProcessor()
    term_num = 0

    for text in commentData:
        tokens = processor.tokenize(text)
        processed = [x for x in tokens if x[1] == 'Noun' or x[1] == 'Verb' or x[1] == 'Adjective']
        for token in processed:
            if token[0] not in d.keys():
                term_num += 1
                d[token[0]] = term_num
    print(d)
    return d

def makeSVMData(data, dict, keyword_list):

    svmdata = {}
    processor = TwitterKoreanProcessor()
    docID = [0 for i in range(len(keyword_list))]
    for x in data:
        key_idx = x[0]-1
        keyword = keyword_list[key_idx][0]
        classes = x[1]

        if keyword not in svmdata.keys():
            svmdata[keyword] = {}
        docID[key_idx] += 1

        svmdata[keyword][docID[key_idx]] = {}
        svmdata[keyword][docID[key_idx]][0] = classes

        text = x[3]
        tokens = processor.tokenize(text)
        processed = [x for x in tokens if x[1] == 'Noun' or x[1] == 'Verb' or x[1] == 'Adjective']
        for token in processed:
            try:
                svmdata[keyword][docID[key_idx]][dict[token[0]]] += 1
            except:
                try:
                    svmdata[keyword][docID[key_idx]][dict[token[0]]] = 1
                except:
                    pass
    pprint.pprint(svmdata)
    return svmdata


def makeTrainData(svmdata):

    for keyword in svmdata.keys():
        f = open(str(keyword) + ".dat", 'w')

        for docID in svmdata[keyword].keys():
            templist = sorted(svmdata[keyword][docID].items())
            if str(templist[0][1]) == "2":
                f.write("-1")
            else:
                f.write(str(templist[0][1]))
            for x in templist[1:]:
                f.write(' ' + str(x[0]) + ':' + str(x[1]))
            f.write('\n')
        f.close()

def trainSVM(keyword_list):
    for keyword in keyword_list:
        key = str(keyword[0])
        cmd = "svm_learn " + key + ".dat" + ' ' + key + ".model"
        os.system(cmd)


def test(Dict, keyword_list):
    conn = pymysql.connect(host='220.230.112.94', user='dbmaster', password='dbmaster', db='spring', charset='utf8')
    curs = conn.cursor()
    sql = "select * from new_comment"
    curs.execute(sql)

    comment_list = curs.fetchall()
    print(comment_list)

    conn.close()

    svmdata = makeSVMData(comment_list, Dict, keyword_list)

    for keyword in svmdata.keys():
        f = open("test" + str(keyword) + ".dat", 'w')

        for docID in svmdata[keyword].keys():
            templist = sorted(svmdata[keyword][docID].items())
            if str(templist[0][1]) == "2":
                f.write("-1")
            else:
                f.write(str(templist[0][1]))
            for x in templist[1:]:
                f.write(' ' + str(x[0]) + ':' + str(x[1]))
            f.write('\n')
        f.close()

conn = pymysql.connect(host='220.230.112.94', user='dbmaster', password='dbmaster', db='spring', charset='utf8')
curs = conn.cursor()

sql = "select * from news_keyword"
curs.execute(sql)

keyword_list = curs.fetchall()
print(keyword_list)

sql = "select * from news_comment"
curs.execute(sql)

comment_list = curs.fetchall()
print(comment_list)

conn.close()

Dict = makeDict([x[3] for x in comment_list])
SVMData = makeSVMData(comment_list, Dict, keyword_list)
makeTrainData(SVMData)
trainSVM(keyword_list)
test(Dict, keyword_list)