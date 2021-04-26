---
layout: page
title: RP- Vulnerability modeling for sub-Saharan Africa
---


**Replication of**
# Vulnerability modeling for sub-Saharan Africa

Original study *by* Malcomb, D. W., E. A. Weaver, and A. R. Krakowka. 2014. Vulnerability modeling for sub-Saharan Africa: An operationalized approach in Malawi. *Applied Geography* 48:17–30. DOI:[10.1016/j.apgeog.2014.01.004](https://doi.org/10.1016/j.apgeog.2014.01.004)

Replication Authors:
Your Name, Joseph Holler, Kufre Udoh, Open Source GIScience students of Fall 2019 and Spring 2021

Replication Materials Available at: [github repository name](github repository link)

Created: `04 April 2021`
Revised: `06 April 2021`

## Abstract

The original study is a multi-criteria analysis of vulnerability to Climate Change in Malawi, and is one of the earliest sub-national geographic models of climate change vulnerability for an African country. The study aims to be replicable, and had 40 citations in Google Scholar as of April 8, 2021.

## Original Study Information

The study region is the country of Malawi. The spatial support of input data includes DHS survey points, Traditional Authority boundaries, and raster grids of flood risk (0.833 degree resolution) and drought exposure (0.416 degree resolution).

The original study was published without data or code, but has detailed narrative description of the methodology. The methods used are feasible for undergraduate students to implement following completion of one introductory GIS course. The study states that its data is available for replication in 23 African countries.


### Data Description and Variables

*Access and Assets Data:*
 Demographic and Health Survey data are a product of the United States Agency for International Development (USAID). Variables contained in this dataset are used to represent adaptive capacity (access + assets) in the Malcomb et al.’s (2014) study. These data come from survey questionnaires with large sample sizes.
The DHS data used in our study were collected in 2010. In Malawi, the provenance of the DHA data dates back as far as 1992, but has not been collected consistently every year. Each point in the household dataset represents a cluster of households with each cluster corresponding to some form of census enumeration units, such as villages in rural areas or city blocks in urban areas [DHS GPS Manual](/data/metadata/DHS_GPS_Manual_English_A4_24May2013_DHSM9.pdf). This means that each household in each cluster has the same GPS data. This data is collected by trained [USAID](https://www.usaid.gov/) staff using GPS receivers.
Missing data is a common occurrence in this dataset as a result of negligence or incorrect naming. However, according to the [DHS GPS Manual](/data/metadata/DHS_GPS_Manual_English_A4_24May2013_DHSM9.pdf), these issues are easily rectified and typically sites for which data does not exist are recollected. Sometimes, however, missing information is coded in as such or assigned a proxy location.
The DHS website acknowledges the high potential for inconsistent or incomplete data in such broad and expansive survey sets. Missing survey data (responses) are never estimated or made up; they are instead coded as a special response indicating the absence of data. As well, there are clear policies in place to ensure the data’s accuracy. More information about data validity can be found on the [DHS’s Data Quality and Use site](https://www.dhsprogram.com/data/Data-Quality-and-Use.cfm). In this analysis, we use the variables listed in **Table 1** to determine the average adaptive capacity of each TA area. Data transformations are outlined below.


**Table 1.** DHS variables used in this analysis.
| Variable Code | Definition |
| ------------- | ------------- |
| HHID | "Case Identification" |
| HV001 | "Cluster number" |
|HV002 | Household number |
| HV246A |"Cattle own" |
|HV246D | "Goats own"|
|HV246E | "Sheep own" |
|HV246G | "Pigs own" |
| HV248 |"Number of sick people 18-59"|
| HV245 | "Hectares for agricultural land"|
|HV271 | "Wealth index factor score (5 decimals)"|
|HV251 | "Number of orphans and vulnerable children"|
|HV207 | “Has Radio” |
| HV243A | “Has a Mobile Telephone”|
|HV219 | Sex of Head of Household”|
|HV226 | “Type of Cooking Fuel” |
| HV206 |"Has electricty” |
 |HV204 |“Time to get to Water Source”|

**Variable Transformations**
1. Eliminate households with null and/or missing values
1. Join TA and LHZ ID data to the DHS clusters
1. Eliminate NA values for livestock
1. Sum counts of all different kinds of livestock into a single variable
1. Apply weights to normalized indicator variables to get scores for each category (assets, access)
1. Find the statistics of the capacity of each TA (min, max, mean, sd)
1. Join ta_capacity to TAs based on ta_id
1. Prepare breaks for mapping
1. Class intervals based on capacity_2010 field
1. Take the values and round them to 2 decimal places
1. Put data in 4 classes based on break values

*Livelihood Zones Data:*

The livelihood zone data is created by aggregating general regions where similar crops are grown and similar ecological patterns exist. This data exists originally at the household level and was aggregated into Livelihood Zones. To construct the aggregation used for “Livelihood Sensitivity” in this analysis, we use these household points from the FEWSnet data that had previously been aggregated into livelihood zones. The four Livelihood Sensitivity categories are 1) Percent of food from own farm (6%); 2) Percent of income from wage labor (6%); 3) Percent of income from cash crops (4%); and 4) Disaster coping strategy (4%). In the original R script, household data from the DHS survey was used as a proxy for the specific data points in the livelihood sensitivity analysis (transformation: Join with DHS clusters to apply LHZ FNID variables). With this additional FEWSnet data at the household level, we can construct these four livelihood sensitivity categories using existing variables (Table 1).

**Table 2.** Constructing livelihood sensitivity categories

| Livelihood Sensitivity Category (LSC)  | Percent Contributing| How LSC was constructed |
| ------------- | ------------- | ------------- |
| Percent of food from own farm  |  6% | Sources of food: crops + livestock  |
| Percent of income from wage labor  | 6%  | Sources of cash: labour etc. / total * 100 |
| Percent of income from cash crops  | 4%  | sources of cash (Crops): (tobacco + sugar + tea + coffee) + / total sources of cash * 100  |
| Disaster coping strategy  | 4%  | Self-employment & small business and trade: (firewood + sale of wild food + grass + mats + charcoal) / total sources of cash * 100 |


*Physical Exposure Data*:
**Flood Data:** This dataset stems from work collected by multiple agencies and funneled into the PREVIEW Global Risk Data Platform, “an effort to share spatial information on global risk from natural hazards.” The dataset was designed by UNEP/GRID-Europe for the Global Assessment Report on Risk Reduction (GAR), using global data. A flood estimation value is assigned via an index of 1 (low) to 5 (extreme)
**Drought Data:**This dataset uses the Standardized Precipitation Index to measure annual drought exposure across the globe. The Standardized Precipitation Index draws on data from a “global monthly gridded precipitation dataset” from the University of East Anglia’s Climatic Research Unit, and was modeled in GIS using methodology from Brad Lyon at Columbia University. The dataset draws on 2010 population information from the LandScanTM Global Population Database at the Oak Ridge National Laboratory.  Drought exposure is reported as the expected average annual (2010) population exposed. The data were compiled by UNEP/GRID-Europe for the Global Assessment Report on Risk Reduction (GAR). The data use the WGS 1984 datum, span the years 1980-2001, and are reported in raster format with spatial resolution 1/24 degree x 1/24 degree.

**Variable Transformations**
1. Load in UNEP raster
1. Set CRS for drought to EPSG:4326
1. Set CRS for flood to EPSG:4326
1.Reproject, clip, and resample based on bounding box (dimensions: xmin = 35.9166666666658188, xmax = 32.6666666666658330,  ymin = -9.3333333333336554, ymax = -17.0833333333336270) and resolution of blank raster we created: resolution is 1/24 degree x 1/24 degree
1. Use bilinear resampling for drought to average continuous population exposure values
1. Use nearest-neighbor resampling for flood risk to preserve integer values


Outline the data used in the study, including:

- sources of each data layer and
- the variable(s) used from each data source
- transformations applied to the variables (e.g. rescaling variables, calculating derived variables, aggregating to different geographic units, etc.)

This part may be compiled collaboratively as a group!

## Analytical Specification

The original study was conducted using ArcGIS and STATA, but does not state which versions of these software were used.
The replication study will use R.

### Materials and Procedure
The steps outlined below mirror the steps used in the [R Code for this project](https://github.com/emmaclinton/RP-Malcomb/blob/main/procedure/code/RP-Malcomb-jh.Rmd).

*Process Adaptive Capacity*
1. Bring in DHS Data [Households Level] (vector)
2. Bring in TA (Traditional Authority boundaries) and LHZ (livelihood zones) data
3. Get rid of unsuitable households (eliminate NULL and/or missing values)
3. Join TA and LHZ ID data to the DHS clusters
4. Pre-process the livestock data
	Filter for NA livestock data
	Update livestock data (summing different kinds)
5. FIELD CALCULATOR: Normalize each indicator variable and rescale from 1-5 (real numbers) based on percent rank
6. FIELD CALCULATOR / ADD FIELD: Apply weights to normalized indicator variables to get scores for each category (assets, access)
7. SUMMARIZE/AGGREGATE: find the stats of the capacity of each TA (min, max, mean, sd)
8. Join ta_capacity to TA based on ta_id
	(Multiply by 20--meaningless??) I have a question about this (so do I) ln.216
9. Prepare breaks for mapping
Class intervals based on capacity_2010 field
Take the values and round them to 2 decimal places
Put data in 4 classes based on break values
10. Save the adaptive capacity scores

*Process Livelihood Sensitivity*
1. Load in LHZ geometries into R
2. Join LHZ sensitivity data into R code
3. Read in processed LHZ dataset
4. Join the data to the LHZ geometries
5. Put LHZ data into quintiles
6. Calculate capacity score based on values in Malcomb et al. (2014)


*Process Physical Exposure*
1. Load in UNEP rasterSet CRS for drought
2. Set CRS for flood
3. Clean and reproject rasters
4. Create a bounding box at extent of Malawi Where does this info come from
5. For Drought: use bilinear to avg continuous population exposure values
6. For Flood: use nearest neighbor to preserve integer values
7. CLIP the traditional authorities with the LHZs to cut out the lake
8. RASTERIZE the ta_capacity data with pixel data corresponding to capacity_2010 field
9. RASTERIZE the livelihood sensitivity score with pixel data corresponding to capacity_2010 field

*Raster Calculations*
1. Create a mask
2. Reclassify the flood layer (quintiles, currently binary)
3. Reclassify the drought values (quantile [from 0 - 1 in intervals of 0.2 =5])
4. AGGREGATE: Create final vulnerability layer using environmental vulnerability score and ta_capacity.

We then georeferenced maps from the original study using QGIS in order to compare the results generated by our R script to those found in Malcomb et al. (2014). We ran a Spearman's Rho correlation test between the two maps of Figs. 4 and 5 to determine the differences in results.

## Unplanned Deviations from the Protocol
Our first pass at creating a workflow before seeing the data outlined several areas of uncertainty. For instance, we were unsure of at what level of organization the DHS data came in (household level, village level, or district level). We were also unsure of the factors outlined below, which are ultimate sources of uncertainty in our replication analysis.

In this protocol, it was unclear how exactly the livelihood zones data were divided into the four categories of livelihood sensitivity. This is a large source of uncertainty in our analysis. In addition, the original study states that it broke the data into quintiles by assigning values of 0-5 to the data. This would actually result in six classes, or sextiles. We decided to use quintiles and assigned values of 1-5 when normalizing our data. It is also unclear how binary data in the original study was normalized on a 1-5 scale. For binary variables (e.g. sex), we assigned a value of 1 to the presumed lower-risk option (e.g. male) and a value of 2 to the higher-risk (e.g. female).

It was also unclear when data were aggregated to the TA level—was this done before or after the data scores were normalized and weighted in the original study? We decided to aggregate after the data had been normalized and weighted.

Summarize changes and uncertainties between
- your interpretation and plan for the workflow based on reading the paper
- your final workflow after accessing the data and code and completing the code

### Discussion

Our replication analysis yielded slightly different results than those generated in the original study. **Fig. 1** shows the results of our replication analysis in terms of access and assets in 2010 on the Traditional Authority level of organization.
**Fig. 2** shows the difference between our results and those generated by Malcomb et al. (2014)

![Results (TA Adaptive Capacity)](/maps/ac_2010.png)
_(Fig. 1) Access and assets (adaptive capacity) scores from our results._

![Results (TA Adaptive Capacity)](/maps/ac_2010.png)
_(Fig. 2) Difference in access and assets (adaptive capacity) scores (reproduction score - original study score)._

Figures to Include:
map of your reproduction results for figure 4
map of your reproduction results for figure 5
map to visualize the difference of results for figure 4
map to visualize the difference of results for figure 5
table to quantify the difference of results for figure 4
scatterplot graph to visualize the difference of results for figure 5
spearman’s rho correlation results for figure 4 and for figure 5

Provide a summary and interpretation of the key findings of the replication *vis-a-vis* the original study results. If the attempt was a failure, discuss possible causes of the failure. In this replication, any failure is probably due to practical causes, which may include:
- lack of data
- lack of code
- lack of details in the original analysis
- uncertainties due to manner in which data has been used

## Conclusion

Restate the key findings and discuss their broader societal implications or contributions to theory.
Do the research findings suggest a need for any future research?

## References

Include any referenced studies or materials in the [AAG Style of author-date referencing](https://www.tandf.co.uk//journals/authors/style/reference/tf_USChicagoB.pdf).

####  Report Template References & License

This template was developed by Peter Kedron and Joseph Holler with funding support from HEGS-2049837. This template is an adaptation of the ReScience Article Template Developed by N.P Rougier, released under a GPL version 3 license and available here: https://github.com/ReScience/template. Copyright © Nicolas Rougier and coauthors. It also draws inspiration from the pre-registration protocol of the Open Science Framework and the replication studies of Camerer et al. (2016, 2018). See https://osf.io/pfdyw/ and https://osf.io/bzm54/

Camerer, C. F., A. Dreber, E. Forsell, T.-H. Ho, J. Huber, M. Johannesson, M. Kirchler, J. Almenberg, A. Altmejd, T. Chan, E. Heikensten, F. Holzmeister, T. Imai, S. Isaksson, G. Nave, T. Pfeiffer, M. Razen, and H. Wu. 2016. Evaluating replicability of laboratory experiments in economics. Science 351 (6280):1433–1436. https://www.sciencemag.org/lookup/doi/10.1126/science.aaf0918.

Camerer, C. F., A. Dreber, F. Holzmeister, T.-H. Ho, J. Huber, M. Johannesson, M. Kirchler, G. Nave, B. A. Nosek, T. Pfeiffer, A. Altmejd, N. Buttrick, T. Chan, Y. Chen, E. Forsell, A. Gampa, E. Heikensten, L. Hummer, T. Imai, S. Isaksson, D. Manfredi, J. Rose, E.-J. Wagenmakers, and H. Wu. 2018. Evaluating the replicability of social science experiments in Nature and Science between 2010 and 2015. Nature Human Behaviour 2 (9):637–644. http://www.nature.com/articles/s41562-018-0399-z.
