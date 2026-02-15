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

onMounted(() => {
  fetchTasks()
  fetchStats()
  fetchBmoSays()
  setInterval(fetchStats, 5000)
})

const getPriorityColor = (priority) => {
  switch (priority) {
    case 'CRITICAL': return 'text-red-500'
    case 'HIGH': return 'text-orange-500'
    case 'NORMAL': return 'text-blue-500'
    default: return 'text-gray-400'
  }
}
</script>

<template>
  <div class="min-h-screen bg-black text-white p-6 font-sans">
    <!-- Header / BMO Says -->
    <header class="mb-10">
      <div class="glass rounded-2xl p-6 flex items-center space-x-4">
        <div class="text-4xl">🕹️</div>
        <div>
          <h1 class="text-xl font-semibold">BMO Dashboard v3</h1>
          <p class="text-gray-400 italic">"{{ bmoMessage }}"</p>
        </div>
      </div>
    </header>

    <main class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <!-- System Stats -->
      <section class="md:col-span-1 space-y-6">
        <h2 class="text-sm font-bold uppercase tracking-widest text-gray-500 px-2">System Health</h2>
        <div class="glass rounded-3xl p-6 space-y-6">
          <div>
            <div class="flex justify-between mb-2">
              <span class="text-sm font-medium">CPU Usage</span>
              <span class="text-sm font-medium">{{ stats.cpu }}%</span>
            </div>
            <div class="w-full bg-white/10 rounded-full h-1.5">
              <div class="bg-apple-blue h-1.5 rounded-full transition-all duration-500" :style="{ width: stats.cpu + '%' }"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between mb-2">
              <span class="text-sm font-medium">RAM Usage</span>
              <span class="text-sm font-medium">{{ stats.ram }}%</span>
            </div>
            <div class="w-full bg-white/10 rounded-full h-1.5">
              <div class="bg-purple-500 h-1.5 rounded-full transition-all duration-500" :style="{ width: stats.ram + '%' }"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between mb-2">
              <span class="text-sm font-medium">Disk Space</span>
              <span class="text-sm font-medium">{{ stats.disk }}%</span>
            </div>
            <div class="w-full bg-white/10 rounded-full h-1.5">
              <div class="bg-green-500 h-1.5 rounded-full transition-all duration-500" :style="{ width: stats.disk + '%' }"></div>
            </div>
          </div>
        </div>
      </section>

      <!-- Mission Control -->
      <section class="md:col-span-3 space-y-6">
        <h2 class="text-sm font-bold uppercase tracking-widest text-gray-500 px-2">Mission Control</h2>
        
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <!-- ToDo Column -->
          <div class="space-y-4">
            <div class="flex items-center justify-between px-2">
              <h3 class="text-xs font-bold text-gray-500 uppercase">To Do</h3>
              <span class="text-xs bg-white/10 px-2 py-0.5 rounded-full text-gray-400">{{ tasks.filter(t => t.status === 'ToDo').length }}</span>
            </div>
            <div v-for="task in tasks.filter(t => t.status === 'ToDo')" :key="task.id" 
                 class="glass rounded-2xl p-4 space-y-3 group hover:bg-white/5 transition-all">
              <div class="flex justify-between items-start">
                <span :class="['text-[10px] font-bold px-2 py-0.5 rounded-md bg-white/5', getPriorityColor(task.priority)]">
                  {{ task.priority }}
                </span>
                <span class="text-[10px] text-gray-500">{{ task.project }}</span>
              </div>
              <h4 class="font-medium text-sm">{{ task.title }}</h4>
            </div>
          </div>

          <!-- In Progress Column -->
          <div class="space-y-4">
            <div class="flex items-center justify-between px-2">
              <h3 class="text-xs font-bold text-apple-blue uppercase">In Progress</h3>
              <span class="text-xs bg-apple-blue/20 px-2 py-0.5 rounded-full text-apple-blue">{{ tasks.filter(t => t.status === 'In Progress').length }}</span>
            </div>
            <div v-for="task in tasks.filter(t => t.status === 'In Progress')" :key="task.id" 
                 class="glass rounded-2xl p-4 space-y-3 border-apple-blue/30 shadow-[0_0_15px_rgba(0,122,255,0.1)] group hover:bg-white/5 transition-all">
              <div class="flex justify-between items-start">
                <span :class="['text-[10px] font-bold px-2 py-0.5 rounded-md bg-white/5', getPriorityColor(task.priority)]">
                  {{ task.priority }}
                </span>
                <span class="text-[10px] text-gray-500">{{ task.project }}</span>
              </div>
              <h4 class="font-medium text-sm">{{ task.title }}</h4>
              <div class="pt-1">
                <div class="w-full bg-apple-blue/10 rounded-full h-1">
                  <div class="bg-apple-blue h-1 rounded-full w-1/2 animate-pulse"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Done Column -->
          <div class="space-y-4">
            <div class="flex items-center justify-between px-2">
              <h3 class="text-xs font-bold text-green-500/70 uppercase">Done</h3>
              <span class="text-xs bg-green-500/10 px-2 py-0.5 rounded-full text-green-500/50">{{ tasks.filter(t => t.status === 'Done').length }}</span>
            </div>
            <div v-for="task in tasks.filter(t => t.status === 'Done')" :key="task.id" 
                 class="glass rounded-2xl p-4 space-y-3 opacity-60 grayscale-[0.5] group hover:bg-white/5 transition-all">
              <div class="flex justify-between items-start">
                <span class="text-[10px] font-bold px-2 py-0.5 rounded-md bg-white/5 text-gray-500">
                  {{ task.priority }}
                </span>
                <span class="text-[10px] text-gray-500">{{ task.project }}</span>
              </div>
              <h4 class="font-medium text-sm line-through text-gray-400">{{ task.title }}</h4>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
</style>
