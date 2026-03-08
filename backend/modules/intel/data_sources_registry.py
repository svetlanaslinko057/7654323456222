"""
Data Sources Registry
=====================
Master registry of all data sources for FOMO Platform.
Tracks what sources are available, their capabilities, sync status, and priority.

Categories:
- funding: Investment rounds, VC data
- ico: Token sales, launchpads
- unlocks: Token unlock schedules
- activities: Airdrops, campaigns, testnets
- market: Price, volume, market data
- projects: Project info, profiles
- funds: Fund/VC profiles
- persons: Key people in crypto
- news: Crypto news feeds
- defi: DeFi protocols, TVL
"""

from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from enum import Enum


class SourceCategory(str, Enum):
    FUNDING = "funding"
    ICO = "ico"
    UNLOCKS = "unlocks"
    ACTIVITIES = "activities"
    MARKET = "market"
    PROJECTS = "projects"
    FUNDS = "funds"
    PERSONS = "persons"
    NEWS = "news"
    DEFI = "defi"
    ANALYTICS = "analytics"


class SourcePriority(str, Enum):
    CRITICAL = "critical"  # Must have, primary source
    HIGH = "high"          # Important, frequently used
    MEDIUM = "medium"      # Useful supplement
    LOW = "low"            # Nice to have


class SourceStatus(str, Enum):
    ACTIVE = "active"      # Parser implemented and working
    PARTIAL = "partial"    # Some endpoints work
    PLANNED = "planned"    # Not implemented yet
    DISABLED = "disabled"  # Temporarily disabled


class DataSourceModel(BaseModel):
    """Schema for data source"""
    id: str
    name: str
    website: str
    categories: List[str]
    data_types: List[str]
    priority: str
    status: str
    has_api: bool
    api_key_required: bool
    rate_limit: Optional[str] = None
    parser_module: Optional[str] = None
    last_sync: Optional[str] = None
    sync_count: int = 0
    error_count: int = 0
    last_error: Optional[str] = None
    description: Optional[str] = None
    is_new: bool = False
    discovered_at: Optional[str] = None


# ═══════════════════════════════════════════════════════════════
# MASTER DATA SOURCES REGISTRY
# ═══════════════════════════════════════════════════════════════

DATA_SOURCES = [
    # ─────────────────────────────────────────────────────────────
    # TIER 1: CRITICAL SOURCES (Active with parsers)
    # ─────────────────────────────────────────────────────────────
    {
        "id": "coingecko",
        "name": "CoinGecko",
        "website": "https://coingecko.com",
        "categories": ["market", "projects", "analytics"],
        "data_types": ["prices", "market_cap", "volume", "project_info", "categories", "exchanges"],
        "priority": "critical",
        "status": "active",
        "has_api": True,
        "api_key_required": False,
        "rate_limit": "50 req/min",
        "parser_module": "parser_coingecko",
        "description": "Primary source for market data and project profiles"
    },
    {
        "id": "cryptorank",
        "name": "CryptoRank",
        "website": "https://cryptorank.io",
        "categories": ["funding", "ico", "unlocks", "activities", "analytics"],
        "data_types": ["funding_rounds", "investors", "ico_calendar", "unlocks", "activities"],
        "priority": "critical",
        "status": "active",
        "has_api": True,
        "api_key_required": False,
        "rate_limit": "30 req/min",
        "parser_module": "parser_cryptorank",
        "description": "Primary source for funding data and token unlocks"
    },
    {
        "id": "dropstab",
        "name": "Dropstab",
        "website": "https://dropstab.com",
        "categories": ["activities"],
        "data_types": ["airdrops", "campaigns", "testnets", "points_programs"],
        "priority": "critical",
        "status": "active",
        "has_api": False,
        "api_key_required": False,
        "rate_limit": "10 req/min",
        "parser_module": "parser_activities",
        "description": "Primary source for crypto activities and airdrops"
    },
    
    # ─────────────────────────────────────────────────────────────
    # TIER 2: HIGH PRIORITY SOURCES (Active with parsers)
    # ─────────────────────────────────────────────────────────────
    {
        "id": "tokenunlocks",
        "name": "TokenUnlocks",
        "website": "https://token.unlocks.app",
        "categories": ["unlocks"],
        "data_types": ["unlock_schedules", "vesting_data", "cliff_dates"],
        "priority": "high",
        "status": "active",
        "has_api": True,
        "api_key_required": False,
        "rate_limit": "10 req/min",
        "parser_module": "parser_tokenunlocks",
        "description": "Specialized source for token unlock data"
    },
    {
        "id": "defillama",
        "name": "DefiLlama",
        "website": "https://defillama.com",
        "categories": ["defi", "projects", "analytics"],
        "data_types": ["tvl", "protocol_data", "yields", "bridges"],
        "priority": "high",
        "status": "active",
        "has_api": True,
        "api_key_required": False,
        "rate_limit": "100 req/min",
        "parser_module": "parser_defillama",
        "description": "DeFi analytics and TVL tracking"
    },
    {
        "id": "rootdata",
        "name": "RootData",
        "website": "https://rootdata.com",
        "categories": ["funding", "funds", "persons"],
        "data_types": ["funding_rounds", "investor_profiles", "team_members"],
        "priority": "high",
        "status": "active",
        "has_api": True,
        "api_key_required": False,
        "rate_limit": "20 req/min",
        "parser_module": "parser_rootdata",
        "description": "Crypto investment and fund data"
    },
    {
        "id": "messari",
        "name": "Messari",
        "website": "https://messari.io",
        "categories": ["projects", "funding", "analytics", "news"],
        "data_types": ["project_profiles", "funding_rounds", "research", "metrics"],
        "priority": "high",
        "status": "planned",
        "has_api": True,
        "api_key_required": True,
        "rate_limit": "20 req/min",
        "parser_module": "parser_messari",
        "description": "Research and analytics platform (requires API key)"
    },
    {
        "id": "coinmarketcap",
        "name": "CoinMarketCap",
        "website": "https://coinmarketcap.com",
        "categories": ["market", "projects", "ico", "activities"],
        "data_types": ["prices", "market_cap", "volume", "ico_calendar", "airdrops"],
        "priority": "high",
        "status": "planned",
        "has_api": True,
        "api_key_required": True,
        "rate_limit": "30 req/min",
        "parser_module": "parser_coinmarketcap",
        "description": "Alternative market data source (requires API key)"
    },
    
    # ─────────────────────────────────────────────────────────────
    # TIER 3: MEDIUM PRIORITY SOURCES (Active with parsers)
    # ─────────────────────────────────────────────────────────────
    {
        "id": "icodrops",
        "name": "ICO Drops",
        "website": "https://icodrops.com",
        "categories": ["ico"],
        "data_types": ["ico_calendar", "token_sales", "launchpads"],
        "priority": "medium",
        "status": "active",
        "has_api": False,
        "api_key_required": False,
        "rate_limit": "10 req/min",
        "parser_module": "parser_icodrops",
        "description": "ICO and token sale calendar"
    },
    {
        "id": "dappradar",
        "name": "DappRadar",
        "website": "https://dappradar.com",
        "categories": ["defi", "projects"],
        "data_types": ["dapps", "usage_stats", "rankings"],
        "priority": "medium",
        "status": "active",
        "has_api": True,
        "api_key_required": False,
        "rate_limit": "50 req/min",
        "parser_module": "parser_dappradar",
        "description": "DApp analytics and rankings"
    },
    {
        "id": "dropsearn",
        "name": "DropsEarn",
        "website": "https://dropsearn.com",
        "categories": ["activities"],
        "data_types": ["airdrops", "campaigns", "testnets"],
        "priority": "medium",
        "status": "active",
        "has_api": False,
        "api_key_required": False,
        "rate_limit": "10 req/min",
        "parser_module": "parser_activities",
        "description": "Alternative source for airdrop campaigns"
    },
    {
        "id": "airdropalert",
        "name": "AirdropAlert",
        "website": "https://airdropalert.com",
        "categories": ["activities"],
        "data_types": ["airdrops"],
        "priority": "medium",
        "status": "active",
        "has_api": False,
        "api_key_required": False,
        "rate_limit": "N/A",
        "parser_module": "parser_airdropalert",
        "description": "Airdrop aggregator"
    },
    
    # ─────────────────────────────────────────────────────────────
    # TIER 4: NEWS SOURCES (Active with parsers)
    # ─────────────────────────────────────────────────────────────
    {
        "id": "cointelegraph",
        "name": "Cointelegraph",
        "website": "https://cointelegraph.com",
        "categories": ["news"],
        "data_types": ["news_articles", "market_updates"],
        "priority": "low",
        "status": "active",
        "has_api": False,
        "api_key_required": False,
        "rate_limit": "N/A",
        "parser_module": "parser_news",
        "description": "Crypto news source (RSS)"
    },
    {
        "id": "theblock",
        "name": "The Block",
        "website": "https://theblock.co",
        "categories": ["news", "analytics"],
        "data_types": ["news_articles", "research", "data"],
        "priority": "low",
        "status": "active",
        "has_api": False,
        "api_key_required": False,
        "rate_limit": "N/A",
        "parser_module": "parser_news",
        "description": "Crypto news and research (RSS)"
    },
    {
        "id": "coindesk",
        "name": "CoinDesk",
        "website": "https://coindesk.com",
        "categories": ["news"],
        "data_types": ["news_articles", "market_updates"],
        "priority": "low",
        "status": "active",
        "has_api": False,
        "api_key_required": False,
        "rate_limit": "N/A",
        "parser_module": "parser_news",
        "description": "Crypto news source (RSS)"
    },
    {
        "id": "incrypted",
        "name": "Incrypted",
        "website": "https://incrypted.com",
        "categories": ["news", "analytics"],
        "data_types": ["news_articles", "market_updates", "research", "guides", "airdrops", "tokensales"],
        "priority": "critical",
        "status": "active",
        "has_api": False,
        "api_key_required": False,
        "rate_limit": "N/A",
        "parser_module": "parser_incrypted",
        "description": "Ukrainian crypto news, analytics, airdrops, tokensales - primary news source"
    },
]


class DataSourcesRegistry:
    """
    Data Sources Registry Manager
    Handles CRUD operations for data sources and tracks sync status
    """
    
    def __init__(self, db):
        self.db = db
        self.collection = db.data_sources
    
    async def seed_sources(self) -> Dict[str, Any]:
        """Seed all predefined data sources to MongoDB"""
        now = datetime.now(timezone.utc).isoformat()
        seeded = 0
        
        for source in DATA_SOURCES:
            doc = {
                **source,
                "sync_count": 0,
                "error_count": 0,
                "last_sync": None,
                "last_error": None,
                "created_at": now,
                "updated_at": now
            }
            await self.collection.update_one(
                {"id": source["id"]},
                {"$set": doc},
                upsert=True
            )
            seeded += 1
        
        return {"seeded": seeded, "total": len(DATA_SOURCES)}
    
    async def get_all_sources(self, 
                               category: Optional[str] = None,
                               status: Optional[str] = None,
                               priority: Optional[str] = None) -> List[Dict]:
        """Get all data sources with optional filters"""
        query = {}
        if category:
            query["categories"] = category
        if status:
            query["status"] = status
        if priority:
            query["priority"] = priority
        
        sources = await self.collection.find(query, {"_id": 0}).to_list(100)
        return sources
    
    async def get_source(self, source_id: str) -> Optional[Dict]:
        """Get single data source by ID"""
        return await self.collection.find_one({"id": source_id}, {"_id": 0})
    
    async def update_sync_status(self, source_id: str, success: bool, 
                                  records: int = 0, error: Optional[str] = None):
        """Update sync status for a source"""
        now = datetime.now(timezone.utc).isoformat()
        update = {
            "updated_at": now,
            "last_sync": now if success else None
        }
        
        if success:
            update["$inc"] = {"sync_count": 1}
        else:
            update["last_error"] = error
            update["$inc"] = {"error_count": 1}
        
        await self.collection.update_one(
            {"id": source_id},
            {"$set": {k: v for k, v in update.items() if k != "$inc"}} | 
            ({"$inc": update["$inc"]} if "$inc" in update else {})
        )
    
    async def get_active_sources(self) -> List[Dict]:
        """Get sources that have active parsers"""
        return await self.collection.find(
            {"status": "active"},
            {"_id": 0}
        ).to_list(50)
    
    async def get_sources_by_data_type(self, data_type: str) -> List[Dict]:
        """Get sources that provide specific data type"""
        return await self.collection.find(
            {"data_types": data_type},
            {"_id": 0}
        ).sort("priority", 1).to_list(20)
    
    async def get_sync_summary(self) -> Dict[str, Any]:
        """Get summary of all sources sync status"""
        sources = await self.get_all_sources()
        
        summary = {
            "total": len(sources),
            "active": sum(1 for s in sources if s.get("status") == "active"),
            "planned": sum(1 for s in sources if s.get("status") == "planned"),
            "by_category": {},
            "by_priority": {},
            "recently_synced": []
        }
        
        for s in sources:
            for cat in s.get("categories", []):
                if cat not in summary["by_category"]:
                    summary["by_category"][cat] = 0
                summary["by_category"][cat] += 1
            
            p = s.get("priority", "unknown")
            if p not in summary["by_priority"]:
                summary["by_priority"][p] = 0
            summary["by_priority"][p] += 1
            
            if s.get("last_sync"):
                summary["recently_synced"].append({
                    "id": s["id"],
                    "name": s["name"],
                    "last_sync": s["last_sync"]
                })
        
        summary["recently_synced"] = sorted(
            summary["recently_synced"], 
            key=lambda x: x["last_sync"], 
            reverse=True
        )[:5]
        
        return summary
