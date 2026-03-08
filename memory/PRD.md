# FOMO Crypto Intelligence Terminal - PRD

## Project Overview
Крипто-интеллектуальный терминал с real-time новостной агрегацией, AI-powered sentiment анализом, detection of confidence/rumor, и расширенной визуализацией.

## Architecture
- **Backend**: FastAPI + MongoDB + Python 3.11
- **Frontend**: React + Tailwind CSS + Radix UI  
- **Sentiment**: Multi-provider (FOMO Custom, OpenAI GPT-4o)
- **Database**: MongoDB (fomo_market)
- **Scheduler**: APScheduler AsyncIOScheduler
- **Real-time**: WebSocket (5 channels)

## Technology Stack
- Backend: FastAPI 0.110.1, Motor (MongoDB async), APScheduler
- Frontend: React 19, Tailwind CSS, Radix UI components
- Data: MongoDB, Redis (optional), ClickHouse (optional)
- Schedulers: 7 data sync jobs, 5 news intelligence jobs, 2 sentiment jobs

## Current Session Changes (2026-03-08)

### Graph System Improvements
- [x] **Added REAL investment data** for major VC funds:
  - a16z Crypto: 30+ investments with real amounts
  - Paradigm: 19 investments
  - Coinbase Ventures: 13 investments
  - Binance Labs: 11 investments
  - Polychain Capital: 9 investments
  - Pantera Capital: 10 investments
  - Dragonfly Capital: 8 investments
  - Multicoin Capital: 8 investments

- [x] **Added project team members** (founders/team):
  - Ethereum: Vitalik Buterin, Gavin Wood, Joseph Lubin
  - Solana: Anatoly Yakovenko, Raj Gokal
  - Polygon: Sandeep Nailwal, Jaynti Kanani, Anurag Arjun
  - 15+ other projects with real team data

- [x] **Added fund team members** (partners):
  - a16z: Marc Andreessen, Ben Horowitz, Chris Dixon, Arianna Simpson
  - Paradigm: Matt Huang, Fred Ehrsam, Dan Robinson
  - 6 other funds with partner data

- [x] **Fixed edge deduplication** - multiple investments now show as multiple edges

### Graph Statistics After Update
- **234 nodes** (was 72)
- **368 edges** (was 77)
- Nodes by type: 11 funds, 89 projects, 57 persons, 44 tokens, 23 assets, 10 exchanges
- Edges by type: 120 invested_in, 69 traded_on, 63 has_token, 36 founded, 32 coinvested_with, 24 works_at

## Implemented Features

### Core Infrastructure
- [x] Bootstrap script для seed данных (persons, projects, investors, exchanges)
- [x] News sources registry (120+ sources across Tiers A-D)
- [x] Data providers configuration
- [x] MongoDB indices for performance
- [x] Auto-bootstrap on startup

### Knowledge Graph Layer (UPDATED)
- [x] Real investment data from 8 major VC funds
- [x] Project team members (founders, CTOs)
- [x] Fund team members (partners)
- [x] Entity alias resolution (82+ aliases)
- [x] Interactive graph visualization with ForceGraph
- [x] Search with autocomplete
- [x] **Multiple edges for multiple investments** (1 investment = 1 line)

### Data Sync Schedulers
- [x] CoinGecko Market Data (5 min)
- [x] DefiLlama TVL (15 min)
- [x] Crypto Activities (15 min)
- [x] CryptoRank Funding (30 min)
- [x] Messari Metrics (60 min)
- [x] Exchange Instruments (60 min)
- [x] Token Unlocks (6 hours)

### News Intelligence Layer
- [x] Raw articles collection
- [x] Normalized articles processing
- [x] Event detection engine
- [x] Feed ranking with importance scoring
- [x] Story collapse/deduplication

### Sentiment Engine
- [x] FOMO Custom Provider (keyword-based)
- [x] OpenAI GPT-4o Provider integration
- [x] Consensus mechanism (weighted average)
- [x] Sentiment cache in MongoDB (7-day TTL)
- [x] Auto-analyze scheduler (2 min intervals)

## Known Limitations
- Redis not available (optional for real-time pipeline)
- ClickHouse not available (optional for candle storage)
- Real-time data parsing requires external API keys

## Backlog

### P0 (Critical) - DONE
- [x] Graph shows real investment data
- [x] Multiple investment rounds = multiple lines
- [x] Entity search working

### P1 (Next)
- [ ] Real-time parser for external data sources
- [ ] WebSocket alerts on sentiment shifts
- [ ] Asset-specific sentiment page
- [ ] Interactive trend charts

### P2 (Medium)
- [ ] Export graph data/reports
- [ ] Custom alert thresholds
- [ ] Multi-language support

### P3 (Low)
- [ ] AI-powered key takeaway
- [ ] Dark mode toggle

## Files Modified This Session
- `/app/backend/modules/knowledge_graph/real_investments.py` - NEW: Real investment data
- `/app/backend/modules/knowledge_graph/builder.py` - Updated to use real data
- `/app/backend/modules/knowledge_graph/query_service.py` - Fixed edge deduplication
- `/app/frontend/src/components/ForceGraphViewer.js` - Fixed line multiplier logic

---
Updated: 2026-03-08
