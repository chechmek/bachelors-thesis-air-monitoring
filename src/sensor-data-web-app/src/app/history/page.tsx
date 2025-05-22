'use client'

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
import { getHistoricalMetrics } from '../actions'
import { HourlySensorMetrics } from '@/types'

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

const chartOptions: ChartOptions<'line'> = {
  responsive: true,
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
          return `${label}: ${value.toFixed(2)}`
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
        text: 'Value',
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

export default function History() {
  const [metrics, setMetrics] = useState<HourlySensorMetrics[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      try {
        const data = await getHistoricalMetrics()
        setMetrics(data)
      } catch (error) {
        console.error('Error fetching data:', error)
      }
      setLoading(false)
    }

    fetchData()
  }, [])

  const aqiData = {
    labels: metrics.map(m => new Date(m.window_end_time).toLocaleString()),
    datasets: [{
      label: 'AQI',
      data: metrics.map(m => m.aqi),
      borderColor: '#22c55e',
      backgroundColor: 'rgba(34, 197, 94, 0.1)',
      fill: true
    }]
  }

  const pm25Data = {
    labels: metrics.map(m => new Date(m.window_end_time).toLocaleString()),
    datasets: [{
      label: 'PM2.5',
      data: metrics.map(m => m.avg_pm2_5),
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      fill: true
    }]
  }

  const tempData = {
    labels: metrics.map(m => new Date(m.window_end_time).toLocaleString()),
    datasets: [{
      label: 'Temperature (°C)',
      data: metrics.map(m => m.avg_temp),
      borderColor: '#ef4444',
      backgroundColor: 'rgba(239, 68, 68, 0.1)',
      fill: true
    }]
  }

  const humidityData = {
    labels: metrics.map(m => new Date(m.window_end_time).toLocaleString()),
    datasets: [{
      label: 'Humidity (%)',
      data: metrics.map(m => m.avg_humidity),
      borderColor: '#a855f7',
      backgroundColor: 'rgba(168, 85, 247, 0.1)',
      fill: true
    }]
  }

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-gray-900">Historical Data</h1>

        <div className="grid grid-cols-1 gap-8">
          {loading ? (
            <div className="h-96 flex items-center justify-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
            </div>
          ) : (
            <>
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-900">AQI History</h2>
                <div className="h-96">
                  <Line data={aqiData} options={chartOptions} />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-900">PM2.5 History</h2>
                <div className="h-96">
                  <Line data={pm25Data} options={chartOptions} />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-900">Temperature History</h2>
                <div className="h-96">
                  <Line data={tempData} options={chartOptions} />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-900">Humidity History</h2>
                <div className="h-96">
                  <Line data={humidityData} options={chartOptions} />
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </main>
  )
} 