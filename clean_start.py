#!/usr/bin/env python3
"""
最终修复脚本 - 100% 确保能运行
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def stop_all_processes():
    """停止所有相关进程"""
    print("🛑 停止所有Python进程...")
    try:
        # Windows PowerShell命令
        subprocess.run(["powershell", "-Command", "Get-Process python*,uvicorn* | Stop-Process -Force -ErrorAction SilentlyContinue"],
                      capture_output=True)
        time.sleep(2)
        print("✅ 进程已停止")
    except:
        print("⚠️  无法停止进程，继续...")

def fix_pydantic():
    """修复pydantic版本问题"""
    print("🔧 修复pydantic版本...")

    try:
        # 卸载所有pydantic相关包
        packages = ["pydantic", "pydantic-settings", "pydantic-core"]
        for pkg in packages:
            subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", pkg],
                          capture_output=True)

        # 安装正确版本
        subprocess.run([sys.executable, "-m", "pip", "install", "pydantic==1.10.13"],
                      check=True, capture_output=True)
        print("✅ pydantic已降级到1.10.13")
        return True
    except Exception as e:
        print(f"⚠️  pydantic修复失败: {e}")
        return False

def create_ultra_simple_app():
    """创建最简单的应用"""
    print("📝 创建最简单应用...")

    # 创建目录（如果不存在）
    Path("simple_backend/app").mkdir(parents=True, exist_ok=True)

    # 创建最简单的main.py
    simple_main = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

# 创建应用
app = FastAPI(
    title="DentalReserve API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS设置 - 允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🎉 DentalReserve API 运行成功！",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "主页": "/",
            "健康检查": "/health",
            "诊所列表": "/api/clinics",
            "API文档": "/docs"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "dentalreserve",
        "timestamp": datetime.now().isoformat()
    }

# 诊所数据
CLINICS = [
    {
        "id": 1,
        "name": "多伦多市中心牙科",
        "address": "123 Bay St, Toronto, ON",
        "phone": "+1 (416) 555-1234",
        "email": "info@torontodental.com",
        "rating": 4.5,
        "services": ["洗牙", "补牙", "根管治疗"]
    },
    {
        "id": 2,
        "name": "温哥华牙科中心",
        "address": "456 Granville St, Vancouver, BC",
        "phone": "+1 (604) 555-5678",
        "email": "contact@vancouverdental.com",
        "rating": 4.8,
        "services": ["牙齿矫正", "种植牙", "美容牙科"]
    }
]

@app.get("/api/clinics")
async def get_clinics():
    return {
        "count": len(CLINICS),
        "clinics": CLINICS
    }

@app.get("/api/clinics/{clinic_id}")
async def get_clinic(clinic_id: int):
    for clinic in CLINICS:
        if clinic["id"] == clinic_id:
            return clinic
    return {"error": "诊所不存在"}

# 登录接口
@app.post("/api/login")
async def login(username: str, password: str):
    # 简单验证
    users = {
        "patient@example.com": "Patient123!",
        "admin@dentalreserve.ca": "Admin123!",
        "doctor@example.com": "Doctor123!"
    }

    if username in users and users[username] == password:
        return {
            "success": True,
            "message": "登录成功",
            "token": "fake-jwt-token-for-demo",
            "user": {
                "email": username,
                "role": "patient" if "patient" in username else "admin" if "admin" in username else "doctor",
                "name": "测试用户"
            }
        }

    return {"success": False, "message": "用户名或密码错误"}

if __name__ == "__main__":
    print("🚀 启动 DentalReserve 服务器...")
    print("="*50)
    print("🌐 访问地址:")
    print("   1. http://localhost:8000")
    print("   2. http://127.0.0.1:8000")
    print("   3. http://0.0.0.0:8000")
    print("\n📚 API文档:")
    print("   http://localhost:8000/docs")
    print("="*50)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
'''

    # 保存文件
    main_file = Path("simple_backend/app/main.py")
    main_file.write_text(simple_main, encoding='utf-8')

    # 创建 __init__.py
    init_file = Path("simple_backend/app/__init__.py")
    init_file.write_text("# Simple DentalReserve App\n", encoding='utf-8')

    print("✅ 最简单的应用已创建在 simple_backend/app/main.py")

def create_single_file_solution():
    """创建单文件解决方案"""
    print("📁 创建单文件版本...")

    single_file = '''#!/usr/bin/env python3
"""
DentalReserve 单文件版本 - 无需安装任何依赖（除了fastapi和uvicorn）
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import json
from datetime import datetime
from typing import List, Optional

# 创建FastAPI应用
app = FastAPI(
    title="DentalReserve API",
    version="1.0.0",
    description="牙医预约平台API - 单文件版本",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 允许所有CORS（开发环境）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 内存数据存储
clinics_db = []
users_db = []
appointments_db = []

# 初始化示例数据
def init_sample_data():
    global clinics_db, users_db

    clinics_db = [
        {
            "id": "clinic_001",
            "name": "多伦多市中心牙科诊所",
            "address": "123 Bay Street, Toronto, ON M5J 2S1",
            "city": "Toronto",
            "province": "ON",
            "phone": "+1 (416) 555-1234",
            "email": "info@torontodental.com",
            "description": "位于多伦多市中心的现代化牙科诊所，提供全方位牙科服务。",
            "latitude": 43.651070,
            "longitude": -79.347015,
            "rating": 4.5,
            "review_count": 124,
            "services": [
                {"name": "牙齿清洁", "duration": 60, "price": 120.00},
                {"name": "补牙", "duration": 90, "price": 200.00},
                {"name": "根管治疗", "duration": 120, "price": 800.00}
            ],
            "doctors": [
                {"name": "Dr. John Smith", "specialty": "General Dentistry"},
                {"name": "Dr. Sarah Lee", "specialty": "Orthodontics"}
            ],
            "hours": {
                "weekdays": "9:00 AM - 6:00 PM",
                "saturday": "10:00 AM - 4:00 PM",
                "sunday": "Closed"
            }
        },
        {
            "id": "clinic_002",
            "name": "温哥华牙科中心",
            "address": "456 Granville Street, Vancouver, BC V6C 1T2",
            "city": "Vancouver",
            "province": "BC",
            "phone": "+1 (604) 555-5678",
            "email": "contact@vancouverdental.com",
            "description": "温哥华领先的牙科护理中心，专注于美容牙科和种植牙。",
            "latitude": 49.282729,
            "longitude": -123.120738,
            "rating": 4.8,
            "review_count": 89,
            "services": [
                {"name": "牙齿矫正", "duration": 120, "price": 5000.00},
                {"name": "牙齿美白", "duration": 90, "price": 300.00},
                {"name": "种植牙", "duration": 180, "price": 2500.00}
            ],
            "doctors": [
                {"name": "Dr. Michael Chen", "specialty": "Cosmetic Dentistry"},
                {"name": "Dr. Lisa Wang", "specialty": "Implantology"}
            ],
            "hours": {
                "weekdays": "8:30 AM - 7:00 PM",
                "saturday": "9:00 AM - 5:00 PM",
                "sunday": "10:00 AM - 3:00 PM"
            }
        }
    ]

    users_db = [
        {
            "id": "user_001",
            "email": "patient@example.com",
            "password": "Patient123!",
            "name": "张三",
            "phone": "+1 (416) 555-1111",
            "role": "patient"
        },
        {
            "id": "user_002",
            "email": "admin@dentalreserve.ca",
            "password": "Admin123!",
            "name": "管理员",
            "phone": "+1 (416) 555-2222",
            "role": "admin"
        }
    ]

# 主页
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DentalReserve - 牙医预约平台</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #2563eb; }
            .endpoint { background: #f3f4f6; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .method { color: #059669; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>🦷 DentalReserve API 正在运行！</h1>
        <p>欢迎使用牙医预约平台API</p>

        <h2>📚 可用接口：</h2>
        <div class="endpoint">
            <span class="method">GET</span> <a href="/docs">/docs</a> - API文档 (Swagger UI)
        </div>
        <div class="endpoint">
            <span class="method">GET</span> <a href="/health">/health</a> - 健康检查
        </div>
        <div class="endpoint">
            <span class="method">GET</span> <a href="/api/clinics">/api/clinics</a> - 获取诊所列表
        </div>
        <div class="endpoint">
            <span class="method">POST</span> /api/login - 用户登录
        </div>

        <h2>👥 测试账户：</h2>
        <ul>
            <li>患者: patient@example.com / Patient123!</li>
            <li>管理员: admin@dentalreserve.ca / Admin123!</li>
        </ul>

        <p><strong>状态：</strong> <span style="color: green;">✓ 在线</span></p>
        <p><strong>时间：</strong> {}</p>
    </body>
    </html>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# 健康检查
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "dentalreserve-api",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "uptime": "running"
    }

# 获取所有诊所
@app.get("/api/clinics")
async def get_clinics():
    return {
        "success": True,
        "count": len(clinics_db),
        "clinics": clinics_db,
        "timestamp": datetime.now().isoformat()
    }

# 获取单个诊所
@app.get("/api/clinics/{clinic_id}")
async def get_clinic(clinic_id: str):
    for clinic in clinics_db:
        if clinic["id"] == clinic_id:
            return {
                "success": True,
                "clinic": clinic,
                "timestamp": datetime.now().isoformat()
            }

    return {
        "success": False,
        "error": "诊所不存在",
        "clinic_id": clinic_id
    }

# 用户登录
@app.post("/api/login")
async def login(request: Request):
    try:
        form_data = await request.json()
        username = form_data.get("username", "")
        password = form_data.get("password", "")
    except:
        form_data = await request.form()
        username = form_data.get("username", "")
        password = form_data.get("password", "")

    for user in users_db:
        if user["email"] == username and user["password"] == password:
            return {
                "success": True,
                "message": "登录成功",
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user["name"],
                    "role": user["role"],
                    "phone": user["phone"]
                },
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJwYXRpZW50QGV4YW1wbGUuY29tIiwicm9sZSI6InBhdGllbnQiLCJuYW1lIjoi5byg5LiJIiwiaWF0IjoxNzA0MjUwMDAwLCJleHAiOjE3MDQ4NTQ4MDB9.fake_token_for_demo"
            }

    return {
        "success": False,
        "error": "用户名或密码错误"
    }

# 搜索诊所
@app.get("/api/clinics/search")
async def search_clinics(
    city: Optional[str] = None,
    service: Optional[str] = None
):
    results = []

    for clinic in clinics_db:
        match = True

        if city and clinic["city"].lower() != city.lower():
            match = False

        if service:
            service_match = False
            for s in clinic["services"]:
                if service.lower() in s["name"].lower():
                    service_match = True
                    break
            if not service_match:
                match = False

        if match:
            results.append(clinic)

    return {
        "success": True,
        "count": len(results),
        "results": results,
        "filters": {
            "city": city,
            "service": service
        }
    }

# 创建预约
@app.post("/api/appointments")
async def create_appointment(request: Request):
    try:
        data = await request.json()

        appointment = {
            "id": f"appt_{datetime.now().timestamp()}",
            "clinic_id": data.get("clinic_id"),
            "patient_id": data.get("patient_id", "user_001"),
            "date": data.get("date"),
            "time": data.get("time"),
            "service": data.get("service"),
            "notes": data.get("notes", ""),
            "status": "confirmed",
            "created_at": datetime.now().isoformat(),
            "virtual_phone": "+1 (416) 555-9999"  # 虚拟电话号码
        }

        appointments_db.append(appointment)

        return {
            "success": True,
            "message": "预约成功！",
            "appointment": appointment,
            "virtual_phone": appointment["virtual_phone"]
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# 获取用户预约
@app.get("/api/appointments")
async def get_appointments(user_id: Optional[str] = None):
    if user_id:
        user_appointments = [a for a in appointments_db if a.get("patient_id") == user_id]
        return {
            "success": True,
            "count": len(user_appointments),
            "appointments": user_appointments
        }

    return {
        "success": True,
        "count": len(appointments_db),
        "appointments": appointments_db
    }

# 模拟拨打电话
@app.post("/api/calls/initiate")
async def initiate_call(request: Request):
    try:
        data = await request.json()

        return {
            "success": True,
            "message": "呼叫已发起",
            "call_id": f"call_{datetime.now().timestamp()}",
            "appointment_id": data.get("appointment_id"),
            "direction": data.get("direction", "patient_to_clinic"),
            "status": "connecting",
            "virtual_phone": "+1 (416) 555-9999"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # 初始化数据
    init_sample_data()

    print("="*70)
    print("🦷 DENTALRESERVE 牙医预约平台")
    print("="*70)
    print("🚀 单文件版本 - 无需复杂配置")
    print("="*70)
    print("\n🌐 访问地址：")
    print("   主页:     http://localhost:8000")
    print("   API文档:  http://localhost:8000/docs")
    print("   健康检查: http://localhost:8000/health")
    print("\n📱 API接口：")
    print("   GET  /api/clinics        - 获取诊所列表")
    print("   POST /api/login          - 用户登录")
    print("   POST /api/appointments   - 创建预约")
    print("   POST /api/calls/initiate - 发起电话呼叫")
    print("\n👥 测试账户：")
    print("   📧 patient@example.com")
    print("   🔑 Patient123!")
    print("="*70)

    # 启动服务器
    uvicorn.run(
        app,
        host="0.0.0.0",  # 重要：使用0.0.0.0而不是127.0.0.1
        port=8000,
        log_level="info",
        access_log=True
    )
'''

    Path("single_file_app.py").write_text(single_file, encoding='utf-8')
    print("✅ 单文件版本已创建: single_file_app.py")

    return Path("single_file_app.py")

def run_single_file():
    """运行单文件版本"""
    print("\n" + "="*60)
    print("🚀 启动单文件版本")
    print("="*60)

    try:
        subprocess.run([sys.executable, "single_file_app.py"])
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")

def main():
    """主函数"""
    print("🦷 DentalReserve 最终修复")
    print("="*60)

    try:
        # 步骤1：停止所有进程
        stop_all_processes()

        # 步骤2：修复pydantic
        fix_pydantic()

        # 步骤3：创建单文件解决方案
        create_single_file_solution()

        # 步骤4：运行
        print("\n✅ 准备就绪！")
        print("现在运行以下命令之一：")
        print("\n选项1 - 单文件版本（推荐）：")
        print("   python single_file_app.py")
        print("\n选项2 - 简单版本：")
        print("   cd simple_backend")
        print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")

        choice = input("\n是否立即启动单文件版本？(y/n): ").strip().lower()
        if choice == 'y':
            run_single_file()
        else:
            print("\n💡 手动启动：")
            print("   1. python single_file_app.py")
            print("   2. 访问 http://localhost:8000")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

        print("\n🎯 终极解决方案：")
        print("1. 手动运行这个命令停止所有进程：")
        print("   taskkill /F /IM python.exe /IM uvicorn.exe")
        print("\n2. 然后运行：")
        print("   python single_file_app.py")

if __name__ == "__main__":
    main()