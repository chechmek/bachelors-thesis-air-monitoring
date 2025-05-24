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
import { Forecast } from '@/types'

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

interface ForecastGraphProps {
  forecast: Forecast | null
  loading: boolean
  onRefetch: () => void
}

export default function ForecastGraph({ forecast, loading, onRefetch }: ForecastGraphProps) {
  const chartData = {
    labels: forecast ? [
      ...forecast.input_sequence.slice(-24).map((_, i) => {
        if (i === 0) return '2 hours ago'
        if (i === 12) return '1 hour ago'
        return ''
      }),
      ...forecast.predicted_sequence.map((_, i) => {
        if (i === 0) return 'current'
        if (i === 10) return '1 hour forecast'
        return ''
      })
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
        pointBackgroundColor: (ctx: { dataIndex: number }) => {
          const index = ctx.dataIndex
          return index < 24 ? '#3b82f6' : '#eab308'
        },
        pointBorderColor: (ctx: { dataIndex: number }) => {
          const index = ctx.dataIndex
          return index < 24 ? '#3b82f6' : '#eab308'
        },
        segment: {
          borderColor: (ctx: { p0DataIndex: number }) => {
            const index = ctx.p0DataIndex
            return index < 24 ? '#3b82f6' : '#eab308'
          }
        }
      }
    ]
  }

  console.log('Chart data:', chartData) 

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
    <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-900">PM2.5 Forecast</h2>
        <button
          onClick={onRefetch}
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
  )
} 