import mysql.connector as connector
import CitationRetrieval

from datetime import datetime


database = connector.connect(host='localhost',database='citations',user='root',password='root')
cursor=database.cursor()

def get_orrcids():
    cursor.execute('select orcid from report')
    ids=cursor.fetchall()
    orcids=[]
    for i in ids:
        orcids.append(i[0])
    return orcids.copy()

def updateTables():
    currDate = datetime.now().strftime('%B')+"_"+str(datetime.now().year)

    

    cursor.execute('select orcid from report')
    ids=cursor.fetchall()
    orcids=[]
    for i in ids:
        orcids.append(i[0])

    cursor.execute('desc report')
    ret=cursor.fetchall()
    avail=[]
    for i in ret:
        avail.append(i[0])

    if currDate not in avail:
        cursor.execute('alter table report add column '+currDate+' VARCHAR(45)')
        for i in orcids:
            print(i)
            tmp=CitationRetrieval.citeCount(i)
            cursor.execute('update report set '+currDate+' = \''+str(tmp)+'\' where orcid = \''+i+'\'')
            print(tmp)
    else:
        for i in orcids:
            print(i)
            tmp=CitationRetrieval.citeCount(i)
            cursor.execute('update report set '+currDate+' = \''+str(tmp)+'\' where orcid = \''+i+'\'')
            print(tmp)
    database.commit()

    print("Database updated successfully! :)")

def get_label():
    cursor.execute('desc report')
    ret=cursor.fetchall()
    avail=[]
    
    for i in ret:
        #print(i[0])
        avail.append(i[0])
    label=[]
    for i in range(2,len(avail)):
        label.append(avail[i])
    return label.copy()

def get_formated_name(ID):
    cursor.execute("select name from report where orcid = %s",(ID,))
    nameresult=cursor.fetchone()

    name=nameresult[0]
    return name

def get_formated_data(ID):
    cursor.execute("select * from report where orcid = %s",(ID,))
    result=cursor.fetchone()
    li=[]
    tmp=0
    #print(result)
    for i in range(2,len(result)):
        if(i<len(result)):
            li.append(int(result[i])-tmp)
            tmp=int(result[i])
    return li.copy()


def formatted():
    orc=get_orrcids()
    res={}
    for i in orc:
        name=get_formated_name(i)
        res[name]=get_formated_data(i)
    return res.copy()


def get_rowcol():
    cursor.execute('desc report')
    ret=cursor.fetchall()
    avail=[]
    for i in ret:
        print(i[0])
        avail.append(i[0])
    cursor.execute('select * from report')
    result=cursor.fetchall()
    
    dat=[avail.copy()]

    for i in result:
        dat.append(list(i))
    print("returning list")
    return dat

if __name__=="__main__":
    #updateTables()
    
    print(formatted())
    print(get_label())