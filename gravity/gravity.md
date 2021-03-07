---
layout: page
title: Gravity Model of Spatial Interaction
---

The purpose of this week's lab was to create a [Gravity Model of Spatial Interaction](https://transportgeography.org/contents/methods/spatial-interactions-gravity-model/) to determine the service area "catchments" of hospitals.

In the gravity model, the potential for interaction between an input and a destination is based on the attributes of the interacting features and the [friction of distance](https://transportgeography.org/contents/methods/spatial-interactions-gravity-model/spatial-interactions-distance-decay/) between them ([Rodrigue](https://transportgeography.org/contents/methods/spatial-interactions-gravity-model/)). The influences of these weight values, as well as the distance exponent, can be changed in the model. For instance, in our model, hospitals were weighted by the number of beds they have available, and towns served by hospitals are weighted by their population.

In this exercise, we analyzed the interactions between hospital clusters and towns in New England and then compared our results to those of the Dartmouth Health Atlas.

The first step in this process was to create a model to preprocess the [hospitals data](https://hifld-geoplatform.opendata.arcgis.com/datasets/6ac5e325468c4cb9b905f1728d6fbf0f_0), which is sourced from the Department of Homeland Security. This data contains the locations of hospitals in the United States and US Territories. This [model](https://github.com/emmaclinton/emmaclinton.github.io/blob/main/gravity/assets/HSA_Preprocess_Model.model3) takes these hospitals and filters them to the extent of the study area and also removes hospitals that lack data on number of beds, hospitals that are closed, and hospitals that are not categorized as children's hospitals, women's hospitals, or general acute care facilities.

After the HSA data was filtered, the next step was to group the hospitals by town, essentially creating a single centroid for all the hospitals that fall within each zip code. This [model](https://github.com/emmaclinton/emmaclinton.github.io/blob/main/gravity/assets/Preprocess_Filtered_Target_Features.model3) sums the number of beds available in the centroids and retains the ZIP code, the hospital name, and the sum of the beds in the attribute table.

Once the data was preprocessed, the [spatial interaction model](https://github.com/emmaclinton/emmaclinton.github.io/blob/main/gravity/assets/GravityModelUsingDistMatrix.model3) could be implemented. This model takes an input layer (in our case, the towns of New England) and a destination layer (the hospital clusters created in the model above). It converts their geometries into centroids and then runs a distance matrix which calculates the distance between each of the inputs and each of the destinations. The parameter "k", which can be adjusted, determines the number of destinations that will be assessed as a possible service destination for the inputs. The default value of k is 20. The input weight values (town population) and target weight values (number of beds) are then joined as attributes to the distance matrix.

The potential for interaction between a source and a destination can be calculated as **(origin weight * destination weight) / distance^2)**. The potential for interaction increases as the weights of the numerator values increase, and decreases as distance increases in the denominator. Initially, input and target features with weights of 0 are excluded from the analysis using the Extract by Expression tool.

In this model, the relative influences of the weights and the distance can be altered by changing their respective exponents. The input weight's influence can be changed via the lambda variable (default = 1), the target weight's influence can be changed by changing alpha (default = 1) and the distance parameter can be changed by changing beta (default = 2).

After potential has been calculated for each input-target pair, the maximum potential value for each input is determined using the Field Calculator. For each input, the input-target combination with the highest potential is determined to be the most likely option for interaction.

The maximum potential data is then joined back to the input layer (in our case, towns) and this information is aggregated to form hospital service area 'catchments' comprised of all towns that are served by a hospital cluster target point.

![Spatial Interaction Model](/assets/GravityModel.png)


Here is a link to the [map](assets/)!
