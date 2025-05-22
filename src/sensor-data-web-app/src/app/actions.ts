'use server'

import pool from '@/lib/db'
import { Forecast, HourlySensorMetrics } from '@/types'

export async function getLatestForecast(): Promise<Forecast> {
  const result = await pool.query(
    'SELECT * FROM forecast ORDER BY date_forecasted DESC LIMIT 1'
  )
  return result.rows[0]
}

export async function getLatestMetrics(): Promise<HourlySensorMetrics> {
  const result = await pool.query(
    'SELECT * FROM hourly_sensor_metrics ORDER BY window_end_time DESC LIMIT 1'
  )
  return result.rows[0]
}

export async function getHistoricalMetrics(): Promise<HourlySensorMetrics[]> {
  const result = await pool.query(
    'SELECT * FROM hourly_sensor_metrics ORDER BY window_end_time DESC LIMIT 100'
  )
  return result.rows
} 