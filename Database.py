import processing
import psycopg2
from PIL import Image, ImageOps
import arcpy

import os

filein = '/Users/staff/Desktop/Map/MapEP2/4 road.png'
fileout = '/Users/staff/Desktop/Map/MapEP2/Shpfile.shp'


im = Image.open('/Users/staff/Desktop/Map/MapEP2/4 road.png')
im_mirror = ImageOps.mirror(im)
im_mirror.save('/Users/staff/Desktop/Map/MapEP2/Photofile.png')


processing.run("gdal:polygonize",
{'INPUT':'/Users/staff/Desktop/Map/MapEP2/Photofile.png',
'BAND':4,'FIELD':'DN','EIGHT_CONNECTEDNESS':False,
'EXTRA':'-q',
'OUTPUT':fileout})


myconnect = psycopg2.connect(database = 'vector',user = 'postgres',password = '026329700',host = 'localhost',port = '5432')

try:
    #Insert Data
    cursor = myconnect.cursor()
    cursor.execute(''' SELECT * FROM dataset ''')
    myresult = cursor.fetchall()
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")
    
except (Exception, psycopg2.Error) as error :   
    print ("Error while connecting to PostgreSQL", error)
    
finally:
    #closing database connection and save.
        if(myconnect):
            cursor.commit()
            cursor.close()
            myconnect.close()
            print("PostgreSQL connection is closed")
     

#import subprocess     

#import ogr2ogr            
#loadfile = path\\file.xml

#command = "C:\\Program Files\\QGIS Chugiak\\bin\\ogr2ogr.exe --config  PG_LIST_ALL_TABLES YES -f \"PostgreSQL\" -append PG:\"host=hostname user=username password=password dbname=dbname\" " + loadfile

#os.system(command)


#import shp2pgsql

#commandline use 

#shp2pgsql -s SRID SHAPEFILE.shp SCHEMA.TABLE | psql -h HOST -d DATABASE -U USER