from fastapi import FastAPI, Request, Form, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from datetime import datetime
from typing import Optional
import sys
import os
from pathlib import Path

# 创建FastAPI应用
app = FastAPI(
    title="DentalReserve",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS设置 - 允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 设置静态文件目录
BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR)), name="static")

# 诊所数据
clinics_data = [
    {
        "id": "1",
        "name": "Toronto Downtown Dental",
        "address": "123 Bay Street, Toronto, ON M5J 2S1",
        "phone": "+1 (416) 555-1234",
        "email": "info@torontodental.com",
        "rating": 4.5,
        "services": ["洗牙", "补牙", "根管治疗"],
        "hours": "周一至周五: 9:00 AM - 6:00 PM",
        "city": "Toronto"
    },
    {
        "id": "2",
        "name": "Vancouver Dental Care",
        "address": "456 Granville Street, Vancouver, BC V6C 1T2",
        "phone": "+1 (604) 555-5678",
        "email": "contact@vancouverdental.com",
        "rating": 4.8,
        "services": ["牙齿矫正", "种植牙", "牙齿美白"],
        "hours": "周一至周六: 8:30 AM - 7:00 PM",
        "city": "Vancouver"
    },
    {
        "id": "3",
        "name": "Montreal Dental Center",
        "address": "789 Saint Catherine Street, Montreal, QC H3B 1B5",
        "phone": "+1 (514) 555-9012",
        "email": "info@montrealdental.com",
        "rating": 4.6,
        "services": ["洗牙", "牙齿美白", "牙周治疗"],
        "hours": "周一至周五: 8:00 AM - 5:00 PM",
        "city": "Montreal"
    },
    {
        "id": "4",
        "name": "Calgary Family Dental",
        "address": "101 8th Avenue SW, Calgary, AB T2P 1B4",
        "phone": "+1 (403) 555-3456",
        "email": "info@calgarydental.com",
        "rating": 4.7,
        "services": ["儿童牙科", "补牙", "牙齿矫正"],
        "hours": "周一至周六: 9:00 AM - 8:00 PM",
        "city": "Calgary"
    }
]

# 用户数据
users_data = {
    "patient@example.com": {"password": "Patient123!", "name": "张三", "role": "patient"},
    "admin@dentalreserve.ca": {"password": "Admin123!", "name": "管理员", "role": "admin"},
    "dr.smith@torontodental.com": {"password": "Doctor123!", "name": "Dr. Smith", "role": "doctor"}
}

# 预约数据
appointments_data = []

# 会话管理
def create_session_token(email: str):
    """创建简单的会话令牌"""
    return f"session_{email}"

def verify_session_token(token: str):
    """验证会话令牌"""
    if token.startswith("session_"):
        email = token.replace("session_", "")
        return email if email in users_data else None
    return None

# 网页路由
@app.get("/", response_class=HTMLResponse)
async def home():
    """主页 - 使用提供的 index.html"""
    with open(BASE_DIR / "templates" / "index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/clinic-dashboard", response_class=HTMLResponse)
async def clinic_dashboard():
    """诊所后台管理页面"""
    with open(BASE_DIR / "templates" / "clinic_dashboard.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.get("/login", response_class=HTMLResponse)
async def login_page():
    """登录页面 - 使用主页的登录功能，不单独提供页面"""
    return RedirectResponse(url="/")

# API路由
@app.get("/health")
def health():
    """健康检查"""
    return {
        "status": "healthy",
        "service": "dentalreserve",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "clinics_count": len(clinics_data),
        "users_count": len(users_data)
    }

@app.get("/api/clinics")
def get_clinics():
    """获取诊所列表"""
    return {
        "success": True,
        "count": len(clinics_data),
        "clinics": clinics_data,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/clinics/{clinic_id}")
def get_clinic(clinic_id: str):
    """获取诊所详情"""
    for clinic in clinics_data:
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

@app.post("/api/login")
def login(username: str, password: str):
    """用户登录"""
    if username in users_data and users_data[username]["password"] == password:
        user = users_data[username]
        return {
            "success": True,
            "message": "登录成功",
            "user": {
                "email": username,
                "name": user["name"],
                "role": user["role"]
            },
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InBhdGllbnRAZXhhbXBsZS5jb20iLCJyb2xlIjoicGF0aWVudCJ9.fake_token_for_testing"
        }

    return {
        "success": False,
        "error": "用户名或密码错误"
    }

@app.get("/api/appointments")
def get_appointments(user_email: Optional[str] = None):
    """获取预约列表"""
    if user_email:
        user_appointments = [a for a in appointments_data if a.get("patient_email") == user_email]
        return {
            "success": True,
            "count": len(user_appointments),
            "appointments": user_appointments
        }

    return {
        "success": True,
        "count": len(appointments_data),
        "appointments": appointments_data
    }

@app.post("/api/appointments")
def create_appointment(
    clinic_id: str,
    date: str,
    time: str,
    service: str,
    patient_name: str,
    patient_email: str,
    patient_phone: str,
    notes: Optional[str] = None
):
    """创建预约"""
    import random

    clinic = None
    for c in clinics_data:
        if c["id"] == clinic_id:
            clinic = c
            break

    if not clinic:
        return {
            "success": False,
            "error": "诊所不存在"
        }

    virtual_phone = f"+1 (416) 555-{random.randint(1000, 9999)}"

    appointment = {
        "id": f"appt_{datetime.now().timestamp()}",
        "clinic_id": clinic_id,
        "clinic_name": clinic["name"],
        "date": date,
        "time": time,
        "service": service,
        "patient_name": patient_name,
        "patient_email": patient_email,
        "patient_phone": patient_phone,
        "virtual_phone": virtual_phone,
        "status": "confirmed",
        "notes": notes,
        "created_at": datetime.now().isoformat()
    }

    appointments_data.append(appointment)

    return {
        "success": True,
        "message": "预约成功！",
        "appointment": appointment,
        "virtual_phone": virtual_phone
    }

@app.post("/api/calls/initiate")
def initiate_call(appointment_id: str, direction: str = "patient_to_clinic"):
    """发起电话呼叫"""
    appointment = None
    for appt in appointments_data:
        if appt["id"] == appointment_id:
            appointment = appt
            break

    if not appointment:
        return {
            "success": False,
            "error": "预约不存在"
        }

    return {
        "success": True,
        "message": "呼叫已发起",
        "appointment_id": appointment_id,
        "direction": direction,
        "virtual_phone": appointment.get("virtual_phone"),
        "call_id": f"call_{datetime.now().timestamp()}",
        "status": "connecting"
    }

@app.get("/api/search")
def search_clinics(
    city: Optional[str] = None,
    service: Optional[str] = None
):
    """搜索诊所"""
    results = []

    for clinic in clinics_data:
        match = True

        if city and city.lower() not in clinic.get("address", "").lower():
            match = False

        if service:
            service_match = False
            for s in clinic.get("services", []):
                if service.lower() in s.lower():
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

def main():
    """主函数"""
    print("="*70)
    print("🦷 DENTALRESERVE 牙医预约平台")
    print("="*70)
    print("🚀 完整网页版本 - 已整合前端页面")
    print("="*70)
    print()
    print("📢 重要文件检查:")
    print("   ✓ index.html - 用户主页")
    print("   ✓ clinic_dashboard.html - 诊所后台")
    print("   ✓ dental_now.py - 后端服务")
    print()
    print("🌐 访问地址:")
    print("   用户主页:      http://localhost:8000")
    print("   诊所后台:      http://localhost:8000/clinic-dashboard")
    print("   API文档:       http://localhost:8000/docs")
    print()
    print("📱 功能特性:")
    print("   • 完整的用户预约界面 (index.html)")
    print("   • 诊所后台管理系统 (clinic_dashboard.html)")
    print("   • RESTful API 接口")
    print("   • 虚拟电话系统")
    print()
    print("👥 测试账户:")
    print("   患者: patient@example.com / Patient123!")
    print("   管理员: admin@dentalreserve.ca / Admin123!")
    print("   医生: dr.smith@torontodental.com / Doctor123!")
    print()
    print("="*70)
    print("🛑 按 Ctrl+C 停止服务器")
    print("="*70)

    try:
        # 启动服务器
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        print("\n💡 请确保以下文件在同一目录:")
        print("   • index.html")
        print("   • clinic_dashboard.html")
        print("   • dental_now.py")

if __name__ == "__main__":
    main()