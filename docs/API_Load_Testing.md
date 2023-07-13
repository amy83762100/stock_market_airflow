# API Load Testing
## Methodology

The load testing was performed using the k6 load testing tool. The test script (`k6.js`) was designed to simulate different scenarios representing various load patterns. The scenarios included in the load test were:

1. `burst_load`: This scenario involved 5 virtual users (VUs) making 20 iterations each, with a maximum duration of 10 seconds and a graceful stop of 30 seconds.
2. `gradual_load`: This scenario involved gradually ramping up the number of VUs over three stages, reaching a maximum of 20 VUs. The duration of this scenario was 4 minutes, with a graceful ramp-down and a graceful stop of 30 seconds.
3. `constant_load`: This scenario maintained a constant arrival rate of 10 iterations per second for 1 minute, with a maximum of 10 to 20 VUs and a graceful stop of 30 seconds.

The load test aimed to analyze the API's performance under different load patterns and provide insights into its scalability and response times.
## Test Results

![Screenshot 2023-07-13 at 1 54 19 PM](https://github.com/amy83762100/stock_market_airflow/assets/76548841/aa2791e6-3e51-4922-b9e5-1581f346dccf)

## Analysis

Based on the load test results, the following bottlenecks were observed:

1. Response Time: The P95 response time for all scenarios ranged between 162 ms and 185 ms. This indicates that the API response time might increase under high load, affecting the overall performance.

2. Low Requests per Second: The average RPS for the burst load scenario was only 0.19, indicating that the API might struggle to handle high concurrency and might require optimizations to improve its throughput.

## Future Improvement

- Model Caching: Loading the model for every prediction can be time-consuming. Instead, you can load the model once during the application startup and store it in memory. Subsequently, reuse the loaded model for each prediction request. This avoids the overhead of loading the model from disk for every request.

- Model Serving Frameworks: Utilizing model serving frameworks can simplify the deployment and management of machine learning models in production. 