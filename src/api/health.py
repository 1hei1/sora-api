import time
import platform
import os
import sys
import psutil
from fastapi import APIRouter, Depends
from ..key_manager import key_manager

# 创建路由
router = APIRouter()

@router.get("/health")
async def health_check():
    """
    API健康检查端点
    
    返回:
        基本的健康状态信息
    """
    return {
        "status": "ok",
        "timestamp": time.time(),
        "version": "2.0.0"
    }

@router.get("/health/extended")
async def extended_health_check():
    """
    扩展的健康检查端点
    
    返回:
        详细的系统和服务状态信息
    """
    # 获取系统信息
    system_info = {
        "platform": platform.platform(),
        "python_version": sys.version,
        "cpu_count": psutil.cpu_count(),
        "memory_total": psutil.virtual_memory().total,
        "memory_available": psutil.virtual_memory().available,
        "disk_usage": psutil.disk_usage('/').percent
    }
    
    # 获取服务信息
    service_info = {
        "uptime": time.time() - psutil.Process(os.getpid()).create_time(),
        "active_keys": sum(1 for k in key_manager.keys if k.get("is_enabled", False)),
        "total_keys": len(key_manager.keys),
    }
    
    return {
        "status": "ok",
        "timestamp": time.time(),
        "version": "2.0.0",
        "system": system_info,
        "service": service_info,
    } 