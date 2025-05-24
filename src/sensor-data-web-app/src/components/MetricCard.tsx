interface MetricCardProps {
  title: string
  value: number | string
  unit?: string
  color: string
}

export default function MetricCard({ title, value, unit = '', color }: MetricCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-lg font-semibold mb-2 text-gray-900">{title}</h3>
      <p className={`text-3xl font-bold ${color}`}>
        {typeof value === 'number' ? value.toFixed(1) : value}{unit}
      </p>
    </div>
  )
} 