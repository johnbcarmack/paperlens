#ArNet
import MySQLdb
import sys
sys.path.append("../")
from paper import Paper
import paperlens_import

connection = MySQLdb.connect (host = "127.0.0.1", user = "paperlens", passwd = "paper1ens", db = "paperlens")
cursor = connection.cursor()
connection.commit()
data = open("../../../data/DBLP-citation.txt")

try:
    title = ''
    citations = 0
    abstract = ''
    n = 0
    for line in data:
        if line.find("#*") == 0:
            title = line[2:len(line)-1].strip('.').lower()
        if line.find("#citation") == 0:
            citations = int(line[9:])
            if citations < 0:
                citations = 0
        if line.find("#!") == 0:
            abstract = line[2:]
        if len(line.strip()) == 0:
            if len(title) > 0:
                hashvalue = paperlens_import.intHash(title.lower())
                cursor.execute("select count(*) from paper where hashvalue=%s",(hashvalue))
                row = cursor.fetchone()
                if(int(row[0]) == 1):
                    cursor.execute("update paper set citations=%s where hashvalue=%s",(citations, hashvalue))
                    cursor.execute("update paper set abstract=%s where hashvalue=%s",(abstract, hashvalue))
            title = ''
            citations = 0
            abstract = ''
            n = n + 1
        
            if n % 10000 == 0:
                print n, title, citations
    connection.commit()
    cursor.close()
    connection.close()
except MySQLdb.Error, e:
    print e.args[0], e.args[1]
