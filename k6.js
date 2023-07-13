import http from 'k6/http'
import { check, sleep } from 'k6'


export const options = {
    scenarios: {
        constant_load: {
        executor: 'constant-arrival-rate',
        rate: 10, // Requests per second
        duration: '1m', // Duration of the scenario
        preAllocatedVUs: 10, // Number of VUs to pre-allocate
        maxVUs: 20, // Maximum number of VUs
        },
        burst_load: {
        executor: 'per-vu-iterations',
        vus: 5,
        iterations: 20,
        maxDuration: '10s',
        },
        gradual_load: {
        executor: 'ramping-vus',
        startVUs: 1,
        stages: [
            { duration: '1m', target: 10 },
            { duration: '2m', target: 20 },
            { duration: '1m', target: 5 },
        ],
        gracefulRampDown: '30s',
        },
    },
}

export function setup() {
  const vol_moving_avg = Math.random() * 1000000 // Generate a random value for vol_moving_avg
  const adj_close_rolling_med = Math.random() * 100 // Generate a random value for adj_close_rolling_med

  return { vol_moving_avg, adj_close_rolling_med }
}

export default function (data) {
    const { vol_moving_avg, adj_close_rolling_med } = data

    const params = {
        headers: {
        'Content-Type': 'application/json',
        },
    }

    const response = http.get(
        `https://stock-market-api-v1-0c7118cdd11c.herokuapp.com/predict?vol_moving_avg=${vol_moving_avg}&adj_close_rolling_med=${adj_close_rolling_med}`,
        params
    )

    check(response, {
        'Status is 200': (r) => r.status === 200,
        'Response is a number': (r) => !isNaN(r.body),
    })

    sleep(1) // Wait for 1 second before making the next request
}
