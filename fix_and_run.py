#!/usr/bin/env python3
"""
修复并运行 DentalReserve
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def fix_requirements():
    """修复 requirements.txt"""
    print("🔧 修复 requirements.txt...")

    req_file = Path("backend/requirements.txt")
    if req_file.exists():
        content = req_file.read_text()

        # 检查是否需要修复
        if "pydantic-settings" not in content and "pydantic==2." in content:
            # 替换为旧版本
            content = content.replace("pydantic==2.5.0", "pydantic==1.10.13")
            content = content.replace('pydantic[email]==2.5.0', 'pydantic[email]==1.10.13')

            # 确保没有 pydantic-settings
            if "pydantic-settings" not in content:
                content = content.replace("pydantic", "pydantic[email]==1.10.13")

            req_file.write_text(content)
            print("✅ 已修复 requirements.txt")

            # 重新安装
            print("📦 重新安装依赖...")
            subprocess.run([
                sys.executable, "-m", "pip", "install",
                "-r", str(req_file), "--force-reinstall"
            ], check=True)
        else:
            print("✅ requirements.txt 正常")
    else:
        print("❌ requirements.txt 不存在")

def fix_config_file():
    """修复 config.py"""
    print("🔧 修复 config.py...")

    config_file = Path("backend/app/core/config.py")
    if config_file.exists():
        content = config_file.read_text()

        # 检查是否有 BaseSettings
        if "from pydantic import BaseSettings" in content:
            # 替换为简单的 BaseModel
            new_content = """import os
from typing import Optional, List
from pydantic import BaseModel, Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

class Settings(BaseModel):
    # 应用配置
    PROJECT_NAME: str = "DentalReserve"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"

    # 文件存储路径
    DATA_DIR: Path = DATA_DIR
    CLINICS_FILE: Path = DATA_DIR / "clinics.json"
    USERS_FILE: Path = DATA_DIR / "users.json"
    APPOINTMENTS_FILE: Path = DATA_DIR / "appointments.json"
    VIRTUAL_NUMBERS_FILE: Path = DATA_DIR / "virtual_numbers.json"
    CALL_LOGS_FILE: Path = DATA_DIR / "call_logs.json"

    # Twilio配置
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_PHONE_NUMBER: str = os.getenv("TWILIO_PHONE_NUMBER", "")

    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    # 环境
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"

    class Config:
        env_file = ".env"

settings = Settings()

# 创建必要目录
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
"""

            config_file.write_text(new_content)
            print("✅ 已修复 config.py")
        else:
            print("✅ config.py 正常")
    else:
        print("⚠️ config.py 不存在，将创建...")

        # 创建目录
        config_file.parent.mkdir(parents=True, exist_ok=True)

        # 写入简单配置
        simple_config = """import os
from typing import List
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

class Settings:
    PROJECT_NAME = "DentalReserve"
    VERSION = "1.0.0"
    API_V1_STR = "/api/v1"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

    # 文件存储
    DATA_DIR = DATA_DIR
    CLINICS_FILE = DATA_DIR / "clinics.json"
    USERS_FILE = DATA_DIR / "users.json"
    APPOINTMENTS_FILE = DATA_DIR / "appointments.json"

    # CORS
    BACKEND_CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    DEBUG = os.getenv("ENVIRONMENT", "development") == "development"

settings = Settings()
settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
"""
        config_file.write_text(simple_config)
        print("✅ 已创建 config.py")

def create_simple_main():
    """创建简单的 main.py 确保能运行"""
    print("🔧 创建简单版 main.py...")

    main_file = Path("backend/app/main.py")
    if main_file.exists():
        # 备份原文件
        backup = main_file.with_suffix('.py.backup')
        main_file.rename(backup)
        print(f"✅ 已备份原文件到 {backup}")

    # 创建简单的 main.py
    simple_main = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import json

# 创建应用
app = FastAPI(
    title="DentalReserve API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路由
@app.get("/")
async def root():
    return {
        "message": "🎉 DentalReserve API 正在运行！",
        "status": "active",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "clinics": "/api/v1/clinics",
            "login": "/api/v1/auth/token"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dentalreserve"}

# 诊所数据
SAMPLE_CLINICS = [
    {
        "id": "1",
        "name": "Toronto Downtown Dental",
        "address": "123 Bay Street, Toronto, ON M5J 2S1",
        "city": "Toronto",
        "province": "ON",
        "phone": "+1 (416) 555-1234",
        "email": "info@torontodental.com",
        "description": "现代化牙科诊所",
        "latitude": 43.651070,
        "longitude": -79.347015,
        "rating": 4.5,
        "review_count": 124
    },
    {
        "id": "2",
        "name": "Vancouver Dental Care",
        "address": "456 Granville Street, Vancouver, BC V6C 1T2",
        "city": "Vancouver",
        "province": "BC",
        "phone": "+1 (604) 555-1234",
        "email": "contact@vancouverdental.com",
        "description": "专业牙科护理",
        "latitude": 49.282729,
        "longitude": -123.120738,
        "rating": 4.8,
        "review_count": 89
    }
]

@app.get("/api/v1/clinics")
async def get_clinics():
    return {
        "count": len(SAMPLE_CLINICS),
        "clinics": SAMPLE_CLINICS
    }

@app.get("/api/v1/clinics/{clinic_id}")
async def get_clinic(clinic_id: str):
    for clinic in SAMPLE_CLINICS:
        if clinic["id"] == clinic_id:
            return clinic
    return {"error": "诊所不存在"}

# 简单的认证
@app.post("/api/v1/auth/token")
async def login(username: str, password: str):
    # 简化版登录，实际应该验证数据库
    test_users = {
        "patient@example.com": {"password": "Patient123!", "role": "patient"},
        "admin@dentalreserve.ca": {"password": "Admin123!", "role": "admin"},
        "dr.smith@torontodental.com": {"password": "Doctor123!", "role": "doctor"}
    }

    if username in test_users and password == test_users[username]["password"]:
        return {
            "access_token": "fake-jwt-token-for-testing",
            "token_type": "bearer",
            "role": test_users[username]["role"]
        }

    return {"error": "用户名或密码错误"}

if __name__ == "__main__":
    print("🚀 启动 DentalReserve API...")
    print("🌐 访问地址: http://localhost:8000")
    print("📚 API文档: http://localhost:8000/docs")

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
"""

    main_file.write_text(simple_main)
    print("✅ 已创建简单版 main.py")

def check_and_create_dirs():
    """检查并创建必要目录"""
    print("📁 检查目录结构...")

    dirs_to_create = [
        Path("data"),
        Path("backend/uploads"),
        Path("backend/app/core"),
        Path("backend/app/api/v1"),
        Path("backend/app/models"),
        Path("backend/app/schemas"),
        Path("backend/app/services"),
    ]

    for dir_path in dirs_to_create:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {dir_path}")

    # 创建必要的 __init__.py 文件
    init_files = [
        Path("backend/app/__init__.py"),
        Path("backend/app/core/__init__.py"),
        Path("backend/app/api/__init__.py"),
        Path("backend/app/api/v1/__init__.py"),
        Path("backend/app/models/__init__.py"),
        Path("backend/app/schemas/__init__.py"),
        Path("backend/app/services/__init__.py"),
    ]

    for init_file in init_files:
        if not init_file.exists():
            init_file.write_text("# Package initialization\n")
            print(f"  ✅ {init_file}")

def run_server():
    """运行服务器"""
    print("\n" + "="*60)
    print("🚀 启动 DentalReserve 服务器")
    print("="*60)

    # 切换到backend目录
    os.chdir("backend")

    try:
        print("📢 服务器信息:")
        print("   访问地址: http://localhost:8000")
        print("   API文档: http://localhost:8000/docs")
        print("   健康检查: http://localhost:8000/health")
        print("\n🛑 按 Ctrl+C 停止服务器")
        print("="*60)

        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    finally:
        os.chdir("..")

def main():
    """主函数"""
    print("🦷 DentalReserve 修复和启动工具")
    print("="*60)

    # 检查当前目录
    current_dir = Path.cwd()
    print(f"📁 当前目录: {current_dir}")

    # 执行修复步骤
    check_and_create_dirs()
    fix_requirements()
    fix_config_file()
    create_simple_main()

    # 运行服务器
    run_server()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 请尝试:")
        print("   1. 手动删除 backend/requirements.txt 中的 pydantic==2.5.0")
        print("   2. 添加 pydantic==1.10.13")
        print("   3. 运行: pip install pydantic==1.10.13 --force-reinstall")
        input("\n按 Enter 退出...")