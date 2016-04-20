# -*- coding: UTF-8     -*-
# -*- author: kohna     -*-
# -*- date  : 2015-11-22-*-
# -*- time  : 20:39     -*-
"""
    Get the MS hole list
    Test result:
        Need time: 3072s
        The db file: 155 MB
        Total items: 991
        Range: ms04-008 -- ms15-123

"""

import requests
import lxml.html as html
import datetime
import sqlite3

# --- some setting start
starttime = datetime.datetime.now()
sqlDB = "tech.db3"   # DB file name

# --- settings end


def geturl(self, urllists):
    temp = requests.session()
    mainhtml = temp.get(self)
    mainhtml = html.fromstring(mainhtml.text)
    tempists = mainhtml.xpath("//div[@id='content']/div/a/@href|//div[@id='content']/div/a/text()")
    for ix in tempists:
        urllists.append(ix)


def getmain(self):  # the self is url
    temp = requests.session()
    mthl = temp.get(self)
    mthl = html.document_fromstring(mthl.text)
    titl = mthl.xpath("//h1/text()")[0]
    fair = mthl.xpath("//div[@id='mainSection']")[0]
    tari = fair.text_content()  # get all text
    tdic = {
        "url": self,
        "title": titl.strip(),
        "airsou": html.tostring(fair, encoding='unicode').strip().replace("'", "''"),  # del space and replace the ' to '',if not the sql cat not be insert
        "airful": tari.strip().replace("'", "''")  # Ditto
    }
    return tdic


class DBopt:  # DB operation
    def __init__(self):
        try:
            self.dbcon = sqlite3.connect(sqlDB)
        except sqlite3.Error, e:
            print u'Sqlit Databese error by ' + e.args[0]
            return

        self.dbcur = self.dbcon.cursor()
        self.sql = 'sql'

    def sqlexe(self):
        try:
            temp = self.dbcur.execute(self.sql)
        except sqlite3.Error, e:
            print u"Sqlit3 Databese execute sql error by " + e.args[0]
            return
        self.dbcon.commit()

        return temp

    def dbcolse(self):
        self.dbcon.close()


if __name__ == "__main__":
    urls = []  # ['url','name']
    sdic = {}
    tempnum = 0
    db = DBopt()
    db.sql = '''CREATE TABLE IF NOT EXISTS technat(id INTEGER PRIMARY KEY,numb VARCHAR(12),url VARCHAR(128),titles VARCHAR(128),airsou text,airfull text)'''
    db.sqlexe()
    seis = requests.Session()
    seisHtml = seis.get("https://technet.microsoft.com/zh-CN/library/security/dn631937.aspx")
    seisHtml = html.document_fromstring(seisHtml.text)
    mainurls = seisHtml.xpath("//div[@class='toclevel2 ']/a/@href")
    for i in mainurls:
        geturl(i, urls)
    for ixa in urls:
        if len(ixa) > 8:  # the url lenght more than 8,so the ixa is url
            sdic = getmain(ixa)
        else:   # else the ixa is hole name ,ex. ms15-123
            print ixa
            db.sql = "INSERT INTO technat(numb,url,titles,airsou,airfull) VALUES('" + ixa + "','" + sdic['url'] + "','" + sdic["title"] + "','" + sdic['airsou'] + "','" + sdic['airful'] + "')"
            db.sqlexe()
            sdic.clear()   # clear the dict for next time.
    db.dbcolse()
    endtime = datetime.datetime.now()
    print (endtime - starttime).seconds
