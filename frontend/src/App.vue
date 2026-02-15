<script setup>
import { ref, onMounted } from 'vue'

const tasks = ref([])
const stats = ref({ cpu: 0, ram: 0, disk: 0 })
const bmoMessage = ref('')

const fetchTasks = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/tasks')
    tasks.value = await res.json()
  } catch (e) {
    console.error('Failed to fetch tasks', e)
  }
}

const fetchStats = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/stats')
    stats.value = await res.json()
  } catch (e) {
    console.error('Failed to fetch stats', e)
  }
}

const fetchBmoSays = async () => {
  try {
    const res = await fetch('http://localhost:5000/api/bmo-says')
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

    <main class="grid grid-cols-1 md:grid-cols-3 gap-6">
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

      <!-- Task List -->
      <section class="md:col-span-2 space-y-6">
        <h2 class="text-sm font-bold uppercase tracking-widest text-gray-500 px-2">Mission Control</h2>
        <div class="grid grid-cols-1 gap-4">
          <div v-for="task in tasks" :key="task.id" class="glass rounded-2xl p-4 flex items-center justify-between group hover:bg-white/5 transition-colors">
            <div class="flex items-center space-x-4">
              <div :class="['w-2 h-10 rounded-full', 
                task.status === 'Done' ? 'bg-green-500' : 
                task.status === 'In Progress' ? 'bg-apple-blue' : 'bg-gray-600']"></div>
              <div>
                <h3 class="font-medium">{{ task.title }}</h3>
                <div class="flex items-center space-x-2 text-xs text-gray-500">
                  <span :class="getPriorityColor(task.priority)">{{ task.priority }}</span>
                  <span>•</span>
                  <span>{{ task.project }}</span>
                </div>
              </div>
            </div>
            <div class="text-xs font-semibold px-3 py-1 rounded-full bg-white/10 uppercase">
              {{ task.status }}
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
</style>
