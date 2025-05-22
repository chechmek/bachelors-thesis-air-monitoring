export interface Forecast {
  id: number
  date_forecasted: string
  date_target: string
  input_sequence: number[]
  predicted_sequence: number[]
  pm2_5: number
}

export interface HourlySensorMetrics {
  id: number
  window_end_time: string
  avg_temp: number
  avg_humidity: number
  avg_pm2_5: number
  aqi: number
} 