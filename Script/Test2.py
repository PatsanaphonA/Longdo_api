import os
import os.path
import sys
from osgeo import gdal
from PIL import Image, ImageOps
import math
import psycopg2
from psycopg2 import Error
import datetime
import multiprocessing as mp

X1 = 564580
Y1 = 816970
X2 = X1 + 1
Y2 = Y1 + 1
zoom = 19

#Loop num increase
basex = X1 #baseX small square
basey = Y1 #baseY small square
Getx = X1
Gety = Y1
Getx2 = X2
Gety2 = Y2
sumX = 3 #small square x
sumY = 3 #small square y
i = X1 + sumX
o = Y1 + sumY
count = 1
count2 = 1
###########

baseX2 = basex #baseX2 Big square
baseY2 = basey #baseY2 Big square
Xmax = 2 #Choose Loop X
Ymax = 2 #Choose Loop Y
XLoop = 0
YLoop = 0

#create table polygon
create_table_query = ('''
		select (ST_UNION(ST_BUFFER((wkb_geometry),0.00000005))) as wkb_geometry
		from map1
		WHERE ST_Area(wkb_geometry::geography) > 3;
		
		drop table map1;
		''')
#insert table polygon
Make_insert = ('''
		with dissolve as (select (ST_UNION(ST_BUFFER((wkb_geometry),0.00000005))) AS wkb_geometry
		from map1
		WHERE ST_Area(wkb_geometry::geography) > 3)
		select a.wkb_geometry
		from dissolve a
		WHERE not EXISTS (
			SELECT b.wkb_geometry 
			FROM mapedit b
			WHERE a.wkb_geometry = b.wkb_geometry or ST_Within(a.wkb_geometry,b.wkb_geometry));
		
		drop table map1;
		''')

Dissolve_create = ('''
	select (ST_DUMP(ST_Simplify(ST_UNION(ST_BUFFER((wkb_geometry),0.00000005)),0.000005))).geom as wkb_geometry
from mapedit;		

	''')

Dissolve_insert = ('''
	select (ST_DUMP(ST_Simplify(ST_UNION(ST_BUFFER((wkb_geometry),0.00000005)),0.000005))).geom as wkb_geometry
from mapedit;	
	
	''')

#connection DB
connection = psycopg2.connect(user = "postgres",
                                  password = "026329700",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "vector")

#CONNECTED
cursor = connection.cursor()

def checkTableExists(dbcon, tablename):
    cursor.execute('''
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        '''.format(tablename.replace('\'', '\'\'')))
    if cursor.fetchone()[0] == 1:
        return True
    return False

#Download Image .png
def ImageDownload(zoom , Gety, Getx):
	url = ("http://ms.longdo.com/mapproxy/tms/1.0.0/dol/EPSG3857/" + str(zoom) + "/" + str(Gety) + "/" + str(Getx) + ".png")
	Dload = ("curl -o test/Map.png " + url)
	os.system(Dload)

#calculate Tile numbers to lon./lat.
def num2deg(xtile, ytile, zoom):
		n = 2.0 ** zoom
		lon_deg = xtile / n * 360.0 - 180.0
		lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
		lat_deg = math.degrees(lat_rad)
		lat_deg = lat_deg * -1
		return (lat_deg, lon_deg)

def Checkdissolve():
	print()
	if (checkTableExists('vector','mapedit')) :
		cursor.execute('''insert into mapedit(wkb_geometry) '''+ Make_insert)
		connection.commit()
		print("Table Insert")
	else :
		cursor.execute('''create table mapedit as '''+ create_table_query)
		connection.commit()
		print("Table Create")

def dissolve():
	if (checkTableExists('vector','mapdissolve')) :
		dissolve = ('''drop table mapdissolve; ''' + Dissolve_insert) 
	dissolve = ('''create table mapdissolve as ''' + Dissolve_create)
	cursor.execute(dissolve)
	connection.commit()




while XLoop < Xmax:
    while YLoop < Ymax:
        while Getx < i:
            while Gety < o:
				#Map location FOR URL
                ImageDownload(zoom,Gety,Getx)
				#Y,lon  X,lat  zoom
                Y1_tile,X1_tile = num2deg(Gety,Getx,zoom+1)
                Y2_tile,X2_tile = num2deg(Gety2,Getx2,zoom+1)
								
				#Add more read Line in .png  							 V       V
                command = ("convert test/Map.png -fuzz 95% -fill red +opaque none testoutput/BG/Map.png")
                os.system(command)
                command1 = ("convert testoutput/BG/Map.png -background none testoutput/Png/Map.png")
                os.system(command1)

				#Flip .png cause polygonize m ake .png flip. So let flip it first ,it will make it correct .png
                im = Image.open(r'testoutput/Png/Map.png')
                im_mirror = ImageOps.flip(im)
                im_mirror.save(r'testoutput/Flip/Map.png')

				#Give .png location and translate to .tif and CRS location
                command2 = ("gdal_translate -co 'WORLDFILE=YES' -a_srs EPSG:4326 -a_ullr " + str(X1_tile) + " " + str(Y1_tile) + " " + str(X2_tile) + " " + str(Y2_tile) + " testoutput/Flip/Map.png testoutput/Tiff/Map.png")		
                os.system(command2)

				#Polygonize sent to DB                               V
                command3 = ("gdal_polygonize.py testoutput/Tiff/Map.png -f PostgreSQL PG:'dbname='vector' user='postgres' host='localhost' port = '5432' password = '026329700'' map1")
                os.system(command3)
                Gety += 1
                Gety2 = Gety + 1
                print(count)
                count += 1
                    #Finish X
            baseX2 = Getx
            Getx += 1
            Getx2 = Getx + 1
            baseY2 = Gety
            Gety = basey
            Gety2 = Gety + 1
        Checkdissolve()
        o += sumY
        i += sumX
        Getx = basex
        Getx2 = Getx + 1
        Gety = baseY2
        Gety2 = Gety + 1
        print("baseY2 = " + str(baseY2))
        print("baseX2 = " + str(baseX2))
        print("O = " + str(o))
        print("i = " + str(i))
        YLoop += 1
        print( "Y = " + str(YLoop))
        
    Getx = baseX2
    Getx2 = Getx + 1
    Gety = basey
    Gety2 = Gety + 1
    XLoop += 1
    print("X = " + str(XLoop))
dissolve()
    