# dissertation-RS

This project is developed for my dissertation. It has two python scripts: data preparation and modeling and evaluation. The first script selects useful data and transforms JSON file into flat file; the second script assigns weighting scheme to user behaviours, trains the ALS model, lists top-N recommendations, and evaluates recall and nDCG of the model.

To compare different models and select the one with the best performance, one can change the setting of the weighting scheme, alpha, and the number of latent factors. All results will be exported into a log.
