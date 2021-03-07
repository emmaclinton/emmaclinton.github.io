---
layout: page
title: Gravity Model of Spatial Interaction
---

The purpose of this week's lab was to create a [Gravity Model of Spatial Interaction](https://transportgeography.org/contents/methods/spatial-interactions-gravity-model/) to determine the service area "catchments" of hospitals.

In the gravity model, the potential for interaction between an input and a destination is based on the attributes of the interacting features and the [friction of distance](https://transportgeography.org/contents/methods/spatial-interactions-gravity-model/spatial-interactions-distance-decay/) between them ([Rodrigue](https://transportgeography.org/contents/methods/spatial-interactions-gravity-model/)). The influences of these weight values, as well as the distance exponent, can be changed in the model. For instance, in our model, hospitals were weighted by the number of beds they have available, and towns served by hospitals are weighted by their population.

In this exercise, we analyzed the interactions between hospital clusters and towns in New England and then compared our results to those of the Dartmouth Health Atlas.

The first step in this process was to create a model to preprocess the [hospitals data](https://hifld-geoplatform.opendata.arcgis.com/datasets/6ac5e325468c4cb9b905f1728d6fbf0f_0), which is sourced from the Department of Homeland Security. This data contains the locations of hospitals in the United States and US Territories. This model takes these hospitals and filters them to the analysis extent and also removes hospitals that lack data on number of beds, hospitals that are closed, and hospitals that are not categorized as children's hospitals, women's hospitals, or general acute care facilities.

Link to model3 files and images of models

Here is a link to the [map](assets/)!
