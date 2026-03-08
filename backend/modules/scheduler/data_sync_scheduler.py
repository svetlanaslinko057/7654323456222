"""
Data Sync Scheduler
===================
APScheduler-based scheduler for automated data synchronization.
Runs parsers on configurable intervals.

Schedule:
- CoinGecko: Every 5 minutes (market data)
- CryptoRank: Every 30 minutes (funding)
- DefiLlama: Every 15 minutes (DeFi TVL)
- TokenUnlocks: Every 6 hours (unlock schedules)
- Messari: Every 1 hour (metrics)
- Activities: Every 15 minutes
- Exchange Instruments: Every 1 hour
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

logger = logging.getLogger(__name__)


class DataSyncScheduler:
    """
    Scheduler for automated data synchronization.
    Manages periodic sync jobs for all data sources.
    """
    
    def __init__(self, db):
        self.db = db
        self.scheduler = AsyncIOScheduler(timezone="UTC")
        self._running = False
        self._jobs: Dict[str, Any] = {}
        self._stats: Dict[str, Dict] = {}
        
        # Register event listeners
        self.scheduler.add_listener(self._on_job_executed, EVENT_JOB_EXECUTED)
        self.scheduler.add_listener(self._on_job_error, EVENT_JOB_ERROR)
    
    def _on_job_executed(self, event):
        """Track successful job execution"""
        job_id = event.job_id
        self._stats[job_id] = {
            "last_run": datetime.now(timezone.utc).isoformat(),
            "status": "success",
            "run_count": self._stats.get(job_id, {}).get("run_count", 0) + 1
        }
        logger.info(f"Scheduler: Job {job_id} completed successfully")
    
    def _on_job_error(self, event):
        """Track failed job execution"""
        job_id = event.job_id
        self._stats[job_id] = {
            "last_run": datetime.now(timezone.utc).isoformat(),
            "status": "error",
            "error": str(event.exception)[:200],
            "error_count": self._stats.get(job_id, {}).get("error_count", 0) + 1
        }
        logger.error(f"Scheduler: Job {job_id} failed: {event.exception}")
    
    async def _run_coingecko_sync(self):
        """Run CoinGecko sync"""
        from modules.parsers.parser_coingecko import sync_coingecko_data
        await sync_coingecko_data(self.db, full=False)
    
    async def _run_cryptorank_sync(self):
        """Run CryptoRank sync"""
        from modules.parsers.parser_cryptorank import sync_cryptorank_data
        await sync_cryptorank_data(self.db)
    
    async def _run_defillama_sync(self):
        """Run DefiLlama sync"""
        from modules.parsers.parser_defillama import sync_defillama_data
        await sync_defillama_data(self.db, limit=100)
    
    async def _run_tokenunlocks_sync(self):
        """Run TokenUnlocks sync"""
        from modules.parsers.parser_tokenunlocks import sync_tokenunlocks_data
        await sync_tokenunlocks_data(self.db)
    
    async def _run_messari_sync(self):
        """Run Messari sync"""
        from modules.parsers.parser_messari import sync_messari_data
        await sync_messari_data(self.db, limit=50)
    
    async def _run_activities_sync(self):
        """Run Activities sync"""
        from modules.parsers.parser_activities import sync_activities_data
        await sync_activities_data(self.db)
    
    async def _run_instruments_sync(self):
        """Run Exchange Instruments sync"""
        from modules.market_data.services import instrument_registry
        try:
            await instrument_registry.sync_instruments("binance")
            await instrument_registry.sync_instruments("bybit")
        except Exception as e:
            logger.error(f"Instruments sync error: {e}")
    
    def setup_default_jobs(self):
        """Setup default sync jobs"""
        jobs = [
            {
                "id": "coingecko_sync",
                "func": self._run_coingecko_sync,
                "trigger": IntervalTrigger(minutes=5),
                "name": "CoinGecko Market Data",
                "enabled": True
            },
            {
                "id": "cryptorank_sync",
                "func": self._run_cryptorank_sync,
                "trigger": IntervalTrigger(minutes=30),
                "name": "CryptoRank Funding",
                "enabled": True
            },
            {
                "id": "defillama_sync",
                "func": self._run_defillama_sync,
                "trigger": IntervalTrigger(minutes=15),
                "name": "DefiLlama TVL",
                "enabled": True
            },
            {
                "id": "tokenunlocks_sync",
                "func": self._run_tokenunlocks_sync,
                "trigger": IntervalTrigger(hours=6),
                "name": "Token Unlocks",
                "enabled": True
            },
            {
                "id": "messari_sync",
                "func": self._run_messari_sync,
                "trigger": IntervalTrigger(hours=1),
                "name": "Messari Metrics",
                "enabled": True
            },
            {
                "id": "activities_sync",
                "func": self._run_activities_sync,
                "trigger": IntervalTrigger(minutes=15),
                "name": "Crypto Activities",
                "enabled": True
            },
            {
                "id": "instruments_sync",
                "func": self._run_instruments_sync,
                "trigger": IntervalTrigger(hours=1),
                "name": "Exchange Instruments",
                "enabled": True
            }
        ]
        
        for job in jobs:
            if job["enabled"]:
                self.add_job(
                    job["id"],
                    job["func"],
                    job["trigger"],
                    job["name"]
                )
        
        logger.info(f"Scheduler: Setup {len(jobs)} default jobs")
    
    def add_job(self, job_id: str, func: Callable, trigger, name: str = None):
        """Add a sync job"""
        if job_id in self._jobs:
            try:
                self.scheduler.remove_job(job_id)
            except:
                pass
        
        job = self.scheduler.add_job(
            func,
            trigger=trigger,
            id=job_id,
            name=name or job_id,
            replace_existing=True
        )
        
        next_run = None
        try:
            if hasattr(job, 'next_run_time') and job.next_run_time:
                next_run = job.next_run_time.isoformat()
        except:
            pass
        
        self._jobs[job_id] = {
            "id": job_id,
            "name": name or job_id,
            "next_run": next_run
        }
        return job
    
    def remove_job(self, job_id: str):
        """Remove a sync job"""
        if job_id in self._jobs:
            self.scheduler.remove_job(job_id)
            del self._jobs[job_id]
    
    def pause_job(self, job_id: str):
        """Pause a sync job"""
        self.scheduler.pause_job(job_id)
    
    def resume_job(self, job_id: str):
        """Resume a sync job"""
        self.scheduler.resume_job(job_id)
    
    def run_job_now(self, job_id: str):
        """Trigger a job to run immediately"""
        job = self.scheduler.get_job(job_id)
        if job:
            job.modify(next_run_time=datetime.now(timezone.utc))
    
    def start(self):
        """Start the scheduler"""
        if not self._running:
            self.scheduler.start()
            self._running = True
            logger.info("Scheduler: Started")
    
    def stop(self):
        """Stop the scheduler"""
        if self._running:
            self.scheduler.shutdown(wait=False)
            self._running = False
            logger.info("Scheduler: Stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get scheduler status"""
        jobs = []
        for job in self.scheduler.get_jobs():
            next_run = None
            try:
                if hasattr(job, 'next_run_time') and job.next_run_time:
                    next_run = job.next_run_time.isoformat()
            except:
                pass
            
            job_info = {
                "id": job.id,
                "name": job.name,
                "next_run": next_run,
                "paused": next_run is None
            }
            if job.id in self._stats:
                job_info.update(self._stats[job.id])
            jobs.append(job_info)
        
        return {
            "running": self._running,
            "job_count": len(jobs),
            "jobs": jobs
        }


# Global scheduler instance
_scheduler: Optional[DataSyncScheduler] = None


def get_scheduler(db) -> DataSyncScheduler:
    """Get or create scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = DataSyncScheduler(db)
    return _scheduler


def init_scheduler(db, auto_start: bool = False):
    """Initialize and optionally start scheduler"""
    scheduler = get_scheduler(db)
    scheduler.setup_default_jobs()
    if auto_start:
        scheduler.start()
    return scheduler
