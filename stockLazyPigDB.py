#!/usr/bin/python
### -*- coding: utf-8 -*-
""""""
import os
import sys
import time
import pandas as pd
import sqlite3

from stlib import db_conn, db_st_get_list, db_st_get
from datetime import datetime
from z_stGetData import stGetDataFile, stGetList
from dateutil import relativedelta

#při vytváření načteme seznam akcií z tabulky dzakor.st
conn = db_conn()
ak_len, ak = db_st_get_list(conn)
st_len, st = db_st_get(conn)

stSeznam, stSeznam_delka = stGetList()


calcDateTime=(time.strftime("%d.%m.%Y %H:%M:%S"))
conn = sqlite3.connect("./db/akcie.db")
cur = conn.cursor()
#values = (akcie,100,1)
#cur.execute('select * from st')
#cur.execute("insert into st values (?, ?, ?, 10300.26, null)", values)

# vytvoříme novou tabulku SQLlite z dataframe stSeznam 
stSeznam.set_index('seznam_yahoo_d', inplace=True)
stSeznam.sort_index(ascending=True, inplace=True)
stSeznam.to_sql("stSeznam", conn, if_exists="replace")
st=pd.read_sql("select * from stSeznam;", conn, index_col=('seznam_yahoo_d'))
conn.commit()
conn.close()
print(stSeznam.head(2))
t = pd.read_excel('to.xlsx', index_col=0) #to.xlsx se generuje programem
t.sort_index(ascending=True, inplace=True)
print t.head(3)

fo = open("stockLazyPig.html", "wb")
#sekce HLAVIČKA DATOVÉ STÁNKY
#header
fo.write("<html>")
fo.write("<head>")
fo.write('<title>Lazy Pig stock stock trade revievie, by Igor Džama</title>\n')

fo.write('<meta http-equiv="cache-control" content="max-age=0" />\n')
fo.write('<meta http-equiv="cache-control" content="no-cache" />\n')
fo.write('<meta http-equiv="expires" content="0" />\n')
fo.write('<meta http-equiv="expires" content="Tue, 01 Jan 1980 1:00:00 GMT" />\n')
fo.write('<meta http-equiv="pragma" content="no-cache" />\n')

fo.write('<meta charset="UTF-8">\n')
fo.write('<!-- CSS goes in the document HEAD or added to your external stylesheet -->\n')
fo.write('<link rel="stylesheet" type="text/css" href="styles.css">\n')
fo.write("</head>")
fo.write("<body>\n")
fo.write ('<H3>(c) IGOR DŽAMA: Lazy Pig trade strategy</H3>')
fo.write ('{}'.format(calcDateTime) )
fo.write ('<div>Lazy Pig strategy = buy and do nothing</div>')
fo.write ('<div>Lazy Pig strategy is calculated using Adjusted Close price (dividends and splits should be considered).</div>')
fo.write ('<div>See <i>Legend & Terms</i> on <a href="https://storage.googleapis.com/dzdata1/dztr00.html" target=_top>Home</a></div>')

fo.write ('<table class="altrowstable" id="sample">\n')
fo.write ('<tr>')
fo.write ('<th>STOCK</th>')
fo.write ('<th>STRATEGY II</th><th>yr II %</th><th>DTAR II</th><th>STRATEGY</th><th>S. PROFIT Y</th><th>S. PROFIT Yp</th><th>LP PROFIT Y</th><th>LP months</th>')
fo.write ('</tr>\n')
i = 0
for ak in stSeznam.index: #!!!for ak in v.index[2:]:
  PBPrumYp=stSeznam.ix[i].PBPrumY/st.ix[i].SCAPITAL*100.
  try:    stII = t.get_value(ak, 'STRATEGIE')
  except: stII = ' - '
  
  try:    
     yrII = t.get_value(ak, 'yr');
     if yrII != yrII: yrII = ' - '
     else:
        yrII = round(yrII,2)
  except: yrII = ' - '

  try:    
     DTAR = t.get_value(ak, 'DTAR')
     DTAR = DTAR.strftime("%Y-%m-%d")
  except: DTAR = ' - '
  print ('DTAR:', DTAR)
    
    
  #if (st.ix[i]['DEV'] == True) | (st.ix[i]['DEV'] == 1):
  #  fo.write('<tr> <th bgcolor="#FF0020">{}</th> <td bgcolor="#FF0020">{}</td> <td bgcolor="#FF0020">{}</td> <td bgcolor="#FF0020" align="right">{:.2f}%</td> <td bgcolor="#FF0020" align="right">{:.2f}%</td> <td id="LPmesicu" align="right"> {}</td> </tr>\n'.format(st.index[i],  st.ix[i]['VS'], st.ix[i]['PBPrumY'], PBPrumYp, st.ix[i]['LPPryv']*100., st.ix[i]['LPmesicu']  ) )
  #else:
  fo.write ('<tr>')
  fo.write ('<th>{}</th>'.format(st.index[i]))
  fo.write ('<td bgcolor="lightblue">{}</td>'.format(stII) )
  fo.write ('<td bgcolor="lightblue" align="right">{}</td>'.format(yrII) )
  fo.write ('<td bgcolor="lightblue">{}</td>'.format(DTAR) )
            
  fo.write('<td align="center">{}</td> <td> <div align="right"> {:.1f} </div> </td> <td align="right">{:.2f}%</td> </td> <td align="right">{:.2f}%</td> <td id="LPmesicu"><div align="right">{}</div></td> </tr>\n'.format(st.ix[i]['VS'], st.ix[i]['PBPrumY'], PBPrumYp, st.ix[i]['LPPryv']*100., st.ix[i]['LPmesicu']  ) )
  i = i+1
fo.write("</table>\n")
fo.write("</body>\n")
fo.write("</html>\n")
fo.close() #Uložená kopie nemá k dispozici styles.css.
s=os.system("cp stockLazyPig.html /mnt/idisk/lstock/html/") #Zkopírujeme do vývojového adresáře na idisku.


