# FOMO Crypto Intelligence Terminal - PRD

## Project Overview
Крипто-интеллектуальный терминал с real-time новостной агрегацией, AI-powered sentiment анализом, detection of confidence/rumor, и расширенной визуализацией.

## Architecture
- **Backend**: FastAPI + MongoDB + Python 3.11
- **Frontend**: React + Tailwind CSS + Radix UI  
- **Database**: MongoDB (fomo_market)
- **Scheduler**: APScheduler AsyncIOScheduler
- **Real-time**: WebSocket (5 channels + sentiment/investment alerts)

## Final Session Updates (2026-03-08)

### UI Improvements - Status Cards
- ✅ **Detailed status messages** on Discovery cards
- ✅ Shows **reason for offline/timeout/degraded** status
- ✅ Example messages:
  - "Rate limited - too many requests"
  - "Connection timeout after 10s - server too slow"
  - "Access denied (HTTP 403) - blocked by server"
  - "Endpoint not found - API may have changed"
  - "API key required for access"
  - "RSS feed working"
  - "Web parser ready"

### Health Check System
- **34 data sources** with detailed health checks
- Shows: status, message, HTTP code, response time
- Statuses: Active, Key Required, Offline, Timeout, Error, Degraded
- Parallel checking (10 sources per batch)

### Data Sources Status After Health Check
**Active (14)**:
- DefiLlama, L2BEAT, growthepie, Artemis
- DEXScreener, GeckoTerminal
- Cointelegraph, The Block, CoinDesk, Incrypted (RSS)
- ICO Drops, DropsEarn (web parsers)

**Needs API Key (3)**:
- CoinGecko (rate limited on free tier)
- CoinMarketCap
- Messari

**Degraded/Offline (17)**:
- Various reasons: API changed, auth required, rate limits

### Bootstrap Configuration
- Auto-runs on startup
- Seeds: 137 API docs, 120 news sources, 34 data sources
- Builds: Knowledge Graph (281 nodes, 499 edges)
- Creates: Entity aliases (110+)

## Implementation Details

### Health Check Messages Format
```python
# Success statuses
"Working correctly"
"RSS feed working"
"Web parser ready"

# Warning statuses
"API key required for access"
"Rate limited - too many requests"
"Authentication required (unexpected)"

# Error statuses
"Connection timeout after {n}s - server too slow"
"Access denied (HTTP 403) - blocked by server"
"Endpoint not found (HTTP 404) - API may have changed"
"Server error (HTTP 500) - source is down"
```

### Files Modified
- `/app/backend/modules/discovery_engine/health_check.py` - Detailed health checks
- `/app/frontend/src/App.js` - UI cards with status reasons
- `/app/backend/bootstrap.py` - Updated DATA_SOURCES_DATA

## Test Results
- Backend: 84.6%
- Frontend: 85%
- **Overall: 85.7%**

---
Updated: 2026-03-08
