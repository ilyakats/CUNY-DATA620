# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import json
import os
import mysql.connector
import string

insQuery1 = ("INSERT INTO billsInfo "
                "(bioguide_id,district,sponsorName,state,thomas_id,sponsorTitle,sponsorType,billTitle, filename, bill_id, billStatus, bill_type) "
                "VALUES (%(bioguide_id)s, %(district)s, %(sponsorName)s, %(state)s, %(thomas_id)s, %(sponsorTitle)s, %(sponsorType)s, "
                "%(billTitle)s, %(filename)s, %(bill_id)s, %(billStatus)s, %(bill_type)s)")

insQuery2 = ("INSERT INTO cosponsors "
                "(bioguide_id,district,cosponsorName,state,thomas_id,cosponsorTitle,cosponsorType, bill_id, original_cosponsor) "
                "VALUES (%(bioguide_id)s, %(district)s, %(cosponsorName)s, %(state)s, %(thomas_id)s, %(cosponsorTitle)s, %(cosponsorType)s, %(bill_id)s, %(original_cosponsor)s)")

dataFolder = 'D:/CUNY/620/Week02/Project1/bills/s'

cnx = mysql.connector.connect(user='root', host='127.0.0.1', database='billsData')
cursor = cnx.cursor()

for path, subdirs, files in os.walk(dataFolder):
    for name in files:
        print os.path.join(path, name)
        filename = os.path.join(path, name)
        with open(filename) as json_file:
            json_data = json.load(json_file)
            sponsor_data = json_data['sponsor']
            bill_id = json_data['bill_id']
            status = json_data['status']
            bill_type = json_data['bill_type']
            billTitle = json_data['short_title']

            if not billTitle:
                billTitle = json_data['official_title']

            bdDf = pd.DataFrame.from_dict(sponsor_data, orient='index')
            bdDf.columns = ['value']
            bdKeys = bdDf.index.unique()
            bd = {}
            bd['bioguide_id'] = " "
            bd['district'] = " "
            bd['sponsorName'] = " "
            bd['state'] = " "
            bd['thomas_id'] = " "
            bd['sponsorTitle'] = " "
            bd['sponsorType'] = " "
            bd['billTitle'] = billTitle
            bd['filename'] = string.replace(filename, '\\', '/')
            bd['bill_id'] = bill_id          
            bd['billStatus'] = status 
            bd['bill_type'] = bill_type
            
            for reqKey in bdKeys:
                if reqKey == 'type':
                    bd['sponsorType'] = bdDf.ix[reqKey,'value']
                elif reqKey == 'name':
                    bd['sponsorName'] = string.replace(bdDf.ix[reqKey,'value'], ',', '')
                elif reqKey == 'title':
                    bd['sponsorTitle'] = bdDf.ix[reqKey,'value']
                elif reqKey == 'title':
                    bd['sponsorTitle'] = bdDf.ix[reqKey,'value']
                else:
                    bd[reqKey] = bdDf.ix[reqKey,'value']

            cursor.execute(insQuery1, bd)
            
            cosponsor_data = json_data['cosponsors']
            if len(cosponsor_data) > 0:
                for i in range(len(cosponsor_data)):
                    cbdDf = pd.DataFrame.from_dict(cosponsor_data[i], orient='index')
                    cbdDf.columns = ['value']
                    cbdKeys = cbdDf.index.unique()
                    cbd = {}
                    cbd['bill_id'] = bill_id
                    cbd['bioguide_id'] = " "
                    cbd['district'] = " "
                    cbd['cosponsorName'] = " "
                    cbd['state'] = " "
                    cbd['thomas_id'] = " "
                    cbd['cosponsorTitle'] = " "
                    cbd['cosponsorType'] = " "
                    cbd['original_cosponsor'] = " "
                
                    for reqKey in cbdKeys:
                        if reqKey == 'type':
                            cbd['cosponsorType'] = cbdDf.ix[reqKey,'value']
                        elif reqKey == 'name':
                            cbd['cosponsorName'] = string.replace(cbdDf.ix[reqKey,'value'], ',', '')
                        elif reqKey == 'title':
                            cbd['cosponsorTitle'] = cbdDf.ix[reqKey,'value']
                        elif reqKey == 'title':
                            cbd['cosponsorTitle'] = cbdDf.ix[reqKey,'value']
                        else:
                            cbd[reqKey] = cbdDf.ix[reqKey,'value']
    
                    cursor.execute(insQuery2, cbd)
            
            cnx.commit()

cursor.close()
cnx.close()

