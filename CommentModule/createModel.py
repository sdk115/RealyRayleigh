import pymysql
import os
import makeDict as d

def trainSVM(keyword_list):
    for keyword in keyword_list:
        key = str(keyword[0])
        cmd = "svm_learn train" + key + ".dat" + ' ' + key + ".model"
        os.system(cmd)


def test(Dict, keyword_list):
    conn = pymysql.connect(host='220.230.112.94', user='dbmaster', password='dbmaster', db='spring', charset='utf8')
    curs = conn.cursor()
    sql = "select * from news_comment"
    curs.execute(sql)

    comment_list = curs.fetchall()

    conn.close()

    svmdata = d.makeSVMData(comment_list, Dict, keyword_list)

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

conn.close()
print(comment_list)
Dict = d.loadDict()
print("dict", Dict)
SVMData = d.makeSVMData(comment_list, Dict, keyword_list)
print("svm", SVMData)
d.svmData2dat(SVMData, True)
trainSVM(keyword_list)
test(Dict, keyword_list)