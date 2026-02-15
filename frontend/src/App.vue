<script setup>
import { ref, onMounted } from 'vue'

const tasks = ref([])
const stats = ref({ cpu: 0, ram: 0, disk: 0 })
const bmoMessage = ref('')

const fetchTasks = async () => {
  try {
    const res = await fetch('/api/tasks')
    tasks.value = await res.json()
  } catch (e) {
    console.error('Failed to fetch tasks', e)
  }
}

const fetchStats = async () => {
  try {
    const res = await fetch('/api/stats')
    stats.value = await res.json()
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

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return dateString // Fallback to raw string if invalid
  const pad = (num) => String(num).padStart(2, '0')
  const yyyy = date.getFullYear()
  const mm = pad(date.getMonth() + 1)
  const dd = pad(date.getDate())
  const hh = pad(date.getHours())
  const min = pad(date.getMinutes())
  return `${yyyy}-${mm}-${dd} ${hh}:${min}`
}

onMounted(() => {
  fetchTasks()
  fetchStats()
  fetchBmoSays()
  setInterval(fetchStats, 5000)
})
</script>

<template>
  <div class="min-h-screen bg-black text-white p-6 font-sans">
    <!-- Header / BMO Activity Status -->
    <header class="mb-10">
      <div class="glass rounded-2xl p-6 flex items-center space-x-4">
        <div class="text-4xl">🤖</div>
        <div>
          <h1 class="text-xl font-semibold">BMO Status Monitor</h1>
          <p class="text-gray-400 italic">"{{ bmoMessage || 'Initializing BMO internal systems...' }}"</p>
        </div>
      </div>
    </header>

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
        </div>
      </section>

      <!-- Activity Tracker -->
      <section class="md:col-span-3 space-y-6">
        <h2 class="text-sm font-bold uppercase tracking-widest text-gray-500 px-2">Current Activities</h2>
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- Pending Activity -->
          <div class="space-y-4">
            <div class="flex items-center justify-between px-2 border-b border-white/5 pb-2">
              <h3 class="text-xs font-bold text-gray-500 uppercase">Pending</h3>
              <span class="text-xs bg-white/10 px-2 py-0.5 rounded-full text-gray-400 font-mono">{{ tasks.filter(t => t.status === 'ToDo').length }}</span>
            </div>
            <div v-for="task in tasks.filter(t => t.status === 'ToDo')" :key="task.id" 
                 class="glass rounded-xl p-4 border border-white/5 group hover:border-white/20 transition-all flex flex-col gap-2">
              <h4 class="text-sm font-medium text-gray-200">{{ task.title }}</h4>
              <p class="text-xs text-gray-500 leading-relaxed">{{ task.description }}</p>
              <div class="flex items-center mt-1">
                <span class="text-[10px] text-gray-600 font-mono uppercase tracking-tighter">Updated: {{ formatDate(task.last_updated) }}</span>
              </div>
            </div>
          </div>

          <!-- Active Processes -->
          <div class="space-y-4">
            <div class="flex items-center justify-between px-2 border-b border-blue-500/20 pb-2">
              <h3 class="text-xs font-bold text-blue-400 uppercase">Active</h3>
              <span class="text-xs bg-blue-500/20 px-2 py-0.5 rounded-full text-blue-400 font-mono">{{ tasks.filter(t => t.status === 'In Progress').length }}</span>
            </div>
            <div v-for="task in tasks.filter(t => t.status === 'In Progress')" :key="task.id" 
                 class="glass rounded-xl p-4 border border-blue-500/30 shadow-[0_0_15px_rgba(59,130,246,0.1)] group hover:bg-blue-500/5 transition-all flex flex-col gap-2">
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
          <div class="space-y-4">
            <div class="flex items-center justify-between px-2 border-b border-green-500/20 pb-2">
              <h3 class="text-xs font-bold text-green-500/70 uppercase">Completed</h3>
              <span class="text-xs bg-green-500/10 px-2 py-0.5 rounded-full text-green-500/50 font-mono">{{ tasks.filter(t => t.status === 'Done').length }}</span>
            </div>
            <div v-for="task in tasks.filter(t => t.status === 'Done')" :key="task.id" 
                 class="glass rounded-xl p-4 border border-white/5 opacity-50 hover:opacity-100 transition-all flex flex-col gap-2">
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
</style>
