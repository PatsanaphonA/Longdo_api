import os
import os.path
import sys
from osgeo import gdal
from PIL import Image, ImageOps
import datetime
import Process as pa
import psycopg2
from psycopg2 import Error

x = datetime.datetime.now()
print(x)
#Map Location LOOP
#X1 = 564580
#Y1 = 816970
X1 = 564580
Y1 = 816970
X2 = X1 + 1
Y2 = Y1 + 1
zoom = 19

#Loop num increase
#dissolve size
basex = X1
basey = Y1
Getx = X1
Gety = Y1
Getx2 = X2
Gety2 = Y2
sumX = 2 #< change size of dissolve X
sumY = 2 #< change size of dissolve Y
i = X1 + sumX
o = Y1 + sumY
count = 1
count2 = 1
######
baseX2 = basex #baseX2 Big square
baseY2 = basey #baseY2 Big square
Xmax = 2 #< change maximum of X
Ymax = 2 #< change maximum of Y
XLoop = 0
YLoop = 0

#Start loop donwloading image
while XLoop < Xmax:
    while YLoop < Ymax:
        while Getx < i:
            while Gety < o:
				#Map location FOR URL
                pa.ImageDownload(zoom,Gety,Getx)
				#Y,lon  X,lat  zoom
                Y1_tile,X1_tile = pa.num2deg(Gety,Getx,zoom+1)
                Y2_tile,X2_tile = pa.num2deg(Gety2,Getx2,zoom+1)
								
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
            baseX2 = Getx + 1
            Getx += 1
            Getx2 = Getx + 1
            baseY2 = Gety
            Gety = basey
            Gety2 = Gety + 1
        print("Checkdissolve")
        pa.Checkdissolve()
		
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

pa.dissolve()
print("dissolve")
#Dissolve table
pa.Connect()
b = datetime.datetime.now()
print(b-x)
#limite off : 
#ALTER SYSTEM SET jit=off; = OFF
# select pg_reload_conf(); = T
# show jit; = OFF

