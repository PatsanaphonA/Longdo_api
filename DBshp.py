import os.path  
import psycopg2
import osgeo.ogr  
connection = psycopg2.connect(database = 'vector',user = 'postgres',password = '026329700',host = 'localhost',port = '5432')  
cursor = connection.cursor()  
cursor.execute("DELETE FROM datasent")  
srcFile = ('/Users/staff/Desktop/Map/MapEP2/Shpfile.shp')
shapefile = osgeo.ogr.Open(srcFile)    
layer = shapefile.GetLayer(0)    
for i in range(layer.GetFeatureCount()):  
    feature = layer.GetFeature(i)  
    name = feature.GetField("NAME").decode("Latin-1")  
    wkt = feature.GetGeometryRef().ExportToWkt()  
    cursor.execute("INSERT INTO datasent (name,outline) " + "VALUES (%s, ST_GeometryFromText(%s, " +"4326))", (name.encode("utf8"), wkt))  

connection.commit()  