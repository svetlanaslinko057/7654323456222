"""
FOMO Market Data API
Unified Exchange Data Backend
"""

from fastapi import FastAPI
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
import time

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(
    title="FOMO Market Data API",
    version="2.0.0",
    description="Unified Exchange Data Backend - Binance, Bybit, Coinbase, Hyperliquid"
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# CORE ROUTES
# ═══════════════════════════════════════════════════════════════

@app.get("/api/health")
async def health():
    return {
        "ok": True,
        "service": "FOMO Market Data API",
        "version": "2.0.0",
        "ts": int(time.time() * 1000),
        "layers": {
            "market_data": ["binance", "bybit", "coinbase", "hyperliquid"],
            "asset_intel": "coming_soon"
        }
    }

@app.get("/api")
async def root():
    return {
        "service": "FOMO Market Data API",
        "version": "2.0.0",
        "docs": "/docs",
        "endpoints": {
            "market": "/api/market/*",
            "assets": "/api/assets/*",
            "exchange": "/api/exchange/*",
            "whales": "/api/whales/*",
            "unlocks": "/api/unlocks/*"
        }
    }

# ═══════════════════════════════════════════════════════════════
# REGISTER MARKET DATA MODULE (Layer 1)
# ═══════════════════════════════════════════════════════════════

from modules.market_data import (
    exchange_router,
    market_router,
    assets_router,
    whales_router,
    derivatives_router,
    redis_router,
    candles_router
)

# Register routers
app.include_router(exchange_router)
app.include_router(market_router)
app.include_router(assets_router)
app.include_router(whales_router)
app.include_router(derivatives_router)
app.include_router(redis_router)
app.include_router(candles_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER UNLOCKS MODULE (Layer 2)
# ═══════════════════════════════════════════════════════════════

from modules.unlocks import unlocks_router
app.include_router(unlocks_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER INTEL MODULE (Layer 2 - Crypto Intelligence)
# ═══════════════════════════════════════════════════════════════

from modules.intel import intel_router, admin_router, engine_router
from modules.intel.api.routes_entity import router as entity_router
from modules.intel.api.routes_docs import router as docs_router
from modules.intel.api.routes_public import router as public_router
app.include_router(intel_router)
app.include_router(admin_router)
app.include_router(engine_router)
app.include_router(entity_router)
app.include_router(docs_router)
app.include_router(public_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER NEW INTEL MODULES (Funding Feed, Funds, Persons, ICO, Projects, Indicators)
# ═══════════════════════════════════════════════════════════════

from modules.intel.api.routes_funding import router as funding_router
from modules.intel.api.routes_funds_v2 import router as funds_router
from modules.intel.api.routes_persons_v2 import router as persons_router
from modules.intel.api.routes_investors import router as investors_router
from modules.intel.api.routes_ico import router as ico_router
from modules.intel.api.routes_projects import router as projects_router
from modules.intel.api.routes_indicators import router as indicators_router
from modules.intel.api.routes_activities import router as activities_router
from modules.intel.api.routes_intel_feed import router as intel_feed_router
from modules.intel.api.routes_projects_v2 import router as projects_v2_router
from modules.intel.api.routes_sync import router as sync_router
from modules.intel.api.routes_discovery import router as discovery_router
from modules.intel.api.routes_intel_core import router as intel_core_router
from modules.intel.api.routes_api_keys import router as api_keys_router
from modules.intel.api.routes_llm_keys import router as llm_keys_router
from modules.intel.api.routes_sentiment_keys import router as sentiment_keys_router
from modules.scheduler.routes_scheduler import router as scheduler_router
from modules.intel.api.routes_onchain import router as intel_onchain_router
from modules.intel.api.routes_tokenomics import router as intel_tokenomics_router
from modules.system.routes_system import router as system_router

app.include_router(system_router)

app.include_router(funding_router)
app.include_router(funds_router)
app.include_router(persons_router)
app.include_router(investors_router)
app.include_router(ico_router)
app.include_router(projects_router)
app.include_router(indicators_router)
app.include_router(activities_router)
app.include_router(intel_feed_router)
app.include_router(projects_v2_router)
app.include_router(sync_router)
app.include_router(discovery_router)
app.include_router(intel_core_router)
app.include_router(api_keys_router)
app.include_router(llm_keys_router)
app.include_router(sentiment_keys_router)
app.include_router(scheduler_router)
app.include_router(intel_onchain_router)
app.include_router(intel_tokenomics_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER MARKET API LAYER (First Layer - Exchange/Market Data)
# ═══════════════════════════════════════════════════════════════

from modules.market_data.api.market_routes import router as market_api_router
from modules.market_data.api.derivatives_routes import router as derivatives_api_router
from modules.market_data.api.indices_routes import router as indices_api_router
from modules.market_data.api.spot_routes import router as spot_api_router
from modules.market_data.api.onchain_routes import router as onchain_api_router
from modules.market_data.api.tokenomics_routes import router as tokenomics_api_router

app.include_router(market_api_router)
app.include_router(derivatives_api_router)
app.include_router(indices_api_router)
app.include_router(spot_api_router)
app.include_router(onchain_api_router)
app.include_router(tokenomics_api_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER UNIFIED ASSET REGISTRY (Core Layer)
# ═══════════════════════════════════════════════════════════════

from modules.asset_registry import asset_router
app.include_router(asset_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER PROVIDER GATEWAY (External Data Sources)
# ═══════════════════════════════════════════════════════════════

from modules.provider_gateway import provider_router
app.include_router(provider_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER DISCOVERY ENGINE (Auto API Discovery)
# ═══════════════════════════════════════════════════════════════

from modules.discovery_engine.api import discovery_router
app.include_router(discovery_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER WEBSOCKET MODULE (Real-Time Updates)
# ═══════════════════════════════════════════════════════════════

from modules.websocket import router as websocket_router
app.include_router(websocket_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER SCRAPER ENGINE (Endpoint-based Data Fetching)
# ═══════════════════════════════════════════════════════════════

from modules.scraper_engine.api import router as scraper_router
app.include_router(scraper_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER NEWS PARSER (Crypto News Feed)
# ═══════════════════════════════════════════════════════════════

from modules.news_parser.api import news_router
app.include_router(news_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER DATA FUSION ENGINE
# ═══════════════════════════════════════════════════════════════

from modules.intel.api.routes_fusion import router as fusion_router
app.include_router(fusion_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER ALPHA FEED (Main Event Feed)
# ═══════════════════════════════════════════════════════════════

from modules.intel.api.routes_alpha import router as alpha_router
app.include_router(alpha_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER PROVIDER METRICS (Scoring System)
# ═══════════════════════════════════════════════════════════════

from modules.provider_gateway.api.routes_metrics import router as provider_metrics_router
app.include_router(provider_metrics_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER KNOWLEDGE GRAPH (Relationship Intelligence)
# ═══════════════════════════════════════════════════════════════

from modules.knowledge_graph.api.routes import router as graph_router, init_graph_services
app.include_router(graph_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER NEWS INTELLIGENCE LAYER (Event Detection Engine)
# ═══════════════════════════════════════════════════════════════

from modules.news_intelligence.api import router as news_intelligence_router, set_database as set_news_db
set_news_db(db)
app.include_router(news_intelligence_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER MARKET GATEWAY (Provider-agnostic Market Data)
# ═══════════════════════════════════════════════════════════════

from modules.market_gateway.api import router as market_gateway_router
app.include_router(market_gateway_router)

# ═══════════════════════════════════════════════════════════════
# REGISTER SENTIMENT ENGINE (Multi-Provider Analysis)
# ═══════════════════════════════════════════════════════════════

from modules.sentiment_engine.api import router as sentiment_router, set_database as set_sentiment_db
set_sentiment_db(db)
app.include_router(sentiment_router)

# ═══════════════════════════════════════════════════════════════
# CORS & MIDDLEWARE
# ═══════════════════════════════════════════════════════════════

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# STARTUP / SHUTDOWN
# ═══════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup():
    logger.info("FOMO Market Data API starting...")
    logger.info("Registered routes:")
    logger.info("  - /api/health")
    logger.info("  - /api/market/* (overview, assets)")
    logger.info("  - /api/assets/* (profile, performance, chart, venues)")
    logger.info("  - /api/exchange/* (instruments, ticker, orderbook, trades, candles)")
    logger.info("  - /api/derivatives/* (funding, open-interest, liquidations, long-short)")
    logger.info("  - /api/whales/* (snapshots, leaderboard)")
    logger.info("  - /api/candles/* (historical OHLCV from ClickHouse)")
    logger.info("  - /api/intel/* (crypto intelligence data)")
    
    # ═══════════════════════════════════════════════════════════════
    # 1. LOAD PROXIES FROM MONGODB (Persistence Layer)
    # ═══════════════════════════════════════════════════════════════
    try:
        from modules.intel.common.proxy_manager import proxy_manager
        await proxy_manager.load_from_db()
        status = proxy_manager.get_status()
        if status['total'] > 0:
            logger.info(f"✓ Loaded {status['total']} proxies from MongoDB ({status['enabled']} enabled)")
        else:
            logger.info("○ No proxies configured - exchanges will use direct connection")
    except Exception as e:
        logger.warning(f"Failed to load proxies: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 2. AUTO-BOOTSTRAP: Seed essential data if empty
    # ═══════════════════════════════════════════════════════════════
    try:
        # Check if we need to bootstrap
        persons_count = await db.intel_persons.count_documents({})
        docs_count = await db.intel_docs.count_documents({})
        
        if persons_count == 0:
            logger.info("Database empty - running auto-bootstrap...")
            # Import and run bootstrap logic
            from modules.intel.api.routes_admin import run_bootstrap
            from fastapi import Request
            class FakeDB:
                pass
            await run_bootstrap(db)
            logger.info("✓ Auto-bootstrap complete")
        else:
            logger.info(f"✓ Database has data: {persons_count} persons")
        
        # Ensure API docs are seeded
        if docs_count == 0:
            try:
                from modules.intel.api.documentation_registry import API_DOCUMENTATION
                from datetime import datetime, timezone
                now = datetime.now(timezone.utc)
                for endpoint in API_DOCUMENTATION:
                    doc = {
                        "endpoint_id": endpoint.endpoint_id,
                        "path": endpoint.path,
                        "method": endpoint.method.value,
                        "title_en": endpoint.title_en,
                        "title_ru": endpoint.title_ru,
                        "description_en": endpoint.description_en,
                        "description_ru": endpoint.description_ru,
                        "category": endpoint.category,
                        "tags": endpoint.tags,
                        "updated_at": now
                    }
                    await db.intel_docs.update_one(
                        {"endpoint_id": doc["endpoint_id"]},
                        {"$set": doc},
                        upsert=True
                    )
                logger.info(f"✓ Auto-seeded {len(API_DOCUMENTATION)} API docs")
            except Exception as e:
                logger.warning(f"Failed to seed API docs: {e}")
                
    except Exception as e:
        logger.warning(f"Auto-bootstrap failed: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 2.5. SEED DATA SOURCES REGISTRY
    # ═══════════════════════════════════════════════════════════════
    try:
        from modules.intel.data_sources_registry import DataSourcesRegistry
        sources_registry = DataSourcesRegistry(db)
        sources_count = await db.data_sources.count_documents({})
        if sources_count == 0:
            result = await sources_registry.seed_sources()
            logger.info(f"✓ Seeded {result['seeded']} data sources")
        else:
            logger.info(f"✓ Data sources registry: {sources_count} sources")
    except Exception as e:
        logger.warning(f"Failed to seed data sources: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 2.6. BOOTSTRAP PROVIDER GATEWAY
    # ═══════════════════════════════════════════════════════════════
    try:
        from modules.provider_gateway.registry import ProviderRegistry
        provider_registry = ProviderRegistry(db)
        providers_count = await db.providers.count_documents({})
        if providers_count == 0:
            result = await provider_registry.initialize_defaults()
            logger.info(f"✓ Provider Gateway: initialized {result['created']} providers")
        else:
            logger.info(f"✓ Provider Gateway: {providers_count} providers ready")
    except Exception as e:
        logger.warning(f"Failed to bootstrap Provider Gateway: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 2.7. BOOTSTRAP NEWS PARSER SOURCES
    # ═══════════════════════════════════════════════════════════════
    try:
        from modules.news_parser.parser import NewsParser
        news_parser = NewsParser(db)
        news_sources_count = await db.news_sources.count_documents({})
        if news_sources_count == 0:
            result = await news_parser.initialize_sources()
            logger.info(f"✓ News Parser: initialized {result['created']} sources")
            # Initial crawl to populate news
            crawl_result = await news_parser.crawl_all_sources()
            logger.info(f"✓ News Parser: crawled {crawl_result['total_articles_created']} articles")
        else:
            logger.info(f"✓ News Parser: {news_sources_count} sources ready")
    except Exception as e:
        logger.warning(f"Failed to bootstrap News Parser: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 2.8. BOOTSTRAP ASSET REGISTRY (Core Assets)
    # ═══════════════════════════════════════════════════════════════
    try:
        from modules.asset_registry.registry import AssetRegistry
        from modules.asset_registry.models import AssetCreate, AssetType
        asset_registry = AssetRegistry(db)
        assets_count = await db.assets.count_documents({})
        if assets_count == 0:
            # Seed core crypto assets
            CORE_ASSETS = [
                {"canonical_symbol": "BTC", "canonical_name": "Bitcoin", "asset_type": "coin"},
                {"canonical_symbol": "ETH", "canonical_name": "Ethereum", "asset_type": "coin"},
                {"canonical_symbol": "SOL", "canonical_name": "Solana", "asset_type": "coin"},
                {"canonical_symbol": "BNB", "canonical_name": "Binance Coin", "asset_type": "coin"},
                {"canonical_symbol": "XRP", "canonical_name": "Ripple", "asset_type": "coin"},
                {"canonical_symbol": "ADA", "canonical_name": "Cardano", "asset_type": "coin"},
                {"canonical_symbol": "DOGE", "canonical_name": "Dogecoin", "asset_type": "coin"},
                {"canonical_symbol": "DOT", "canonical_name": "Polkadot", "asset_type": "coin"},
                {"canonical_symbol": "AVAX", "canonical_name": "Avalanche", "asset_type": "coin"},
                {"canonical_symbol": "MATIC", "canonical_name": "Polygon", "asset_type": "token"},
                {"canonical_symbol": "LINK", "canonical_name": "Chainlink", "asset_type": "token"},
                {"canonical_symbol": "UNI", "canonical_name": "Uniswap", "asset_type": "token"},
                {"canonical_symbol": "ATOM", "canonical_name": "Cosmos", "asset_type": "coin"},
                {"canonical_symbol": "LTC", "canonical_name": "Litecoin", "asset_type": "coin"},
                {"canonical_symbol": "TRX", "canonical_name": "Tron", "asset_type": "coin"},
                {"canonical_symbol": "USDT", "canonical_name": "Tether", "asset_type": "stablecoin"},
                {"canonical_symbol": "USDC", "canonical_name": "USD Coin", "asset_type": "stablecoin"},
                {"canonical_symbol": "DAI", "canonical_name": "Dai", "asset_type": "stablecoin"},
                {"canonical_symbol": "ARB", "canonical_name": "Arbitrum", "asset_type": "token"},
                {"canonical_symbol": "OP", "canonical_name": "Optimism", "asset_type": "token"},
                {"canonical_symbol": "NEAR", "canonical_name": "NEAR Protocol", "asset_type": "coin"},
                {"canonical_symbol": "APT", "canonical_name": "Aptos", "asset_type": "coin"},
                {"canonical_symbol": "SUI", "canonical_name": "Sui", "asset_type": "coin"},
                {"canonical_symbol": "AAVE", "canonical_name": "Aave", "asset_type": "token"},
                {"canonical_symbol": "CRV", "canonical_name": "Curve", "asset_type": "token"},
            ]
            result = await asset_registry.bulk_create_assets(CORE_ASSETS)
            logger.info(f"✓ Asset Registry: seeded {result['created']} core assets")
        else:
            logger.info(f"✓ Asset Registry: {assets_count} assets ready")
    except Exception as e:
        logger.warning(f"Failed to bootstrap Asset Registry: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 3. SYNC INSTRUMENTS (Market Data Layer)
    # ═══════════════════════════════════════════════════════════════
    from modules.market_data.services import instrument_registry
    try:
        await instrument_registry.sync_all(force=True)
        stats = instrument_registry.stats()
        logger.info(f"✓ Instrument registry synced: {stats['total_instruments']} instruments, {stats['total_assets']} assets")
    except Exception as e:
        logger.warning(f"Failed to sync instruments on startup: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 4. AUTO-START DATA SYNC SCHEDULER (P0 Critical!)
    # ═══════════════════════════════════════════════════════════════
    try:
        from modules.scheduler.data_sync_scheduler import init_scheduler, get_scheduler
        scheduler = init_scheduler(db, auto_start=True)
        status = scheduler.get_status()
        logger.info(f"✓ Data Sync Scheduler STARTED: {status['job_count']} jobs active")
        for job in status['jobs']:
            logger.info(f"  → {job['name']}: next run {job.get('next_run', 'pending')}")
    except Exception as e:
        logger.error(f"✗ CRITICAL: Data Sync Scheduler FAILED to start: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 5. AUTO-START DISCOVERY SCHEDULER
    # ═══════════════════════════════════════════════════════════════
    try:
        from modules.scheduler.discovery_scheduler import get_discovery_scheduler
        discovery_scheduler = get_discovery_scheduler(db)
        discovery_scheduler.start()
        logger.info(f"✓ Discovery Scheduler STARTED (interval: {discovery_scheduler.interval // 60} min)")
    except Exception as e:
        logger.error(f"✗ CRITICAL: Discovery Scheduler FAILED to start: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 5.5. AUTO-START SELF-LEARNING DISCOVERY SCHEDULER
    # ═══════════════════════════════════════════════════════════════
    try:
        from modules.scheduler.self_learning_scheduler import get_self_learning_scheduler
        self_learning_scheduler = get_self_learning_scheduler(db)
        self_learning_scheduler.start()
        status = self_learning_scheduler.get_status()
        logger.info(f"✓ Self-Learning Discovery STARTED ({len(status.get('jobs', []))} jobs)")
        for job in status.get('jobs', []):
            logger.info(f"  → {job['name']}: next run {job.get('next_run', 'N/A')}")
    except Exception as e:
        logger.warning(f"Self-Learning Scheduler not started: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 6. AUTO-START NEWS INTELLIGENCE SCHEDULER
    # ═══════════════════════════════════════════════════════════════
    try:
        from modules.news_intelligence.jobs.scheduler import NewsScheduler
        news_scheduler = NewsScheduler(db)
        news_scheduler.start()
        status = news_scheduler.get_status()
        logger.info(f"✓ News Intelligence Scheduler STARTED: {status.get('job_count', 0)} jobs")
    except Exception as e:
        logger.warning(f"News Intelligence Scheduler not started: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 7. AUTO-START SENTIMENT SCHEDULER (Auto-Analyze + Caching)
    # ═══════════════════════════════════════════════════════════════
    try:
        from modules.scheduler.sentiment_scheduler import start_sentiment_scheduler
        sentiment_scheduler = start_sentiment_scheduler(db)
        status = sentiment_scheduler.get_status()
        logger.info(f"✓ Sentiment Scheduler STARTED: {len(status.get('jobs', []))} jobs")
    except Exception as e:
        logger.warning(f"Sentiment Scheduler not started: {e}")
    
    # Start Redis Pipeline (Stage 5)
    from modules.market_data.services import redis_pipeline
    try:
        await redis_pipeline.start()
        logger.info("Redis Pipeline started")
    except Exception as e:
        logger.warning(f"Failed to start Redis Pipeline: {e}")
    
    # Start Candle Ingestor (Stage 7)
    from modules.market_data.services import candle_ingestor
    try:
        await candle_ingestor.start()
        logger.info("Candle Ingestor started")
    except Exception as e:
        logger.warning(f"Failed to start Candle Ingestor: {e}")
    
    # Log startup complete
    logger.info("=" * 50)
    logger.info("FOMO Market Data API ready!")
    logger.info("  - Proxy Admin: POST /api/intel/admin/proxy/*")
    logger.info("  - Start Parser: POST /api/intel/admin/proxy/start-parser")
    logger.info("  - Full Sync: POST /api/cryptorank/sync/all")
    logger.info("  - Graph API: /api/graph/*")
    logger.info("=" * 50)
    
    # ═══════════════════════════════════════════════════════════════
    # INITIALIZE KNOWLEDGE GRAPH SERVICES
    # ═══════════════════════════════════════════════════════════════
    try:
        init_graph_services(db)
        logger.info("✓ Knowledge Graph services initialized")
        
        # Bootstrap aliases
        alias_count = await db.entity_aliases.count_documents({})
        if alias_count == 0:
            logger.info("Bootstrapping common entity aliases...")
            from modules.knowledge_graph.alias_resolver import bootstrap_common_aliases
            count = await bootstrap_common_aliases(db)
            logger.info(f"✓ Bootstrapped {count} entity aliases")
        else:
            logger.info(f"✓ Entity aliases exist: {alias_count}")
        
        # Check if graph needs initial build
        graph_nodes_count = await db.graph_nodes.count_documents({})
        if graph_nodes_count == 0:
            logger.info("Graph empty - running initial build...")
            from modules.knowledge_graph.builder import GraphBuilder
            builder = GraphBuilder(db)
            snapshot = await builder.full_rebuild()
            logger.info(f"✓ Initial graph build complete: {snapshot.node_count} nodes, {snapshot.edge_count} edges")
        else:
            logger.info(f"✓ Graph has data: {graph_nodes_count} nodes")
    except Exception as e:
        logger.warning(f"Failed to initialize Knowledge Graph: {e}")

@app.on_event("shutdown")
async def shutdown():
    # Stop Sentiment Scheduler
    try:
        from modules.scheduler.sentiment_scheduler import get_sentiment_scheduler
        scheduler = get_sentiment_scheduler()
        if scheduler:
            scheduler.stop()
            logger.info("Sentiment Scheduler stopped")
    except Exception:
        pass
    
    # Stop Data Sync Scheduler
    try:
        from modules.scheduler.data_sync_scheduler import get_scheduler
        scheduler = get_scheduler(db)
        scheduler.stop()
        logger.info("Data Sync Scheduler stopped")
    except Exception:
        pass
    
    # Stop Discovery Scheduler
    try:
        from modules.scheduler.discovery_scheduler import get_discovery_scheduler
        discovery_scheduler = get_discovery_scheduler(db)
        discovery_scheduler.stop()
        logger.info("Discovery Scheduler stopped")
    except Exception:
        pass
    
    # Stop Intel Scheduler
    from modules.intel.engine import stop_intel_scheduler
    try:
        await stop_intel_scheduler()
        logger.info("Intel Scheduler stopped")
    except Exception:
        pass
    
    # Stop Candle Ingestor
    from modules.market_data.services import candle_ingestor
    try:
        await candle_ingestor.stop()
    except Exception:
        pass
    
    # Stop Redis Pipeline
    from modules.market_data.services import redis_pipeline
    try:
        await redis_pipeline.stop()
    except Exception:
        pass
    
    client.close()
    logger.info("FOMO Market Data API shutdown")
