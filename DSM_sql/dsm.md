---
layout: page
title: Greenspace Access Analysis in PostGIS using Open Street Map Data
---

In this analysis, we attempt to use SQL queries in PostGIS to answer a simple spatial question about environmental justice in Dar es Salaam, Tanzania. [Drew An-Pham](https://daptx.github.io/) and I collaborated on this lab. Here, we attempt to answer a simple spatial question about access to greenspaces in this growing city: _What percent of residences in each of the public administrative wards are within 0.25 km of a public greenspace?_

**DATA**

The data used in this analysis came from [OpenStreetMap](https://www.openstreetmap.org/#map=15/-6.8564/39.1488), or OSM. OSM is a public mapping effort aimed at creating open spatial data. Open data free and can be used for any purpose as long as the data source and contributors are given credit ([OSM](https://www.openstreetmap.org/about)). These data are collected by local parties (which can be individuals, organizations, enterprises, etc.), and the information around collection is contained in the data with a unique identifier and timestamp for each user. This information can be used to determine who was involved in the collection of the data, as the objectives of private users may differ from those of corporations or organizations. In our case, it appears that the majority of the main contributors to this dataset in this area are members of [RamaniHuria](https://ramanihuria.org/en/), a Tanzanian mapping project aimed at collecting data regarding flood risk in Dar es Salaam.

Data in OSM is organized in the form of **tags**, which consist of a _key_ and a _value_, in the form of key="value". A key is used to define the type or category of the object in question, and the value is used to enumerate or elaborate on the character of the feature. An example of this key="value" format would be natural="wood". The key here is _natural_, which specifies the type of feature as a natural feature, and the value is _wood_, meaning that the type of natural feature is a wood or a forest.

**METHODS**

```
/* Create a table of points that are residential buildings*/
/* Here, we are defining residential buildings as any point/polygon that is not listed as an amenity and listed as a building*/
-- by default, PostGIS doesn't seem to know what type of geometry it's getting,
--so we type-cast it with ::geometry(multipolygon,32737)  where the parameters are the geometry type and SRID

CREATE TABLE respoint AS
SELECT osm_id, building, amenity, st_transform(way,32737)::geometry(point,32737) as geom, osm_user, osm_uid, osm_version, osm_timestamp
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

![Percent of Residences with Access to Greenspace by Ward](/assets/wardPct_DSM.png)

Here is a [link to a web map of our final results](/assets/index.html)

DATA SOURCES:
