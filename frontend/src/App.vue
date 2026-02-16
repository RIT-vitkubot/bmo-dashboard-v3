<script setup>
import { ref, onMounted } from 'vue'

const tasks = ref([])
const stats = ref({ cpu: 0, ram: 0, disk: 0 })
const bmoMessage = ref('')
const scheduleEvents = ref([])
const isUpdating = ref(false)

// Token Usage
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

const triggerFlash = () => {
  isUpdating.value = true
  setTimeout(() => {
    isUpdating.value = false
  }, 1000)
}

const fetchTasks = async () => {
  try {
    const res = await fetch('/api/activities')
    tasks.value = await res.json()
    triggerFlash()
  } catch (e) {
    console.error('Failed to fetch tasks', e)
  }
}

const fetchStats = async () => {
  try {
    const res = await fetch('/api/stats')
    stats.value = await res.json()
    // stats are fetched every 5s, maybe only flash on significant changes or just a subtle indicator
  } catch (e) {
    console.error('Failed to fetch stats', e)
  }
}

const fetchBmoSays = async () => {
  try {
    const res = await fetch('/api/bmo-says')
    const data = await res.json()
    bmoMessage.value = data.message
  } catch (e) {
    console.error('Failed to fetch BMO message', e)
  }
}

const fetchSchedule = async () => {
  try {
    const res = await fetch('/api/schedule')
    scheduleEvents.value = await res.json()
  } catch (e) {
    console.error('Failed to fetch schedule', e)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return dateString 
  const pad = (num) => String(num).padStart(2, '0')
  const yyyy = date.getFullYear()
  const mm = pad(date.getMonth() + 1)
  const dd = pad(date.getDate())
  const hh = pad(date.getHours())
  const min = pad(date.getMinutes())
  return `${yyyy}-${mm}-${dd} ${hh}:${min}`
}

const getCalColor = (calName) => {
  if (!calName) return 'text-blue-400'
  const name = calName.toLowerCase()
  if (name.includes('❤') || name.includes('srdce') || name.includes('love')) return 'text-red-400'
  if (name.includes('tul')) return 'text-blue-400'
  if (name.includes('moe')) return 'text-green-400'
  return 'text-purple-400'
}

const getCalBorder = (calName) => {
  if (!calName) return 'hover:border-blue-500/30'
  const name = calName.toLowerCase()
  if (name.includes('❤') || name.includes('srdce') || name.includes('love')) return 'hover:border-red-500/30'
  if (name.includes('tul')) return 'hover:border-blue-500/30'
  if (name.includes('moe')) return 'hover:border-green-500/30'
  return 'hover:border-purple-500/30'
}

onMounted(() => {
  fetchTasks()
  fetchStats()
  fetchBmoSays()
  fetchSchedule()
  fetchTokenUsage()
  
  // Polling intervals per requirements
  setInterval(fetchStats, 5000)      // stats 5s
  setInterval(fetchTasks, 30000)     // activities 30s
  setInterval(fetchSchedule, 300000) // schedule 5min
  setInterval(fetchBmoSays, 60000)    // BMO says 1min
  setInterval(fetchTokenUsage, 60000) // Token usage 1min
})
</script>

<template>
  <div class="min-h-screen bg-black text-white p-6 font-sans">
    <!-- Header / BMO Activity Status -->
    <header class="mb-10">
      <div class="glass rounded-2xl p-6 flex items-center space-x-4">
        <div class="text-4xl">🤖</div>
        <div>
          <h1 class="text-xl font-semibold text-gray-100">BMO Status Monitor <span class="text-[10px] bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded ml-2 uppercase tracking-widest">v3.1 Intelligence</span></h1>
          <p class="text-gray-400 italic">"{{ bmoMessage || 'Initializing BMO internal systems...' }}"</p>
        </div>
      </div>
    </header>

    <!-- BMO Schedule Bar -->
    <section v-if="scheduleEvents.length > 0" class="mb-10">
      <div class="flex items-center space-x-2 px-2 mb-4">
        <span class="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
        <h2 class="text-sm font-bold uppercase tracking-widest text-gray-500">BMO Internal Cron Schedule</h2>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="job in scheduleEvents.slice(0, 4)" :key="job.name + job.time" 
             class="glass rounded-xl p-4 border border-white/5 transition-all hover:border-blue-500/30">
          <div class="flex items-center space-x-1 mb-1">
            <span class="text-[10px]">🕒</span>
            <p class="text-[10px] font-bold uppercase text-blue-400">{{ job.time }}</p>
          </div>
          <h3 class="text-sm font-medium text-gray-200 truncate">{{ job.name }}</h3>
        </div>
      </div>
    </section>

    <main class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <!-- BMO Core Stats -->
      <section class="md:col-span-1 space-y-6">
        <h2 class="text-sm font-bold uppercase tracking-widest text-gray-500 px-2">BMO Core Health</h2>
        <div class="glass rounded-3xl p-6 space-y-6">
          <div>
            <div class="flex justify-between mb-2">
              <span class="text-sm font-medium text-gray-400">Computational Load</span>
              <span class="text-sm font-medium">{{ stats.cpu }}%</span>
            </div>
            <div class="w-full bg-white/10 rounded-full h-1.5">
              <div class="bg-blue-500 h-1.5 rounded-full transition-all duration-500 shadow-[0_0_8px_rgba(59,130,246,0.5)]" :style="{ width: stats.cpu + '%' }"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between mb-2">
              <span class="text-sm font-medium text-gray-400">Memory Allocation</span>
              <span class="text-sm font-medium">{{ stats.ram }}%</span>
            </div>
            <div class="w-full bg-white/10 rounded-full h-1.5">
              <div class="bg-purple-500 h-1.5 rounded-full transition-all duration-500 shadow-[0_0_8px_rgba(168,85,247,0.5)]" :style="{ width: stats.ram + '%' }"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between mb-2">
              <span class="text-sm font-medium text-gray-400">Storage Capacity</span>
              <span class="text-sm font-medium">{{ stats.disk }}%</span>
            </div>
            <div class="w-full bg-white/10 rounded-full h-1.5">
              <div class="bg-green-500 h-1.5 rounded-full transition-all duration-500 shadow-[0_0_8px_rgba(34,197,94,0.5)]" :style="{ width: stats.disk + '%' }"></div>
            </div>
          </div>
          <div class="pt-4 border-t border-white/5 space-y-4">
            <div class="flex justify-between items-center">
              <span class="text-sm font-medium text-gray-400">Server Uptime</span>
              <span class="text-sm font-mono text-blue-400">{{ stats.uptime || '0:00:00' }}</span>
            </div>
            <div v-if="stats.vpn && Object.keys(stats.vpn).length > 0" class="space-y-2">
              <h3 class="text-[10px] font-bold uppercase text-gray-600 tracking-widest">Active Tunnels</h3>
              <div v-for="(net, iface) in stats.vpn" :key="iface" class="flex items-center justify-between bg-white/5 p-2 rounded-lg border border-white/5">
                <span class="text-xs font-mono text-blue-300">{{ iface }}</span>
                <span class="text-[10px] text-green-500 font-bold">ONLINE</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Activity Tracker -->
      <section class="md:col-span-3 space-y-6">
        <h2 class="text-sm font-bold uppercase tracking-widest text-gray-500 px-2">Current Activities</h2>
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Pending Activity -->
          <div class="space-y-4" :class="{ 'update-flash': isUpdating }">
            <div class="flex items-center justify-between px-2 border-b border-white/5 pb-2">
              <h3 class="text-xs font-bold text-gray-500 uppercase">Pending</h3>
              <span class="text-xs bg-white/10 px-2 py-0.5 rounded-full text-gray-400 font-mono">{{ tasks.filter(t => t.status === 'Pending').length }}</span>
            </div>
            <div v-for="task in tasks.filter(t => t.status === 'Pending')" :key="task.id" 
                 class="glass rounded-xl p-4 border border-white/5 group hover:border-white/20 transition-all flex flex-col gap-2 relative">
              <span class="absolute top-2 right-2 text-[8px] font-mono text-gray-700">#{{ task.id }}</span>
              <h4 class="text-sm font-medium text-gray-200">{{ task.title }}</h4>
              <p class="text-xs text-gray-500 leading-relaxed">{{ task.description }}</p>
              <div class="flex items-center mt-1">
                <span class="text-[10px] text-gray-600 font-mono uppercase tracking-tighter">Updated: {{ formatDate(task.last_updated) }}</span>
              </div>
            </div>
          </div>

          <!-- Active Processes -->
          <div class="space-y-4" :class="{ 'update-flash': isUpdating }">
            <div class="flex items-center justify-between px-2 border-b border-blue-500/20 pb-2">
              <h3 class="text-xs font-bold text-blue-400 uppercase">Active</h3>
              <span class="text-xs bg-blue-500/20 px-2 py-0.5 rounded-full text-blue-400 font-mono">{{ tasks.filter(t => t.status === 'Active').length }}</span>
            </div>
            <div v-for="task in tasks.filter(t => t.status === 'Active')" :key="task.id" 
                 class="glass rounded-xl p-4 border border-blue-500/30 shadow-[0_0_15px_rgba(59,130,246,0.1)] group hover:bg-blue-500/5 transition-all flex flex-col gap-2 relative">
              <span class="absolute top-2 right-2 text-[8px] font-mono text-blue-900/50">#{{ task.id }}</span>
              <h4 class="font-semibold text-sm text-blue-50">{{ task.title }}</h4>
              <p class="text-xs text-blue-200/60 leading-relaxed">{{ task.description }}</p>
              <div class="pt-1">
                <div class="w-full bg-blue-900/30 rounded-full h-1">
                  <div class="bg-blue-400 h-1 rounded-full w-2/3 animate-[pulse_2s_infinite]"></div>
                </div>
              </div>
              <div class="flex items-center mt-1">
                <span class="text-[10px] text-blue-400/50 font-mono uppercase tracking-tighter">Live Since: {{ formatDate(task.last_updated) }}</span>
              </div>
            </div>
          </div>

          <!-- Completed Logs -->
          <div class="space-y-4" :class="{ 'update-flash': isUpdating }">
            <div class="flex items-center justify-between px-2 border-b border-green-500/20 pb-2">
              <h3 class="text-xs font-bold text-green-500/70 uppercase">Completed</h3>
              <span class="text-xs bg-green-500/10 px-2 py-0.5 rounded-full text-green-500/50 font-mono">{{ tasks.filter(t => t.status === 'Completed').length }}</span>
            </div>
            <div v-for="task in tasks.filter(t => t.status === 'Completed')" :key="task.id" 
                 class="glass rounded-xl p-4 border border-white/5 opacity-50 hover:opacity-100 transition-all flex flex-col gap-2 relative">
              <span class="absolute top-2 right-2 text-[8px] font-mono text-gray-800">#{{ task.id }}</span>
              <h4 class="text-sm text-gray-300 flex items-center font-medium">
                <span class="mr-2 text-green-500/50 text-xs">✓</span>
                {{ task.title }}
              </h4>
              <p class="text-xs text-gray-500 leading-relaxed">{{ task.description }}</p>
              <div class="flex items-center mt-1">
                <span class="text-[10px] text-green-900 font-mono uppercase tracking-tighter">Logged: {{ formatDate(task.last_updated) }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Token Usage Monitor -->
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

                <!-- Daily Chart (Simple CSS Bars) -->
                <div class="space-y-4">
                    <h3 class="text-xs font-bold text-gray-400 uppercase">Last 7 Days</h3>
                    <div class="flex items-end space-x-2 h-32 border-b border-white/10 pb-2">
                        <div v-for="day in tokenDaily" :key="day.date" class="flex-1 flex flex-col items-center group relative h-full justify-end">
                             <!-- Tooltip -->
                             <span class="absolute -top-8 bg-black text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap z-10 border border-white/20">
                                {{ day.tokens.toLocaleString() }} tokens
                             </span>
                             <div class="w-full bg-blue-500/50 hover:bg-blue-400 rounded-t transition-all" 
                                  :style="{ height: Math.max((day.tokens / (Math.max(...tokenDaily.map(d => d.tokens)) || 1)) * 100, 5) + '%' }"></div>
                             <span class="text-[10px] text-gray-600 mt-1 font-mono truncate w-full text-center">{{ day.date.slice(5) }}</span>
                        </div>
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
    </main>
  </div>
</template>

<style scoped>
.glass {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.update-flash {
  animation: flash-border 1s ease-out;
}

@keyframes flash-border {
  0% { border-color: rgba(59, 130, 246, 0.5); box-shadow: 0 0 15px rgba(59, 130, 246, 0.2); }
  100% { border-color: rgba(255, 255, 255, 0.05); box-shadow: none; }
}
</style>
