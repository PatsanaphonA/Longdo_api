--UNION
DROP TABLE TEST;
CREATE TABLE TEST AS 
SELECT 
  ogc_fid, 
  dn,
  (ST_DUMPRINGS(ST_Union(wkb_geometry))).geom as geometry
FROM getpoint
GROUP BY 
  ogc_fid,
  wkb_geometry
UNION
SELECT 
  ogc_fid, 
  dn,
  (ST_DUMPRINGS(ST_Union(wkb_geometry))).geom as geometry
FROM getpoint2
GROUP BY 
  ogc_fid,
  wkb_geometry;

--UNION2
drop table uni;
create table uni as
SELECT (ST_DUMP(ST_multi(ST_Union(ST_buffer((a.wkb_geometry),0.0000125))))).geom 
FROM getpoint a
WHERE ST_isValid(a.wkb_geometry)
GROUP BY a.wkb_geometry
union
SELECT (ST_DUMP(ST_multi(ST_Union(ST_BUFFER((b.wkb_geometry),0.0000125))))).geom
FROM getpoint2 b
WHERE ST_isValid(b.wkb_geometry)
GROUP BY b.wkb_geometry;


DROP TABLE dissolve;
create table dissolve as
SELECT ogc_fid, dn, (ST_Union(ST_ExteriorRing(ST_BUFFER((the_geom),0.0)))) as the_geom
from test
group by ogc_fid,dn;

DROP TABLE merged;
CREATE TABLE merged AS
SELECT ogc_fid,
  (ST_DUMP(ST_POLYGONIZE(ST_MULTI(the_geom)))).geom AS the_geom
FROM test
group by ogc_fid;
-- Update the geometry_columns table
SELECT Populate_Geometry_Columns();

drop table uni;
create table uni as
SELECT (ST_Dump(ST_UNION(ST_BUFFER((a.wkb_geometry),0.00000125)))).geom  
FROM getpoint a ,getpoint2 b 
WHERE ST_TOUCHES(a.wkb_geometry, b.wkb_geometry)
AND (a.ogc_fid > b.ogc_fid)
union
SELECT (ST_Dump(ST_UNION(ST_BUFFER((b.wkb_geometry),0.00000125)))).geom  
FROM getpoint a ,getpoint2 b 
WHERE ST_TOUCHES(a.wkb_geometry, b.wkb_geometry)
AND (a.ogc_fid < b.ogc_fid)

--Multi
DROP TABLE dissolve;
create table dissolve as
SELECT ogc_fid, dn, st_multi(ST_LineMerge(ST_COLLECT(ST_ExteriorRing(ST_BUFFER((wkb_geometry),0.000001))))) as the_geom
FROM getpoint
group by ogc_fid,dn;
--multilinestring
DROP TABLE dissolve;
create table dissolve as
SELECT ogc_fid, dn, ST_ASTEXT(ST_LineMerge(ST_COLLECT(ST_ExteriorRing(ST_BUFFER((wkb_geometry),0.000001))))) as the_geom
from getpoint2
group by ogc_fid,dn,wkb_geometry;

drop table merged;
create table merged as
SELECT st_intersection(a.wkb_geometry,b.wkb_geometry)
FROM getpoint a , getpoint2 b
where st_intersects(a.wkb_geometry,b.wkb_geometry)

drop table merged;
create table merged as
SELECT st_difference(a.wkb_geometry,b.wkb_geometry)
FROM getpoint a , getpoint2 b
where st_intersects(a.wkb_geometry,b.wkb_geometry)

drop table dissolve;
create table dissolve as
SELECT a.ogc_fid,(ST_DUMP(ST_UNION(ST_BUFFER((a.wkb_geometry),0.00000125),ST_BUFFER((b.wkb_geometry),0.00000125)))).geom
FROM getpoint a , getpoint2 b
where st_intersects(a.wkb_geometry,b.wkb_geometry);

DROP TABLE dissolve;
create table dissolve as
SELECT (ST_BuildArea(ST_UNION(ST_COLLECT(ST_ExteriorRing(a.wkb_geometry),ST_ExteriorRing(b.wkb_geometry))))) as the_geom
from getpoint a, getpoint2 b
where st_intersects(a.wkb_geometry,b.wkb_geometry)
group by a.wkb_geometry;

--FIRST SUCC but wrong Quest
drop table dissolve;
create table dissolve as
SELECT (ST_UNION(ST_COLLECT(a.wkb_geometry,b.wkb_geometry))) as the_geom
FROM getpoint a join getpoint2 b
on st_intersects(a.wkb_geometry,b.wkb_geometry);

drop table uni;
create table uni as 
select (ST_DUMP(ST_polygonize(the_geom))).geom
FROM dissolve;


drop table dissolve;
create table dissolve as
select ogc_fid,dn,(ST_Multi(ST_UNION(ST_ExteriorRing(wkb_geometry)))) as wkb_geometry
from getpoint
group by ogc_fid,dn,wkb_geometry;

drop table merged;
create table merged as
select ogc_fid,dn,MAX(dn),(ST_DUMP(ST_POLYGONIZE(wkb_geometry))).geom as wkb_geometry
from dissolve
where ST_area(wkb_geometry) > 2.8
group by ogc_fid,dn,wkb_geometry;


--drop table test;
create table test as
SELECT ogc_fid,wkb_geometry
from merged
where ST_AREA(wkb_geometry,false) > 0.35;


drop table dissolve;
create table dissolve as
select ogc_fid,dn,(ST_Multi(ST_UNION(ST_Boundary((wkb_geometry))))) as wkb_geometry
from getpoint
group by ogc_fid,dn,wkb_geometry;

drop table merged;
create table merged as
select ogc_fid,dn,(ST_DUMP(ST_POLYGONIZE(wkb_geometry))).geom as wkb_geometry
from dissolve
group by ogc_fid,dn,wkb_geometry;

--drop table maptest;
--create table maptest as
insert into maptest
SELECT ogc_fid,dn,(ST_UNION(ST_COLLECT(st_buffer(st_buffer(wkb_geometry,1,'join=mitre mitre_limit=1.0'),-1,'join=mitre mitre_limit=1.0'),wkb_geometry))) as wkb_geometry
from merged
group by ogc_fid,dn,wkb_geometry;
  
drop table dissolve;
create table dissolve as
select ogc_fid,dn,(ST_Multi(ST_UNION(ST_Boundary((wkb_geometry))))) as wkb_geometry
from getpoint
group by ogc_fid,dn,wkb_geometry;

drop table merged;
create table merged as
select ogc_fid,dn,(ST_DUMP(ST_POLYGONIZE(wkb_geometry))).geom as wkb_geometry
from dissolve
group by ogc_fid,dn,wkb_geometry;

drop table maptest;
create table maptest as
SELECT ST_MULTI(ST_UNION(ST_COLLECT(st_buffer(st_buffer(wkb_geometry,1,'join=mitre mitre_limit=1.0'),-1,'join=mitre mitre_limit=1.0'),wkb_geometry))) as wkb_geometry
from merged;



drop table dissolve;
create table dissolve as
select ogc_fid,dn,(ST_Multi(ST_UNION(ST_Boundary((wkb_geometry))))) as wkb_geometry
from getpoint
group by ogc_fid,dn,wkb_geometry
having dn not in (select max(dn)from getpoint);

drop table merged;
create table merged as
select ogc_fid,dn,(ST_DUMP(ST_POLYGONIZE(wkb_geometry))).geom as wkb_geometry
from dissolve
group by ogc_fid,dn,wkb_geometry;

drop table maptest;
create table maptest as
SELECT (ST_DUMP(ST_MULTI(ST_UNION(ST_COLLECT(st_buffer(st_buffer(wkb_geometry,1,'join=mitre mitre_limit=1.0'),-1,'join=mitre mitre_limit=1.0'),wkb_geometry))))).geom as wkb_geometry
from merged;


drop table dissolve2;
create table dissolve2 as
select ogc_fid,dn,(ST_Multi(ST_UNION(ST_Boundary((wkb_geometry))))) as wkb_geometry
from getpoint2
group by ogc_fid,dn,wkb_geometry
having dn not in (select max(dn)from getpoint2);

drop table merged2;
create table merged2 as
select ogc_fid,dn,(ST_DUMP(ST_POLYGONIZE(wkb_geometry))).geom as wkb_geometry
from dissolve2
group by ogc_fid,dn,wkb_geometry;

insert into maptest
SELECT (ST_DUMP(ST_MULTI(ST_UNION(ST_COLLECT(st_buffer(st_buffer(wkb_geometry,1,'join=mitre mitre_limit=1.0'),-1,'join=mitre mitre_limit=1.0'),wkb_geometry))))).geom as wkb_geometry
from merged2;

drop table test;
create table test as
SELECT (ST_Dump(ST_Union(ST_Buffer(wkb_geometry, 0.000001)))).geom AS the_geom
FROM maptest;


drop table maptest;
create table maptest as
SELECT dn,(ST_DUMP(ST_MULTI(ST_UNION(ST_COLLECT(st_buffer(st_buffer(wkb_geometry,1,'join=mitre mitre_limit=1.0'),-1,'join=mitre mitre_limit=1.0'),wkb_geometry))))).geom as wkb_geometry
from getpoint
group by dn
having dn not in (select max(dn)from getpoint);


insert into maptest
SELECT dn,(ST_DUMP(ST_MULTI(ST_UNION(ST_COLLECT(st_buffer(st_buffer(wkb_geometry,1,'join=mitre mitre_limit=1.0'),-1,'join=mitre mitre_limit=1.0'),wkb_geometry))))).geom as wkb_geometry
from getpoint5
group by dn
having dn not in (select max(dn)from getpoint5);


drop table test;
create table test as
SELECT (ST_Dump(ST_UNION(ST_Buffer(wkb_geometry, 0.000001)))).geom AS the_geom
FROM maptest;


drop table uni;
create table uni as
select ogc_fid,dn,(ST_BUILDAREA(ST_Multi(ST_UNION(ST_Boundary(ST_BUFFER((wkb_geometry),0.0000001)))))) as wkb_geometry
from maketest
group by ogc_fid,dn,wkb_geometry;


drop table dissolve;
create table dissolve as
SELECT (ST_DUMP(ST_MULTI(ST_UNION(ST_COLLECT(a.wkb_geometry,b.wkb_geometry))))).geom as wkb_geometry
FROM get1 a , get2 b
where ST_Touches(a.wkb_geometry,b.wkb_geometry) and st_intersects(a.wkb_geometry,b.wkb_geometry);


select 'intersection', ST_Intersection(g1.wkb_geometry, g2.wkb_geometry)
from get1 g1
JOIN get2 g2 ON ST_Intersects(g1.wkb_geometry, g2.wkb_geometry)
WHERE ST_GeometryType(ST_Intersection(g1.wkb_geometry, g2.wkb_geometry)) = 'ST_LineString'


select wkb_geometry, ST_Area(wkb_geometry::geography)
from get1 
WHERE ST_Area(wkb_geometry::geography) > 1

UNION

select wkb_geometry, ST_Area(wkb_geometry::geography)
from get2
WHERE ST_Area(wkb_geometry::geography) > 1


drop table dissolve;
create table dissolve as
select ST_BUFFER(wkb_geometry,0.000000001) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get1 
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry
UNION
select wkb_geometry as wkb_geometry, ST_Area(wkb_geometry::geography)
from get2
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

drop table test;
create table test as
SELECT (ST_Dump(ST_UNION(ST_BUFFER(wkb_geometry, 0.000000001)))).geom AS the_geom
FROM dissolve;



--SUCCC wait for test
drop table dissolve;
create table dissolve as
select (ST_BUFFER(wkb_geometry,-0.0000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get1 
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry
UNION
select (ST_BUFFER(wkb_geometry,0.0000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get2
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get3
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get4
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get5
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get6
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get7
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get8
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

drop table test;
create table test as
SELECT (ST_Dump(ST_UNION(ST_BUFFER((wkb_geometry),0.00000001)))).geom AS the_geom
FROM dissolve;



drop table dissolve;
create table dissolve as
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get1 
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get2
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get3
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get4
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get5
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get6
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get7
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

insert into dissolve
select (ST_BUFFER(wkb_geometry,-0.00000001)) as wkb_geometry, ST_Area(wkb_geometry::geography)
from get8
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

drop table test;
create table test as
SELECT (ST_Dump(ST_UNION(ST_BUFFER((wkb_geometry),0.00000001)))).geom AS the_geom
FROM dissolve;


--SUCC GOOD PROCESSING
drop table dissolve2;
create table dissolve2 as
select (ST_DUMP(ST_BUFFER(wkb_geometry,-0.00000001))).geom as wkb_geometry, ST_Area(wkb_geometry::geography)
from get
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

drop table test;
create table test as
SELECT (ST_Dump(ST_UNION(ST_BUFFER((wkb_geometry),0.00000001)))).geom AS wkb_geometry
FROM dissolve2;

--SMOOTH SHAPE
drop table dissolve2;
create table dissolve2 as
select (ST_DUMP(ST_BUFFER(wkb_geometry,-0.00000001))).geom as wkb_geometry, ST_Area(wkb_geometry::geography)
from get
WHERE ST_Area(wkb_geometry::geography) > 1
group by wkb_geometry;

drop table test;
create table test as
SELECT (ST_Dump(ST_Simplify(ST_UNION(ST_BUFFER((wkb_geometry),0.00000001)),0.000004))).geom AS wkb_geometry
FROM dissolve2;