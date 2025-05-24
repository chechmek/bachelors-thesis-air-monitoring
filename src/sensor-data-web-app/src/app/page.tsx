'use client'

import type { NextPage } from 'next'
import { useEffect, useState } from 'react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js'
import zoomPlugin from 'chartjs-plugin-zoom'
import { getLatestForecast, getLatestMetrics } from './actions'
import { Forecast, HourlySensorMetrics } from '@/types'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  zoomPlugin
)

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

  const chartData = {
    labels: forecast ? [
      ...forecast.input_sequence.slice(-24).map((_, i) => `-${24 - i}m`),
      ...forecast.predicted_sequence.map((_, i) => `+${i + 1}h`)
    ] : [],
    datasets: [
      {
        label: 'PM2.5',
        data: forecast ? [
          ...forecast.input_sequence.slice(-24),
          ...forecast.predicted_sequence
        ] : [],
        borderWidth: 2,
        fill: false,
        pointBackgroundColor: (ctx) => {
          const index = ctx.dataIndex
          return index < 24 ? '#3b82f6' : '#eab308'
        },
        pointBorderColor: (ctx) => {
          const index = ctx.dataIndex
          return index < 24 ? '#3b82f6' : '#eab308'
        },
        segment: {
          borderColor: (ctx) => {
            const index = ctx.p0DataIndex
            return index < 24 ? '#3b82f6' : '#eab308'
          }
        }
      }
    ]
  }

  console.log('Chart Data:', {
    labels: chartData.labels,
    data: chartData.datasets[0].data,
    inputLength: forecast?.input_sequence.length,
    predictedLength: forecast?.predicted_sequence.length
  })

  const chartOptions: ChartOptions<'line'> = {
    responsive: true,
    spanGaps: true,
    plugins: {
      zoom: {
        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true
          },
          mode: 'x',
        },
        pan: {
          enabled: true,
          mode: 'x',
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const label = context.dataset.label || ''
            const value = context.parsed.y
            const index = context.dataIndex
            const type = index < 24 ? 'Input' : 'Predicted'
            return `${type} ${label}: ${value.toFixed(2)}`
          }
        }
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Time',
          color: '#374151'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        },
        ticks: {
          color: '#374151'
        }
      },
      y: {
        title: {
          display: true,
          text: 'PM2.5',
          color: '#374151'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        },
        ticks: {
          color: '#374151'
        }
      }
    }
  }

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-gray-900">Sensor Live Data</h1>
        
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-gray-900">PM2.5 Forecast</h2>
            <button
              onClick={fetchData}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            >
              Refetch
            </button>
          </div>
          
          {loading ? (
            <div className="h-96 flex items-center justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            </div>
          ) : (
            <div className="h-96">
              <Line data={chartData} options={chartOptions} />
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-2 text-gray-900">Current PM2.5</h3>
            <p className="text-3xl font-bold text-blue-500">
              {forecast?.input_sequence[forecast.input_sequence.length - 1].toFixed(2)}
            </p>
          </div>
          
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-2 text-gray-900">1-hour Predicted PM2.5</h3>
            <p className="text-3xl font-bold text-yellow-500">
              {forecast?.predicted_sequence[0].toFixed(2)}
            </p>
          </div>
          
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-2 text-gray-900">Current AQI</h3>
            <p className="text-3xl font-bold text-green-500">
              {metrics?.aqi}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-2 text-gray-900">Temperature</h3>
            <p className="text-3xl font-bold text-red-500">
              {metrics?.avg_temp.toFixed(1)}°C
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-2 text-gray-900">Humidity</h3>
            <p className="text-3xl font-bold text-purple-500">
              {metrics?.avg_humidity.toFixed(1)}%
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}

export default Home
