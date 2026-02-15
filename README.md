# 🤖 BMO Status Monitor v3

## Přehled projektu
BMO Status Monitor v3 je inteligentní řídicí centrum navržené pro real-time vizualizaci vnitřního stavu BMO, aktivních procesů a celkového zdraví systému. Hlavním účelem této aplikace je poskytnout lidskému operátorovi (Vít Parma) absolutní transparentnost ohledně toho, na čem BMO právě pracuje, co plánuje a co již bylo dokončeno.

## 🎯 Hlavní cíle
- **Operační transparentnost:** Okamžitý přehled o frontě úkolů a aktivitách BMO.
- **Monitorování systému:** Živá telemetrie hostitelského Ubuntu serveru (CPU, RAM, Disk).
- **Proaktivní komunikace:** Přímé rozhraní pro kontextové rady, vtipy a systémová upozornění od BMO.

## 🛠 Technický stack
- **Backend:** Flask (Python) s využitím knihovny `psutil` pro sběr systémových dat.
- **Frontend:** Vue.js 3 + Tailwind CSS pro moderní a reaktivní uživatelské rozhraní.
- **Design:** Apple-style minimalismus s využitím efektu Glassmorphismu a plnohodnotného Dark Mode.
- **Synchronizace:** Real-time aktualizace pomocí API pollingu (v plánu přechod na WebSockety).

## ✨ Funkce a moduly
- **Vizualizace aktivit:** Třísloupcové rozvržení (Trello-style) rozdělující práci na:
  - 📥 **Pending** (Plánované aktivity)
  - ⚙️ **Active** (Právě probíhající procesy s pulzujícím indikátorem)
  - ✅ **Completed** (Dokončené milníky)
- **Karty aktivit:** Každá karta obsahuje nadpis, stručný popis technického stavu a čas poslední aktualizace.
- **Health Dashboard:** Dynamické ukazatele vytížení hardwarových prostředků serveru.
- **"BMO Says" Widget:** Interaktivní bublina pro přímé zprávy od BMO operátorovi.

## 🚀 Stav implementace
- **Fáze 1 (The Face):** Základní UI kostra, layout a integrace API. [DOKONČENO]
- **Fáze 2 (The Heart):** Perzistence dat, refaktorizace logiky a pokročilá telemetrie. [V REALIZACI]
- **Fáze 3 (The Brain):** Automatické aktualizace stavu na základě git logů a systémových událostí. [PLÁNOVÁNO]

---
*Vytvořeno s hrdostí systémem BMO pro Víta Parmu. 🕹️🪛*
