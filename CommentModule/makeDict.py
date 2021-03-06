from twkorean import TwitterKoreanProcessor
import pymysql
import os

def makeDict(commentData):
    d = []
    processor = TwitterKoreanProcessor()

    for text in commentData:
        tokens = processor.tokenize(text)
        processed = [x for x in tokens if x[1] == 'Noun' or x[1] == 'Verb' or x[1] == 'Adjective']
        for token in processed:
            if token[0] not in d:
                d.append(token[0])

    conn = pymysql.connect(host='220.230.112.94', user='dbmaster', password='dbmaster', db='spring', charset='utf8mb4')
    curs = conn.cursor()
    sql = "INSERT INTO dictionary(term) VALUES(%s)"
    try:
        curs.executemany(sql, tuple(d))
    except pymysql.IntegrityError:
        pass

    conn.commit()
    conn.close()

    return d

def loadDict():

    conn = pymysql.connect(host='220.230.112.94', user='dbmaster', password='dbmaster', db='spring', charset='utf8mb4')
    curs = conn.cursor()
    sql = "select term, id from dictionary"
    dict_size = curs.execute(sql)
    rows = curs.fetchall()

    print(dict_size, rows)
    d = dict(rows)

    conn.close()
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
    return svmdata

def svmData2dat(svmdata, fortrain=False):
    for keyword in svmdata.keys():
        if fortrain == True:
            f = open("train" + str(keyword) + ".dat", 'w')
        else:
            f = open("forClassify" + ".dat", 'w')

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

def classify(filename, keyword_idx):
    cmd = "svm_classify " + filename + '.dat ' + str(keyword_idx) + ".model" + ' ' + filename +".classify"
    os.system(cmd)

def loadClassify(filename):
    classes = []
    for x in open(filename, 'r'):
        x = float(x)
        if x > 0:
            classes.append(1)
        else:
            classes.append(2)

    return classes