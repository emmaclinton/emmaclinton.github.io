---
layout: page
title: RE- Spatial-temporal and content analysis of Twitter Data
---


**Reproduction of**
# "Rapidly measuring spatial accessibility of COVID-19 healthcare resources: a case study of Illinois, USA."

Original study *by* Kang, J. Y., A. Michels, F. Lyu, Shaohua Wang, N. Agbodo, V. L. Freeman, and Shaowen Wang. 2020. Rapidly measuring spatial accessibility of COVID-19 healthcare resources: a case study of Illinois, USA. International Journal of Health Geographics 19 (1):1–17. [DOI:10.1186/s12942-020-00229-x.](DOI:10.1186/s12942-020-00229-x)

Replication Author:
Emma Clinton

Replication Materials Available at: [emmaclinton.github.io](https://github.com/emmaclinton/RP-Kang)

Created: `19 May 2021`
Revised: `24 May 2021`

## Original Study Information

This analysis is a reproduction of [Kang et al. (2020)](https://doi.org/10.1186/s12942-020-00229-x). This study looks at the cyberinfrastructure and analysis behind the [Where COVID 19 Dashboard](https://wherecovid19.cigi.illinois.edu/spatialAccess.html) for the state of Illinois. This dashboard is meant to be a tool to rapidly measure the accessibility of healthcare resources (ICU beds and ventilators) in order to understand how prepared healthcare systems are to save lives during crises like the COVID-19 pandemic and to inform where future services should potentially be allocated.

This paper found that ICU beds and ventilators are not evenly distributed throughout the state of Illinois, and that people living in central and northern Chicago were better able to access healthcare services than the population living in southern Chicago. There was no significant difference between at-risk populations' access to beds and ventilators and COVID-19 patients' access to those same services.

Reproduction of this analysis is important for verification of the results of the original study, which have very important implications in terms of health care provision in the context of emergency situations like the evolving COVID-19 pandemic. Replication of this study could prove highly useful for creating similar tools for other states or even at a federal level.

## Materials and Procedure
The script needed to replicate the data search is included [here](https://github.com/emmaclinton/RP-Kang/blob/main/COVID-19Acc.ipynb).

**CITE DATA SOURCES**

The original study by [Kang et al. (2020)](https://doi.org/10.1186/s12942-020-00229-x) used hospital data from IDPH, COVID-19 confirmed case data from IDPH, residential data from the United States Census Bureau, and road network data from Open Street Map to analyze the spatial accessibility of healthcare resources for residents of the state of Illinois in the context of the COVID-19 pandemic. This analysis used a parallel enhanced two-step floating catchment area to find all people within the catchment areas of the healthcare services. The catchments in this analysis were created from travel time along the road network.

The second step in the analysis was to calculate a service-to-population ratio within each catchment. The "service" in this model is defined as ICU beds and/or ventilators. Two ratios were calculated: a bed-to-at-risk-population ratio and a bed-to-COVID-19 patients ratio. At-risk population was defined as population over age 50. To account for distance decay, multiple zones were created to represent different travel times: 0-10 min, 10-20 min, and 20-30 min, and three weights were applied in these zones (1, 0.68, and 0.22), respectively. These zones are created from a convex hull based on network travel nodes. It must be noted that these weights are not justified in the text of the paper nor in the provided code, so it is unclear on what they are based. Accessibility was then calculated as the sum of the service-to-population ratio. This summing means that areas that fall within areas of overlap between catchments were given a higher accessibility rating.

Finally, the final accessibility results are aggregated into hexagonal grids. (Hexagons were used to minimize orientation bias from edge effects.)

## Deviations from the Protocol

The original study calculated accessibility of healthcare services for both the state of Illinois and for the city of Chicago. A modified version of the original analysis code, provided by [Joseph Holler](https://github.com/josephholler), which only calculates accessibility for the city of Chicago, was used in this reproduction.

The road network provided for us to complete this replication was confined to the limits of Chicago. The road network we used therefore did not  account for use of hospitals outside of the city, regardless of their distance from Chicago. However, the original collection of hospital points was used, meaning that hospitals outside of the city limits were snapped to the nearest node in the road network, causing hospitals outside of the city to be assigned to the node of the city’s road network to which they were most closely located. This reproduction attempts to account for these errors by modifying the road network used in the study to include a 30-km buffer around the city to include roads that fall within that distance. Additionally, errors in the OSM data speed attribute made it impossible for the original code to be run. Speed limits for nodes with these hardcoded errors are therefore assigned the study's default speed of 35 mph (the same speed as is assigned to roads with no speed data). This code correction can be attributed to [Maja Cannavo](https://majacannavo.github.io/geog323/geog323main).

Another alteration to the code was made regarding the weights assigned to different distance buffers for the hospitals. [Kang et al. (2020)](https://doi.org/10.1186/s12942-020-00229-x) did not explain nor justify the weight values used in their analysis. Therefore, the analysis was also run with new weight values of [1.0, 0.5, and 1.0]. These weight values come from [Delameter, Shortridge, and Kilcoyne (2019)](https://doi.org/10.1186/s12913-019-3969-5), who found that for a two-step floating catchment analysis, the most accurate weight values for healthcare service distance decay came from a logistic cumulative distance function, with distance decay based on distance to the nearest facility for a population.


## Replication Results

The spatial analysis of hospital accessibility in Chicago yielded the results shown in **Fig. 1.**

![Fig. 1](/kang/assets/basic_result.png)

_Fig. 1. Temporal analysis._

The revised spatial analysis of hospital accessibility including the 30km buffer of the road network in Chicago yielded the results shown in **Fig. 2.**

![Fig. 2](/kang/assets/final.png)

_Fig. 1. Temporal analysis._

The revised spatial analysis of hospital accessibility including the 30km buffer of the road network and using the new weight values from [Delameter, Shortridge, and Kilcoyne (2019)](https://doi.org/10.1186/s12913-019-3969-5) yielded the results shown in **Fig. 3.**

![Fig. 3](/kang/assets/new_weights.png)


## Discussion

![Fig. 5](/twit/results/figures/may5tornado.png)

_Fig. 5. NOAA Tornado Warning (May 05)._

![Fig. 6](/twit/results/figures/tornadopts.png)

_Fig. 5. NOAA Tornado and Storm Location Points (May 05)._

When comparing **Fig 3** and **Fig. 4** with **Fig. 5** and **Fig. 6**, it does appear that a great deal of Twitter activity paralleled the tornado tracks. These storms were severe and caused widespread dmamage, and many southern states were warned to be on alert for tornadoes on May 3-5, 2021. In some areas, storm activity resulted in significant property damage, several deaths, and extensive power outages (Victor and Jimenez, 2021). These storms generally moved eastwards, and it appears that the areas of the country that have the highest significant clustering of activity are located within the moderate- to high-risk areas of the American south. (**Fig. 4**, **Fig. 5**, **Fig. 6**).

Power outages are important to consider in the context of Twitter analyses, because outages may mean that individuals who are impacted are unable to share information about their status or the situation evolving around them, leading to an incomplete picture of a disaster scenario (Crawford and Finn, 2014). It is also important to consider the human implications of such events when mapping natural disasters. There is a tendency to dissociate data like these from the humans that produced them, especially when data are made anonymous and aggregate. However, it is essential to recognize the devastating impacts of such events and realize that the repercussions of events like tornadoes and severe storms extend far beyond the temporal bounds of the storm event itself.

These findings seem to confirm the findings of Wang et al. (2016) in that the areas that experienced tornado warning or damage were found to have high cluster density of tornado-related Twitter activity. These results also track well with the findings of Holler (2021) in that the Twitter activity largely tracks the eastward movement of this storm event and its impacts, similar to the activity correlating with the movement of Hurricane Dorian.


## Conclusion

Similar to Wang et al. (2016) and Holler (2021), this replication analysis shows that Twitter activity during natural disasters spatially and temporally tracks the development and anticipation of the physical event itself. However, it is still necessary to acknowledge that there is a lack of spatial information in much Twitter data, leading to an incomplete picture of social media activity during such events. It would be interesting to analyze areas impacted by power outages to see how Twitter activity tracks in places that may not have had access to service during these storm events.

## References

Crawford, K., and M. Finn. 2014. The limits of crisis data: analytical and ethical challenges of using social and mobile data to understand disasters. GeoJournal 80 (4):491–502. DOI:10.1007/s10708-014-9597-z

Victor, D., & Jimenez, J. (2021, May 04). Severe weather continues in south for third straight day. The New York Times. [https://www.nytimes.com/2021/05/04/us/tornado-storm-south.html](https://www.nytimes.com/2021/05/04/us/tornado-storm-south.html)

Wang, Z., X. Ye, and M. H. Tsou. 2016. Spatial, temporal, and content analysis of Twitter for wildfire hazards. Natural Hazards 83 (1):523–540. DOI:10.1007/s11069-016-2329-6

####  Report Template References & License

This template was developed by Peter Kedron and Joseph Holler with funding support from HEGS-2049837. This template is an adaptation of the ReScience Article Template Developed by N.P Rougier, released under a GPL version 3 license and available here: https://github.com/ReScience/template. Copyright © Nicolas Rougier and coauthors. It also draws inspiration from the pre-registration protocol of the Open Science Framework and the replication studies of Camerer et al. (2016, 2018). See https://osf.io/pfdyw/ and https://osf.io/bzm54/

Camerer, C. F., A. Dreber, E. Forsell, T.-H. Ho, J. Huber, M. Johannesson, M. Kirchler, J. Almenberg, A. Altmejd, T. Chan, E. Heikensten, F. Holzmeister, T. Imai, S. Isaksson, G. Nave, T. Pfeiffer, M. Razen, and H. Wu. 2016. Evaluating replicability of laboratory experiments in economics. Science 351 (6280):1433–1436. https://www.sciencemag.org/lookup/doi/10.1126/science.aaf0918.

Camerer, C. F., A. Dreber, F. Holzmeister, T.-H. Ho, J. Huber, M. Johannesson, M. Kirchler, G. Nave, B. A. Nosek, T. Pfeiffer, A. Altmejd, N. Buttrick, T. Chan, Y. Chen, E. Forsell, A. Gampa, E. Heikensten, L. Hummer, T. Imai, S. Isaksson, D. Manfredi, J. Rose, E.-J. Wagenmakers, and H. Wu. 2018. Evaluating the replicability of social science experiments in Nature and Science between 2010 and 2015. Nature Human Behaviour 2 (9):637–644. http://www.nature.com/articles/s41562-018-0399-z.
