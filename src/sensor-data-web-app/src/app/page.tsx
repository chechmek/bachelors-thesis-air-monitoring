'use client'

import type { NextPage } from 'next'
import { useEffect, useState } from 'react'
import { getLatestForecast, getLatestMetrics } from './actions'
import { Forecast, HourlySensorMetrics } from '@/types'
import ForecastGraph from '@/components/ForecastGraph'
import MetricCard from '@/components/MetricCard'

const Home: NextPage = () => {
  const [forecast, setForecast] = useState<Forecast | null>(null)
  const [metrics, setMetrics] = useState<HourlySensorMetrics | null>(null)
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    setLoading(true)
    try {
      const [forecastData, metricsData] = await Promise.all([
        getLatestForecast(),
        getLatestMetrics()
      ])
      setForecast(forecastData)
      setMetrics(metricsData)
    } catch (error) {
      console.error('Error fetching data:', error)
    }
    setLoading(false)
  }

  useEffect(() => {
    fetchData()
  }, [])

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-gray-900">Sensor Live Data</h1>
        <ForecastGraph
          forecast={forecast}
          loading={loading}
          onRefetch={fetchData}
        />
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <MetricCard
            title="Current PM2.5"
            value={forecast?.input_sequence[forecast.input_sequence.length - 1] ?? 0}
            color="text-blue-500"
          />
          <MetricCard
            title="1-hour Predicted PM2.5"
            value={forecast?.predicted_sequence[0] ?? 0}
            color="text-yellow-500"
          />
          <MetricCard
            title="Current AQI"
            value={metrics?.aqi ?? 0}
            color="text-green-500"
          />
          <MetricCard
            title="Temperature"
            value={metrics?.avg_temp ?? 0}
            unit="°C"
            color="text-red-500"
          />
          <MetricCard
            title="Humidity"
            value={metrics?.avg_humidity ?? 0}
            unit="%"
            color="text-purple-500"
          />
        </div>
      </div>
    </main>
  )
}

export default Home
