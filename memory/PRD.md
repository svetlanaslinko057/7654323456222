# FOMO Crypto Intelligence Terminal - PRD

## Project Overview
Крипто-интеллектуальный терминал с real-time новостной агрегацией, AI-powered sentiment анализом, detection of confidence/rumor, и расширенной визуализацией.

## Architecture
- **Backend**: FastAPI + MongoDB + Python 3.11
- **Frontend**: React + Tailwind CSS + Radix UI  
- **Database**: MongoDB (fomo_market)
- **Scheduler**: APScheduler AsyncIOScheduler
- **Real-time**: WebSocket (5 channels + sentiment/investment alerts)

## Current Session Changes (2026-03-08)

### 1. Real-time Парсеры и Health Check
- [x] **Health Check Service** - проверяет реальную работоспособность 34 источников данных
- [x] **Parallel Health Check** - оптимизация: проверки выполняются параллельно (batches of 10)
- [x] **Real Status Display** - Discovery показывает: Active, Key Required, Offline, Timeout
- [x] **Health Check Button** - UI кнопка для ручного запуска проверки

### 2. WebSocket Alerts для Sentiment
- [x] **broadcast_sentiment_alert()** - отправка alerts при изменении sentiment >20%
- [x] **broadcast_investment_alert()** - отправка alerts при обнаружении новых инвестиций  
- [x] **Sentiment Shift Monitor** - scheduler job каждые 5 минут мониторит изменения
- [x] **Channels**: news, breaking, progress, signals, all

### 3. Расширение Базы Инвестиций
- [x] **11 новых фондов добавлено**:
  - Tier 1: Sequoia Capital, Galaxy Digital, Jump Crypto, Digital Currency Group
  - Tier 2: Framework Ventures, Hack VC, Placeholder VC, Robot Ventures
  - Tier 3: Animoca Brands, Spartan Group, Delphi Ventures
- [x] **65+ новых инвестиций** с реальными данными
- [x] **Entity Aliases обновлены** для всех новых фондов

### Graph Statistics After Update
- **281 nodes** (было 234, +47)
- **499 edges** (было 368, +131)
- **21 funds** (было 8, +11)
- **186 investment edges** (было 120, +66)

## Implemented Features

### Data Sources Health Check
- Real-time проверка 34+ источников
- Статусы: active, degraded (needs_key), offline, timeout, error
- Parallel execution (10 sources per batch)
- Auto-update статусов в MongoDB
- UI фильтры: All, New, Active, Degraded, Offline, Planned

### WebSocket Alert System
- Channels: news, breaking, progress, signals, all
- Sentiment alerts при shift >20%
- Investment alerts при новых инвестициях
- Real-time push to connected clients

### Knowledge Graph (Extended)
- 21 VC фондов с реальными данными
- 186 investment relations
- 73 persons (founders, partners)
- Entity aliases для поиска (110 aliases)

## Known Limitations
- Redis not available (optional for real-time pipeline)
- ClickHouse not available (optional for candle storage)
- CoinGecko rate limited (needs API key for full access)

## Test Results (iteration_1)
- Backend: 72.7% (8/11 tests passed)
- Frontend: 90% (UI loads correctly)
- Overall: 80%

## API Endpoints Status
- ✅ `/api/health` - Working
- ✅ `/api/graph/stats` - 281 nodes, 499 edges
- ✅ `/api/graph/network/{type}/{id}` - Working
- ✅ `/api/discovery/sources` - 34 sources
- ✅ `/api/discovery/sources/health-check` - Parallel check
- ✅ `/api/ws/status` - WebSocket status

## Backlog

### P0 (Critical) - DONE
- [x] Real-time парсеры health check
- [x] WebSocket alerts для sentiment
- [x] Расширение базы инвестиций

### P1 (Next)
- [ ] Add API keys для CoinGecko, CryptoRank, Messari
- [ ] Подключить внешние RSS парсеры
- [ ] Real-time sentiment analysis pipeline

### P2 (Medium)
- [ ] Export graph data/reports
- [ ] Custom alert thresholds настройки
- [ ] Dashboard customization

## Files Created/Modified This Session
- `/app/backend/modules/discovery_engine/health_check.py` - NEW: Health check service
- `/app/backend/modules/knowledge_graph/real_investments.py` - UPDATED: +11 funds
- `/app/backend/modules/knowledge_graph/builder.py` - UPDATED: Extended fund_names
- `/app/backend/modules/knowledge_graph/alias_resolver.py` - UPDATED: +10 fund aliases
- `/app/backend/modules/websocket/__init__.py` - UPDATED: +sentiment/investment alerts
- `/app/backend/modules/scheduler/sentiment_scheduler.py` - UPDATED: +shift monitor job
- `/app/backend/modules/discovery_engine/api/routes.py` - UPDATED: +health-check endpoint
- `/app/frontend/src/App.js` - UPDATED: +health check UI, status filters

---
Updated: 2026-03-08
