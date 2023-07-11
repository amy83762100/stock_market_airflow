# Model Selection and Performance Comparison

We experimented with different models to assess their performance and select the most suitable one based on specific requirements. Here are the results of the conducted experiments:

##  Experiment 1: RandomForestRegressor (Baseline)

Previously, the RandomForestRegressor algorithm was used with the following parameters:
   ```
RandomForestRegressor(n_estimators=50, max_depth=5, random_state=42, n_jobs=-1)
   ```
- Result:
    - Time: 744.51 seconds
    - Memory usage: 483.18 MB
    - MAE: 484,881.77
    - MSE: 44,442,244,640,816.66

##  Experiment 2: LightGBM (boosting='gbdt')

A transition was made from the RandomForestRegressor to LightGBM to improve predictive accuracy and processing speed. The first experiment with LightGBM used the 'gbdt' boosting type and the following parameters:
   ```
    param = {'num_leaves': 75, 'max_depth': 10} # boosting: 'gbdt', learning rate: 0.1
    num_round = 100
   ```
- Result:
    - Time: 57.46 seconds
    - Memory usage: 5807.49 MB
    - MAE: 479,776.44
    - MSE: 69,650,280,259,173.53

##  Experiment 3: LightGBM (boosting='dart')

Another experiment was conducted with LightGBM, this time using the 'dart' boosting type, which introduces dropouts during the tree-building process. The following parameters were used:
   ```
    param = {'num_leaves': 100, 'max_depth': 10, 'boosting': 'dart'} # learning rate: 0.1
    num_round = 100
   ```
- Result:
    - Time: 257.43 seconds
    - Memory usage: 4806.63 MB
    - MAE: 460,743.43
    - MSE: 71,709,656,974,918.84

##  Experiment 4: LightGBM (boosting='gbdt', 'force_row_wise': True)

To explore additional variations, a new experiment was conducted with LightGBM using the 'gbdt' boosting type and the 'force_row_wise' parameter set to True.
   ```
    param = {'num_leaves': 75, 'max_depth': 10, 'force_row_wise': True} # boosting: 'gbdt', learning rate: 0.1
    num_round = 100
   ```
- Result:
    - Time: 90.87 seconds
    - Memory usage: 1770.69 MB
    - MAE: 479,776.44
    - MSE: 69,650,280,259,173.53

##  Experiment 5: LightGBM (boosting='dart', 'force_row_wise': True)

To explore additional variations, a new experiment was conducted with LightGBM using the 'gbdt' boosting type and the 'force_row_wise' parameter set to True.
   ```
    param = {'num_leaves': 100, 'max_depth': 10, 'boosting': 'dart', 'force_col_wise': True} # learning rate: 0.1
    num_round = 100
   ```
- Result:
    - Time: 655.01 seconds
    - Memory usage: 611.24 MB
    - MAE: 460,743.43
    - MSE: 71,709,656,974,918.84

The full experiment log can be found in [docs/ml_model_experiment_results.txt](https://github.com/amy83762100/stock_market_airflow/blob/main/docs/ml_model_experiment_results.txt)

## Model Selection and Trade-offs

- The LightGBM model with 'dart' boosting demonstrated lower MAE compared to the 'gbdt' boosting variant.
- However, the 'gbdt' boosting variant showed faster execution time and lower memory usage compared to 'dart'.
- The 'force_row_wise' parameter, set to True in some experiments, optimized memory usage by reducing the internal memory footprint.

- If minimizing memory usage and execution time are the primary concerns, the 'gbdt' variation may be preferable. It provides a reasonable MAE while demonstrating faster performance and lower memory requirements.

- However, if optimizing prediction accuracy is the top priority and the available computational resources can accommodate the increased memory usage and longer execution time, the 'dart' variation may be the better choice. It achieves a lower MAE, indicating more accurate predictions.

## Conclusion
After conducting several [experiments](https://github.com/amy83762100/stock_market_airflow/blob/main/docs/ml_model_experiment_results.txt), LightGBM was chosen due to its promising performance. The following parameters were selected for LightGBM:
   ```
param = {'num_leaves': 100, 'max_depth': 10, 'boosting': 'dart', 'force_col_wise': True} # learning rate: 0.1
num_round = 100
model = lgb.train(param, d_train, num_round)

   ```
Transitioning from RandomForestRegressor to LightGBM have improved the predictive accuracy and overall speed of the model. Through experimentation, it was determined that using LightGBM with the 'dart' boosting type achieved a better MAE compared to the default 'gbdt' boosting type. The chosen LightGBM model demonstrated improved performance and showed potential for accurate predictions.

(Considering that the outliers in the data do not have a significant impact, prioritizing the Mean Absolute Error (MAE) aligns with the objective of achieving accurate predictions.)
