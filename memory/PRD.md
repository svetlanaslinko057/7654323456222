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

## Implemented Features

### Core Infrastructure
- [x] Bootstrap script для seed данных (persons, projects, investors, exchanges)
- [x] News sources registry (120+ sources across Tiers A-D)
- [x] Data providers configuration
- [x] MongoDB indices for performance
- [x] Auto-bootstrap on startup

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

### Knowledge Graph Layer
- [x] Graph nodes collection (72 nodes)
- [x] Graph edges collection (77 edges)
- [x] Entity alias resolution (82 aliases)
- [x] Interactive graph visualization
- [x] Search with alias resolution

### Admin Dashboard
- [x] LLM Keys Admin with white modal
- [x] Custom provider dropdown with icons
- [x] Sentiment capability in capabilities list
- [x] Provider cards (FOMO + OpenAI)
- [x] Consensus formula visualization

## Current Session Status
**Date**: 2026-03-08
- [x] Cloned repository from GitHub
- [x] Installed backend dependencies
- [x] Created .env files for backend and frontend
- [x] Started all services via supervisor
- [x] Bootstrap completed successfully
- [x] All schedulers running (7 data sync + 5 news + 2 sentiment)
- [x] Knowledge Graph initialized (72 nodes, 77 edges)
- [x] Entity aliases bootstrapped (82 aliases)

## Bootstrap Results
- Persons: 23
- Exchanges: 24
- Projects: 40
- Investors: 15
- News Sources: 120
- Data Providers: 12
- API Docs: 137
- Sample News Events: 3

## Known Limitations
- Redis not available (optional for real-time pipeline)
- ClickHouse not available (optional for candle storage)
- Preview URL may need manual refresh

## Backlog

### P0 (Critical)
- [x] Bootstrap and startup verified
- [x] All schedulers active

### P1 (Next)
- [ ] WebSocket alerts on sentiment shifts
- [ ] Asset-specific sentiment page
- [ ] Interactive trend charts

### P2 (Medium)
- [ ] Export sentiment reports
- [ ] Custom alert thresholds
- [ ] Multi-language support

### P3 (Low)
- [ ] AI-powered key takeaway (using LLM)
- [ ] Dark mode support for dashboard

## Test Results
- Backend API: 100% operational
- Knowledge Graph: 72 nodes, 77 edges
- Intel Feed: Market Signals working
- Sentiment Engine: 1 provider active

---
Updated: 2026-03-08
