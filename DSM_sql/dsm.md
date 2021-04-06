---
layout: page
title: Greenspace Access Analysis in PostGIS using Open Street Map Data
---

In this analysis, we attempt to use SQL queries in PostGIS to answer a simple spatial question about environmental justice in Dar es Salaam, Tanzania. [Drew An-Pham](https://daptx.github.io/) and I collaborated on this lab. Here, we attempt to answer a simple spatial question about access to greenspaces in this growing city: _What percent of residences in each of the public administrative wards are within 0.25 km of a public greenspace?_

**DATA**

The data used in this analysis came from [OpenStreetMap](https://www.openstreetmap.org/#map=15/-6.8564/39.1488), or OSM. OSM is a public mapping effort aimed at creating open spatial data. Open data free and can be used for any purpose as long as the data source and contributors are given credit [OSM](https://www.openstreetmap.org/about). These data are collected by local parties (which can be individuals or enterprises), and the information around collection is contained in the data with a unique identifier and timestamp for each user. This information can be used to determine who was involved in the collection of the data, as the objectives of private users may differ from those of corporations or organizations.

Data in OSM is organized in the form of **tags**, which consist of a _key_ and a _value_. A key is used to define the type or category of the object in question, and the value is used to enumerate or elaborate on the character of the feature. An example of this key="value" format would be natural="wood". The key here is _natural_, which specifies the type of feature as a natural feature, and the value is _wood_, meaning that the type of natural feature is a wood or a forest.

![Percent of Residences with Access to Greenspace by Ward](/assets/wardPct_DSM.png)

Here is a [link to a web map of our final results](/assets/index.html)

DATA SOURCES:
