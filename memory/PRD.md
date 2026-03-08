# FOMO Crypto Intelligence Terminal - PRD

## Project Overview
Крипто-интеллектуальный терминал с real-time новостной агрегацией, AI-powered sentiment анализом, detection of confidence/rumor, и расширенной визуализацией.

## Architecture
- **Backend**: FastAPI + MongoDB + Python 3.11
- **Frontend**: React + Tailwind CSS + Radix UI  
- **Database**: MongoDB (fomo_market)
- **Scheduler**: APScheduler AsyncIOScheduler
- **Real-time**: WebSocket (5 channels + sentiment/investment alerts)

## Final Session Changes (2026-03-08)

### 1. All Data Sources Activated
- **34 data sources** total
  - **31 Active** - полностью функциональны
  - **3 Needs Key** - CoinGecko, CoinMarketCap, Messari (только эти требуют API ключи)

### 2. All 120 News Sources Active
- **Tier A**: 15 primary sources (Cointelegraph, The Block, Decrypt, etc.)
- **Tier B**: 35 secondary sources
- **Tier C**: 40 research sources
- **Tier D**: 30 aggregators
- **Languages**: EN 101, ZH 8, RU 7, JP 2, UA 1, DE 1
- **Categories**: News 48, Official 21, Research 18, Analytics 7, Security 5, DeFi 4

### 3. Real-time Sentiment Pipeline
- **Sentiment Shift Monitor** - scheduler job каждые 5 минут
- **WebSocket alerts** - broadcast при sentiment change >20%
- **Investment alerts** - broadcast при обнаружении новых инвестиций
- **Health monitor** для всех news sources с health_score tracking

### 4. Knowledge Graph Extended
- **21 VC funds** с реальными данными
- **281 nodes** total
- **499 edges** total
- **186 investment edges**
- **110+ entity aliases** для поиска

### 5. Bootstrap Updated
- Unified bootstrap module
- Auto-initialization on startup
- 137 API docs seeded
- Entity aliases bootstrapped
- Knowledge Graph auto-rebuilt

## Implemented Features

### Data Sources (34 total)
- ✅ Market Data: DefiLlama, Token Terminal, DEXScreener, GeckoTerminal, DEXTools
- ✅ Intel/Funding: CryptoRank, Dropstab, RootData, Crunchbase
- ✅ Token Unlocks: TokenUnlocks, VestLab
- ✅ Derivatives: Coinglass, Laevitas, Velo Data
- ✅ On-chain: Nansen, Arkham, Dune, Glassnode, Santiment
- ✅ L2: L2BEAT, growthepie, Artemis
- ✅ Activities: ICO Drops, DappRadar, DropsEarn, AirdropAlert
- ✅ News RSS: Cointelegraph, The Block, CoinDesk, Incrypted
- ⚠️ Needs Key: CoinGecko, CoinMarketCap, Messari

### News Intelligence
- ✅ 120 news sources active
- ✅ RSS parsing with health tracking
- ✅ Multi-language support (EN, ZH, RU, JP, UA, DE)
- ✅ Category filtering (news, official, research, analytics, security, defi)
- ✅ Real-time health monitoring

### WebSocket Alerts
- ✅ 5 channels: news, breaking, progress, signals, all
- ✅ Sentiment shift alerts (>20% change)
- ✅ Investment detection alerts
- ✅ Real-time broadcast to connected clients

### Knowledge Graph
- ✅ 21 VC funds with real investment data
- ✅ 186 investment relations
- ✅ 73 persons (founders, partners)
- ✅ 110+ entity aliases for search
- ✅ Interactive visualization

## Test Results
- Backend: 84.6% (11/13 API tests passed)
- Frontend: 85% (UI loads correctly)
- Key Requirements: 87.5% (7/8 met)
- **Overall: 85.7%**

## Known Limitations
- Redis not available (optional for real-time pipeline)
- ClickHouse not available (optional for candle storage)
- 3 sources require API keys: CoinGecko, CoinMarketCap, Messari

## API Stats
- **137 API docs** seeded
- **34 data sources** configured
- **120 news sources** active
- **281 graph nodes**
- **499 graph edges**

## Files Modified This Session
- `/app/backend/bootstrap.py` - Updated DATA_SOURCES_DATA with correct statuses
- `/app/backend/modules/discovery_engine/health_check.py` - Parallel health check
- `/app/backend/modules/news_intelligence/api/routes.py` - Fixed sources-registry endpoint
- `/app/backend/modules/websocket/__init__.py` - Added sentiment/investment alerts
- `/app/backend/modules/scheduler/sentiment_scheduler.py` - Added shift monitor
- `/app/backend/modules/knowledge_graph/real_investments.py` - 11 new VC funds
- `/app/frontend/src/App.js` - Fixed News Sources page API endpoint

---
Updated: 2026-03-08
