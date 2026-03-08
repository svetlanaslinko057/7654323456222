"""
Scheduler API Routes
====================
API endpoints for managing the data sync scheduler.
"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import Optional
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/scheduler", tags=["Scheduler"])


def ts_now():
    return int(datetime.now(timezone.utc).timestamp() * 1000)


@router.get("/status")
async def get_scheduler_status():
    """Get scheduler status and all jobs"""
    from server import db
    from modules.scheduler.data_sync_scheduler import get_scheduler
    
    scheduler = get_scheduler(db)
    status = scheduler.get_status()
    
    return {
        "ts": ts_now(),
        **status
    }


@router.post("/start")
async def start_scheduler():
    """Start the scheduler"""
    from server import db
    from modules.scheduler.data_sync_scheduler import init_scheduler
    
    scheduler = init_scheduler(db, auto_start=True)
    
    return {
        "ts": ts_now(),
        "ok": True,
        "message": "Scheduler started",
        "status": scheduler.get_status()
    }


@router.post("/stop")
async def stop_scheduler():
    """Stop the scheduler"""
    from server import db
    from modules.scheduler.data_sync_scheduler import get_scheduler
    
    scheduler = get_scheduler(db)
    scheduler.stop()
    
    return {
        "ts": ts_now(),
        "ok": True,
        "message": "Scheduler stopped"
    }


@router.post("/jobs/{job_id}/run")
async def run_job_now(job_id: str, background_tasks: BackgroundTasks):
    """Trigger a job to run immediately"""
    from server import db
    from modules.scheduler.data_sync_scheduler import get_scheduler
    
    scheduler = get_scheduler(db)
    
    # Find job
    status = scheduler.get_status()
    job_exists = any(j["id"] == job_id for j in status["jobs"])
    
    if not job_exists:
        raise HTTPException(404, f"Job {job_id} not found")
    
    scheduler.run_job_now(job_id)
    
    return {
        "ts": ts_now(),
        "ok": True,
        "message": f"Job {job_id} triggered"
    }


@router.post("/jobs/{job_id}/pause")
async def pause_job(job_id: str):
    """Pause a scheduled job"""
    from server import db
    from modules.scheduler.data_sync_scheduler import get_scheduler
    
    scheduler = get_scheduler(db)
    scheduler.pause_job(job_id)
    
    return {
        "ts": ts_now(),
        "ok": True,
        "message": f"Job {job_id} paused"
    }


@router.post("/jobs/{job_id}/resume")
async def resume_job(job_id: str):
    """Resume a paused job"""
    from server import db
    from modules.scheduler.data_sync_scheduler import get_scheduler
    
    scheduler = get_scheduler(db)
    scheduler.resume_job(job_id)
    
    return {
        "ts": ts_now(),
        "ok": True,
        "message": f"Job {job_id} resumed"
    }


# ═══════════════════════════════════════════════════════════════
# MANUAL SYNC TRIGGERS (enhanced from routes_sync)
# ═══════════════════════════════════════════════════════════════

@router.post("/sync/defillama")
async def sync_defillama(background_tasks: BackgroundTasks):
    """Sync DefiLlama protocols and TVL data"""
    from server import db
    from modules.parsers.parser_defillama import sync_defillama_data
    
    background_tasks.add_task(sync_defillama_data, db, 100)
    
    return {
        "ts": ts_now(),
        "ok": True,
        "message": "DefiLlama sync started"
    }


@router.post("/sync/tokenunlocks")
async def sync_tokenunlocks(background_tasks: BackgroundTasks):
    """Sync token unlock schedules"""
    from server import db
    from modules.parsers.parser_tokenunlocks import sync_tokenunlocks_data
    
    background_tasks.add_task(sync_tokenunlocks_data, db, 90)
    
    return {
        "ts": ts_now(),
        "ok": True,
        "message": "TokenUnlocks sync started"
    }


@router.post("/sync/messari")
async def sync_messari(background_tasks: BackgroundTasks):
    """Sync Messari asset metrics"""
    from server import db
    from modules.parsers.parser_messari import sync_messari_data
    
    background_tasks.add_task(sync_messari_data, db, 50)
    
    return {
        "ts": ts_now(),
        "ok": True,
        "message": "Messari sync started"
    }


@router.post("/sync/all-new")
async def sync_all_new_sources(background_tasks: BackgroundTasks):
    """Sync all new data sources (DefiLlama, TokenUnlocks, Messari)"""
    from server import db
    from modules.parsers.parser_defillama import sync_defillama_data
    from modules.parsers.parser_tokenunlocks import sync_tokenunlocks_data
    from modules.parsers.parser_messari import sync_messari_data
    
    async def run_all():
        try:
            await sync_defillama_data(db, 100)
            await sync_tokenunlocks_data(db, 90)
            await sync_messari_data(db, 50)
            logger.info("All new sources sync complete")
        except Exception as e:
            logger.error(f"Sync all new error: {e}")
    
    background_tasks.add_task(run_all)
    
    return {
        "ts": ts_now(),
        "ok": True,
        "message": "All new sources sync started",
        "sources": ["defillama", "tokenunlocks", "messari"]
    }



# ═══════════════════════════════════════════════════════════════
# DISCOVERY SCHEDULER ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@router.get("/discovery/status")
async def get_discovery_scheduler_status():
    """Get auto-discovery scheduler status"""
    from server import db
    from modules.scheduler.discovery_scheduler import get_discovery_scheduler
    
    scheduler = get_discovery_scheduler(db)
    return scheduler.get_status()


@router.post("/discovery/start")
async def start_discovery_scheduler():
    """Start the auto-discovery scheduler (runs every 60 minutes)"""
    from server import db
    from modules.scheduler.discovery_scheduler import get_discovery_scheduler
    
    scheduler = get_discovery_scheduler(db)
    result = scheduler.start()
    
    return {
        "ts": ts_now(),
        "ok": True,
        **result
    }


@router.post("/discovery/stop")
async def stop_discovery_scheduler():
    """Stop the auto-discovery scheduler"""
    from server import db
    from modules.scheduler.discovery_scheduler import get_discovery_scheduler
    
    scheduler = get_discovery_scheduler(db)
    result = scheduler.stop()
    
    return {
        "ts": ts_now(),
        "ok": True,
        **result
    }


@router.post("/discovery/run-now")
async def run_discovery_now(background_tasks: BackgroundTasks):
    """Trigger discovery immediately (runs in background)"""
    from server import db
    from modules.scheduler.discovery_scheduler import get_discovery_scheduler
    
    scheduler = get_discovery_scheduler(db)
    
    async def run():
        await scheduler.run_now()
    
    background_tasks.add_task(run)
    
    return {
        "ts": ts_now(),
        "ok": True,
        "message": "Discovery started in background"
    }
