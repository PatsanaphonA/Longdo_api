import os
import os.path
import subprocess
from osgeo import gdal
import processing

#Make .shp file connect(merge) 
processing.run("native:union", 
    {'INPUT':'Ouput/Shp/get3.shp',
    'OVERLAY':'Output/Shp/get4.shp',
    'OVERLAY_FIELDS_PREFIX':'',
    'OUTPUT':'Output/Union/GetMapUnion.shp'})

    #Get only polygon
processing.run("native:dissolve", {'INPUT':'Output/Union/GetMapUnion.shp',
    'FIELD':[], 
    'OUTPUT':'Output/Dissolve/GetDissolve.shp'})


    #Separate polygon
processing.run('native:multiparttosingleparts', {
    'INPUT':'Output/Dissolve/GetDissolve.shp', 
    'OUTPUT':'Output/Multi/GetPolygon.shp',})
    
    
#Database
command3 = ('gdal_polygonize.py Output/Multi/GetPolygon.shp -f PostgreSQL PG:"dbname={dbname} user={user} host={host} port={port} password={password}" Point'.format(dbname='vector' ,user='postgres' ,host='localhost' ,port=5432 ,password='026329700'))
os.system(command3)

#PostgreSQL PG:"dbname='vector' user='postgres' host='localhost' port='5432' password='026329700'" Mastering_Polygon''


