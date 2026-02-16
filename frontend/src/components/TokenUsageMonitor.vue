<template>
  <section class="md:col-span-4 mt-6">
    <h2 class="text-sm font-bold uppercase tracking-widest text-gray-500 px-2 mb-4">Token Usage Monitor (Gemini)</h2>
    <div class="glass rounded-3xl p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <!-- Status -->
            <div class="space-y-4">
                <h3 class="text-xs font-bold text-gray-400 uppercase">Monthly Usage</h3>
                <div class="text-4xl font-mono" :class="tokenStatus.status === 'OK' ? 'text-green-400' : 'text-red-400'">
                    {{ (tokenStatus.used || 0).toLocaleString() }} <span class="text-sm text-gray-600">tokens</span>
                </div>
                <div class="w-full bg-white/10 rounded-full h-2">
                    <div class="h-2 rounded-full transition-all duration-1000"
                         :class="tokenStatus.status === 'OK' ? 'bg-green-500' : 'bg-red-500'"
                         :style="{ width: Math.min(tokenStatus.percentage || 0, 100) + '%' }"></div>
                </div>
                <div class="flex justify-between text-xs text-gray-500 font-mono">
                    <span>{{ tokenStatus.percentage || 0 }}% of Limit</span>
                    <span>{{ (tokenStatus.limit || 0).toLocaleString() }} Limit</span>
                </div>
            </div>

            <!-- Daily Chart -->
            <div class="space-y-4">
                <h3 class="text-xs font-bold text-gray-400 uppercase">Last 7 Days</h3>
                <div class="h-32">
                  <Line :data="chartData" :options="chartOptions" />
                </div>
            </div>

            <!-- Models Breakdown -->
            <div class="space-y-4">
                <h3 class="text-xs font-bold text-gray-400 uppercase">Model Breakdown</h3>
                <div class="space-y-2">
                    <div v-for="model in tokenModels" :key="model.model_name" class="flex items-center justify-between text-sm border-b border-white/5 pb-2">
                        <span class="font-mono text-gray-300">{{ model.model_name }}</span>
                        <span class="font-mono text-blue-400">{{ (model.tokens || 0).toLocaleString() }}</span>
                    </div>
                    <div v-if="tokenModels.length === 0" class="text-center text-gray-600 italic py-4">No usage data yet.</div>
                </div>
            </div>
        </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const tokenStatus = ref({ used: 0, limit: 1000000, percentage: 0, status: 'OK' })
const tokenDaily = ref([])
const tokenModels = ref([])

const fetchTokenUsage = async () => {
  try {
    const [resStatus, resDaily, resModels] = await Promise.all([
      fetch('/api/token-usage/status'),
      fetch('/api/token-usage/daily'),
      fetch('/api/token-usage/models')
    ])
    tokenStatus.value = await resStatus.json()
    tokenDaily.value = await resDaily.json()
    tokenModels.value = await resModels.json()
  } catch (e) {
    console.error('Failed to fetch token usage', e)
  }
}

onMounted(() => {
  fetchTokenUsage()
  setInterval(fetchTokenUsage, 60000) // Poll every minute
})

const chartData = computed(() => ({
  labels: tokenDaily.value.map(d => d.date.slice(5)),
  datasets: [
    {
      label: 'Tokens',
      backgroundColor: 'rgba(59, 130, 246, 0.2)',
      borderColor: 'rgba(59, 130, 246, 1)',
      pointBackgroundColor: 'rgba(59, 130, 246, 1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(59, 130, 246, 1)',
      data: tokenDaily.value.map(d => d.tokens),
      fill: true,
      tension: 0.4
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: 'rgba(0,0,0,0.8)',
      titleFont: {
        size: 10,
        family: 'monospace'
      },
      bodyFont: {
        size: 12,
        family: 'monospace'
      },
      callbacks: {
        label: function(context) {
          return `${context.dataset.label}: ${context.parsed.y.toLocaleString()}`;
        }
      }
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      },
      ticks: {
        color: '#9CA3AF',
        font: {
            size: 10,
            family: 'monospace'
        }
      }
    },
    y: {
      grid: {
        color: 'rgba(255, 255, 255, 0.05)'
      },
      ticks: {
        color: '#9CA3AF',
        font: {
            size: 10,
            family: 'monospace'
        },
        callback: function(value) {
            if (value >= 1000) {
                return (value / 1000) + 'k'
            }
            return value;
        }
      }
    }
  }
}
</script>

<style scoped>
.glass {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
}
</style>
