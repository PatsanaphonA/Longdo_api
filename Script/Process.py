import psycopg2
from psycopg2 import Error
import math
import os
import os.path
import sys

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

Dissolve_script= ('''
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

#check table exists or not
def checkTableExists(dbcon, tablename):
    cursor.execute('''
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        '''.format(tablename.replace('\'', '\'\'')))
    if cursor.fetchone()[0] == 1:
        return True
    return False

#Clean image
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
		dissolve = ('''drop table mapdissolve; ''')
		cursor.execute(dissolve)
		connection.commit()
	dissolve = ('''create table mapdissolve as ''' + Dissolve_script)
	cursor.execute(dissolve)
	connection.commit()

#calculate Tile numbers to lon./lat.
def num2deg(xtile, ytile, zoom):
		n = 2.0 ** zoom
		lon_deg = xtile / n * 360.0 - 180.0
		lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
		lat_deg = math.degrees(lat_rad)
		lat_deg = lat_deg * -1
		return (lat_deg, lon_deg)

#Download Image .png
def ImageDownload(zoom , Gety, Getx):
	url = ("http://ms.longdo.com/mapproxy/tms/1.0.0/dol/EPSG3857/" + str(zoom) + "/" + str(Gety) + "/" + str(Getx) + ".png")
	Dload = ("curl -o test/Map.png " + url)
	os.system(Dload)

def Connect():
	if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
