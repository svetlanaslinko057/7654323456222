"""
Data Sources Health Check Service
=================================

Проверяет реальную работоспособность каждого источника данных.
Обновляет статусы в Discovery на основе реальных проверок.
"""

import asyncio
import httpx
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)


# Health check configurations for each data source
HEALTH_CHECKS = {
    # Market Data
    "coingecko": {
        "url": "https://api.coingecko.com/api/v3/ping",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10,
        "requires_key": False,
    },
    "coinmarketcap": {
        "url": "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest",
        "method": "GET",
        "expected_status": [200, 401],  # 401 = needs API key
        "timeout": 10,
        "requires_key": True,
        "key_env": "CMC_API_KEY",
    },
    "messari": {
        "url": "https://data.messari.io/api/v1/assets",
        "method": "GET",
        "expected_status": [200, 401, 429],
        "timeout": 10,
        "requires_key": True,
        "key_env": "MESSARI_API_KEY",
    },
    
    # DeFi
    "defillama": {
        "url": "https://api.llama.fi/protocols",
        "method": "GET",
        "expected_status": 200,
        "timeout": 15,
        "requires_key": False,
    },
    "tokenterminal": {
        "url": "https://api.tokenterminal.com/v2/projects",
        "method": "GET",
        "expected_status": [200, 401, 403],
        "timeout": 10,
        "requires_key": True,
    },
    
    # DEX
    "dexscreener": {
        "url": "https://api.dexscreener.com/latest/dex/search?q=eth",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10,
        "requires_key": False,
    },
    "geckoterminal": {
        "url": "https://api.geckoterminal.com/api/v2/networks/eth/trending_pools",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10,
        "requires_key": False,
    },
    "dextools": {
        "url": "https://public-api.dextools.io/trial/v2/token/ether/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2/info",
        "method": "GET",
        "expected_status": [200, 401, 429],
        "timeout": 10,
        "requires_key": False,  # Trial endpoint
    },
    
    # Intel / Funding
    "cryptorank": {
        "url": "https://api.cryptorank.io/v1/currencies",
        "method": "GET",
        "expected_status": [200, 401],
        "timeout": 10,
        "requires_key": False,  # Basic endpoint is free
    },
    "dropstab": {
        "url": "https://dropstab.com/api/v1/activities",
        "method": "GET",
        "expected_status": [200, 403, 404],
        "timeout": 10,
        "requires_key": False,
    },
    "rootdata": {
        "url": "https://api.rootdata.com/open/ser_inv",
        "method": "GET",
        "expected_status": [200, 401, 403],
        "timeout": 10,
        "requires_key": True,
    },
    
    # Token Unlocks
    "tokenunlocks": {
        "url": "https://token.unlocks.app/api/v1/unlocks",
        "method": "GET",
        "expected_status": [200, 401, 403],
        "timeout": 10,
        "requires_key": False,
    },
    
    # Derivatives
    "coinglass": {
        "url": "https://open-api.coinglass.com/public/v2/funding",
        "method": "GET",
        "expected_status": [200, 401],
        "timeout": 10,
        "requires_key": False,  # Public endpoint
    },
    "laevitas": {
        "url": "https://api.laevitas.ch/analytics/defi",
        "method": "GET",
        "expected_status": [200, 401, 403],
        "timeout": 10,
        "requires_key": True,
    },
    
    # L2
    "l2beat": {
        "url": "https://api.l2beat.com/tvl.json",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10,
        "requires_key": False,
    },
    "growthepie": {
        "url": "https://api.growthepie.xyz/v1/chains.json",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10,
        "requires_key": False,
    },
    
    # News
    "cointelegraph": {
        "url": "https://cointelegraph.com/rss",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10,
        "requires_key": False,
        "type": "rss",
    },
    "theblock": {
        "url": "https://www.theblock.co/rss.xml",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10,
        "requires_key": False,
        "type": "rss",
    },
    "coindesk": {
        "url": "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10,
        "requires_key": False,
        "type": "rss",
    },
    "incrypted": {
        "url": "https://incrypted.com/feed/",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10,
        "requires_key": False,
        "type": "rss",
    },
    
    # Activities
    "icodrops": {
        "url": "https://icodrops.com/",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10,
        "requires_key": False,
        "type": "html",
    },
    "dappradar": {
        "url": "https://api.dappradar.com/4tsxo4vuhotaojtl/dapps",
        "method": "GET",
        "expected_status": [200, 401, 403],
        "timeout": 10,
        "requires_key": True,
    },
    "dropsearn": {
        "url": "https://dropsearn.com/airdrops/",
        "method": "GET",
        "expected_status": 200,
        "timeout": 10,
        "requires_key": False,
        "type": "html",
    },
    "airdropalert": {
        "url": "https://airdropalert.com/api/airdrops",
        "method": "GET",
        "expected_status": [200, 403, 404],
        "timeout": 10,
        "requires_key": False,
    },
}


class DataSourceHealthChecker:
    """
    Проверяет работоспособность источников данных.
    """
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.client = httpx.AsyncClient(
            timeout=30,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
        )
    
    async def close(self):
        await self.client.aclose()
    
    async def check_single_source(self, source_id: str) -> Dict[str, Any]:
        """Check a single data source"""
        config = HEALTH_CHECKS.get(source_id)
        
        if not config:
            return {
                "source_id": source_id,
                "status": "unknown",
                "message": "No health check configured",
                "checked_at": datetime.now(timezone.utc).isoformat()
            }
        
        try:
            url = config["url"]
            method = config.get("method", "GET")
            timeout = config.get("timeout", 10)
            expected = config.get("expected_status", 200)
            
            # Make request
            if method == "GET":
                resp = await self.client.get(url, timeout=timeout)
            else:
                resp = await self.client.post(url, timeout=timeout)
            
            # Check status
            if isinstance(expected, list):
                is_ok = resp.status_code in expected
            else:
                is_ok = resp.status_code == expected
            
            # Determine status
            if is_ok:
                if resp.status_code == 200:
                    status = "active"
                    message = "Working"
                elif resp.status_code == 401:
                    status = "needs_key"
                    message = "API key required"
                elif resp.status_code == 429:
                    status = "rate_limited"
                    message = "Rate limited"
                else:
                    status = "active"
                    message = f"OK ({resp.status_code})"
            else:
                status = "error"
                message = f"Unexpected status: {resp.status_code}"
            
            # Check response content for RSS/HTML
            if config.get("type") == "rss" and resp.status_code == 200:
                content = resp.text[:500]
                if "<rss" in content or "<feed" in content or "<?xml" in content:
                    status = "active"
                    message = "RSS feed working"
                else:
                    status = "degraded"
                    message = "RSS format issue"
            
            return {
                "source_id": source_id,
                "status": status,
                "http_status": resp.status_code,
                "message": message,
                "response_time_ms": int(resp.elapsed.total_seconds() * 1000),
                "checked_at": datetime.now(timezone.utc).isoformat()
            }
            
        except httpx.TimeoutException:
            return {
                "source_id": source_id,
                "status": "timeout",
                "message": f"Timeout after {config.get('timeout', 10)}s",
                "checked_at": datetime.now(timezone.utc).isoformat()
            }
        except httpx.ConnectError as e:
            return {
                "source_id": source_id,
                "status": "offline",
                "message": f"Connection failed: {str(e)[:100]}",
                "checked_at": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            return {
                "source_id": source_id,
                "status": "error",
                "message": f"Error: {str(e)[:100]}",
                "checked_at": datetime.now(timezone.utc).isoformat()
            }
    
    async def check_all_sources(self) -> Dict[str, Any]:
        """Check all configured data sources"""
        results = []
        
        # Get all sources from DB
        cursor = self.db.data_sources.find({}, {"_id": 0})
        sources = await cursor.to_list(length=100)
        
        # Check each source
        for source in sources:
            source_id = source.get("id")
            if source_id:
                result = await self.check_single_source(source_id)
                results.append(result)
                # Small delay to avoid rate limits
                await asyncio.sleep(0.5)
        
        # Update statuses in database
        for result in results:
            status = result["status"]
            
            # Map status to DB status
            if status == "active":
                db_status = "active"
            elif status in ["needs_key", "rate_limited"]:
                db_status = "degraded"
            elif status == "timeout":
                db_status = "timeout"
            elif status == "offline":
                db_status = "offline"
            else:
                db_status = "error"
            
            await self.db.data_sources.update_one(
                {"id": result["source_id"]},
                {"$set": {
                    "status": db_status,
                    "last_check": result,
                    "last_checked_at": result["checked_at"]
                }}
            )
        
        # Summary
        summary = {
            "total": len(results),
            "active": len([r for r in results if r["status"] == "active"]),
            "degraded": len([r for r in results if r["status"] in ["needs_key", "rate_limited", "degraded"]]),
            "offline": len([r for r in results if r["status"] in ["timeout", "offline", "error"]]),
            "checked_at": datetime.now(timezone.utc).isoformat()
        }
        
        return {
            "summary": summary,
            "results": results
        }


async def run_health_check(db: AsyncIOMotorDatabase) -> Dict[str, Any]:
    """Run health check for all data sources"""
    checker = DataSourceHealthChecker(db)
    try:
        return await checker.check_all_sources()
    finally:
        await checker.close()
