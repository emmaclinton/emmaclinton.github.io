---
layout: page
title: Greenspace Access Analysis in PostGIS using Open Street Map Data
---

In this analysis, we attempt to use SQL queries in PostGIS to answer a simple spatial question about environmental justice in Dar es Salaam, Tanzania. [Drew An-Pham](https://daptx.github.io/) and I collaborated on this lab. Here, we attempt to answer a simple spatial question about access to greenspaces in this growing city: _What percent of residences in each of the public administrative wards are within 0.25 km of a public greenspace?_

**DATA**

The data used in this analysis came from [OpenStreetMap](https://www.openstreetmap.org/#map=15/-6.8564/39.1488), or OSM. OSM is a public mapping effort aimed at creating open spatial data. Open data free and can be used for any purpose as long as the data source and contributors are given credit ([OSM](https://www.openstreetmap.org/about)). These data are collected by local parties (which can be individuals, organizations, enterprises, etc.), and the information around collection is contained in the data with a unique identifier and timestamp for each user. This information can be used to determine who was involved in the collection of the data, as the objectives of private users may differ from those of corporations or organizations. In our case, it appears that the majority of the main contributors to this dataset in this area are members of [RamaniHuria](https://ramanihuria.org/en/), a Tanzanian mapping project aimed at collecting data regarding flood risk in Dar es Salaam.

Data in OSM is organized in the form of **tags**, which consist of a _key_ and a _value_, in the form of key="value". A key is used to define the type or category of the object in question, and the value is used to enumerate or elaborate on the character of the feature. An example of this key="value" format would be natural="wood". The key here is _natural_, which specifies the type of feature as a natural feature, and the value is _wood_, meaning that the type of natural feature is a wood or a forest.

**METHODS**

The first step in this analysis is to pick out the residential buildings within the city. Here, we are defining residential buildings as any point/polygon
that is not listed as an amenity and is listed as a building.

```
/* Create a table of points that are residential buildings*/

-- By default, PostGIS doesn't seem to know what type of geometry it's getting,
-- so we type-cast it with ::geometry(multipolygon,32737)  where the parameters
-- are the geometry type and SRID

CREATE TABLE respoint AS
SELECT osm_id, building, amenity, st_transform(way,32737)::geometry(point,32737) AS geom,
  osm_user, osm_uid, osm_version, osm_timestamp
FROM public.planet_osm_point
WHERE amenity IS NULL
AND building IS NOT NULL;

ALTER TABLE respoint
ADD COLUMN res real;

UPDATE respoint
SET res = 1
WHERE building = 'yes' OR building = 'residential';

DELETE FROM respoint
WHERE res IS NULL;

ALTER TABLE respoint
DROP COLUMN amenity;
}
```

We then repeat this process of picking out residences with the polygon features to ensure our analysis captures all residences.

```

CREATE TABLE respoly AS
SELECT osm_id, building, amenity, st_transform(way,32737)::geometry(polygon,32737) AS geom,
  osm_user, osm_uid, osm_version, osm_timestamp
FROM public.planet_osm_polygon
WHERE amenity IS NULL
AND building IS NOT NULL;

ALTER TABLE respoly
ADD COLUMN res real;

UPDATE respoly
SET res = 1
WHERE building = 'yes' OR building = 'residential';

DELETE FROM respoly
WHERE res IS NULL;
```

When using SQL, it's best to simplify, simplify. Here, we convert these complex polygons to their centroids for ease of analysis, then merge these features with the points layer to create a single layer of residences.

```
/* Now, convert the polygons to centroids to simplify the geometries. */

CREATE TABLE respoly_centroids AS
SELECT osm_id, building, osm_user, osm_uid, osm_version, osm_timestamp,
  st_centroid(geom)::geometry(point,32737) AS geom
FROM respoly;

/* Union the points together to create one point-based table of residences*/

CREATE TABLE uni_residences AS
SELECT DISTINCT osm_id, building, st_transform(geom,32737)::geometry(point,32737) AS geom,
  osm_user, osm_uid, osm_version, osm_timestamp
FROM respoint
UNION
SELECT DISTINCT osm_id, building, st_transform(geom,32737)::geometry(point,32737) AS geom,
  osm_user, osm_uid, osm_version, osm_timestamp
FROM respoly_centroids;

```
Our analysis will eventually be visually represented using the wards. We therefore need to join identifying information about the wards to the residences point layer, using the spatial relationship between residential points and wards to assign a "ward_name" value to residential points

```
/* Join the wards data to the uni_residences table. */

ALTER TABLE uni_residences
ADD COLUMN ward_name text;

UPDATE uni_residences
SET ward_name= ward_census.ward_name
FROM ward_census
WHERE st_intersects(uni_residences.geom, st_transform(ward_census.utmgeom,32737));

```



![Percent of Residences with Access to Greenspace by Ward](/assets/wardPct_DSM.png)

Here is a [link to a web map of our final results](/assets/index.html). 

DATA SOURCES:
