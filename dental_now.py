from fastapi import FastAPI, Request, Form, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
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

# 设置基础目录 - 只定义一次
BASE_DIR = Path(__file__).parent

# 确保必要的目录存在
templates_dir = BASE_DIR / "templates"
static_dir = BASE_DIR / "static"

# 创建目录如果不存在
templates_dir.mkdir(exist_ok=True)
static_dir.mkdir(exist_ok=True)

# 设置静态文件目录
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

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
    try:
        index_path = templates_dir / "index.html"
        if not index_path.exists():
            print(f"⚠️ 警告: index.html 不存在于 {index_path}")
            # 返回一个简单的主页作为后备
            fallback_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>DentalReserve 牙医预约平台</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    h1 { color: #2563eb; }
                    .container { max-width: 800px; margin: 0 auto; }
                    .status { background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0; }
                    .links a { display: inline-block; margin: 10px; padding: 10px 20px; background: #2563eb; color: white; text-decoration: none; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🦷 DentalReserve 牙医预约平台</h1>
                    <p>欢迎使用牙医预约平台！系统正在运行中。</p>

                    <div class="status">
                        <h3>系统状态 ✅</h3>
                        <p>后端服务正常运行</p>
                        <p>时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
                        <p>服务版本: 1.0.0</p>
                    </div>

                    <div class="links">
                        <h3>快速访问:</h3>
                        <a href="/docs">API 文档</a>
                        <a href="/health">健康检查</a>
                        <a href="/clinic-dashboard">诊所后台</a>
                        <a href="/admin-dashboard">管理员后台</a>
                    </div>

                    <div style="margin-top: 30px; color: #666;">
                        <p>如果这是你第一次看到此页面，请确保已上传正确的模板文件。</p>
                        <p>📁 预期文件路径: <code>templates/index.html</code></p>
                    </div>
                </div>
            </body>
            </html>
            """
            return HTMLResponse(content=fallback_html)

        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        print(f"❌ 读取主页错误: {e}")
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>错误</title></head>
        <body>
            <h1>服务器错误</h1>
            <p>读取主页时发生错误: {str(e)}</p>
            <p>请检查 templates/index.html 文件是否存在。</p>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=500)

@app.get("/clinic-dashboard", response_class=HTMLResponse)
async def clinic_dashboard():
    """诊所后台管理页面"""
    try:
        clinic_path = templates_dir / "clinic_dashboard.html"
        if not clinic_path.exists():
            return HTMLResponse(content="<h1>诊所后台页面未找到</h1><p>请上传 clinic_dashboard.html 文件到 templates 目录</p>", status_code=404)

        with open(clinic_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        return HTMLResponse(content=f"<h1>错误</h1><p>{str(e)}</p>", status_code=500)

@app.get("/admin-dashboard", response_class=HTMLResponse)
async def admin_dashboard():
    """管理员后台页面"""
    try:
        admin_path = templates_dir / "admin_dashboard.html"
        if not admin_path.exists():
            return HTMLResponse(content="<h1>管理员后台页面未找到</h1><p>请上传 admin_dashboard.html 文件到 templates 目录</p>", status_code=404)

        with open(admin_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        return HTMLResponse(content=f"<h1>错误</h1><p>{str(e)}</p>", status_code=500)

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
        "users_count": len(users_data),
        "appointments_count": len(appointments_data),
        "environment": os.environ.get("RENDER", "development"),
        "port": os.environ.get("PORT", "8000")
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
def login(username: str = Form(...), password: str = Form(...)):
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
    clinic_id: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    service: str = Form(...),
    patient_name: str = Form(...),
    patient_email: str = Form(...),
    patient_phone: str = Form(...),
    notes: Optional[str] = Form(None)
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
def initiate_call(appointment_id: str = Form(...), direction: str = Form("patient_to_clinic")):
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

@app.get("/api/admin/stats")
def get_admin_stats():
    """获取管理员统计数据"""
    return {
        "success": True,
        "stats": {
            "total_clinics": len(clinics_data),
            "total_users": len(users_data),
            "total_appointments": len(appointments_data),
            "confirmed_appointments": len([a for a in appointments_data if a.get("status") == "confirmed"]),
            "cancelled_appointments": len([a for a in appointments_data if a.get("status") == "cancelled"]),
            "today_appointments": len([a for a in appointments_data if a.get("date") == datetime.now().strftime("%Y-%m-%d")])
        }
    }

@app.post("/api/admin/clinics")
def add_clinic(
    name: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    city: str = Form(...),
    services: str = Form(...),  # 逗号分隔的服务列表
    hours: str = Form("周一至周五: 9:00 AM - 6:00 PM"),
    rating: float = Form(4.5)
):
    """管理员添加新诊所"""
    new_clinic = {
        "id": str(len(clinics_data) + 1),
        "name": name,
        "address": address,
        "phone": phone,
        "email": email,
        "rating": rating,
        "services": [s.strip() for s in services.split(",")],
        "hours": hours,
        "city": city
    }

    clinics_data.append(new_clinic)

    return {
        "success": True,
        "message": "诊所添加成功",
        "clinic": new_clinic
    }

@app.delete("/api/admin/clinics/{clinic_id}")
def delete_clinic(clinic_id: str):
    """管理员删除诊所"""
    global clinics_data

    original_count = len(clinics_data)
    clinics_data = [c for c in clinics_data if c["id"] != clinic_id]

    if len(clinics_data) < original_count:
        return {
            "success": True,
            "message": "诊所删除成功",
            "clinic_id": clinic_id
        }
    else:
        return {
            "success": False,
            "error": "诊所不存在"
        }

@app.get("/api/admin/appointments")
def get_all_appointments():
    """管理员获取所有预约"""
    return {
        "success": True,
        "count": len(appointments_data),
        "appointments": appointments_data
    }

# 添加一个简单的根路由测试
@app.get("/test")
def test_route():
    """测试路由"""
    return {
        "message": "DentalReserve API 正在运行",
        "timestamp": datetime.now().isoformat(),
        "environment": "Render" if os.environ.get("RENDER") else "Local",
        "port": os.environ.get("PORT", "8000"),
        "directory": str(BASE_DIR)
    }

def main():
    """主函数 - 仅用于本地运行"""
    print("="*70)
    print("🦷 DENTALRESERVE 牙医预约平台")
    print("="*70)
    print(f"📁 当前目录: {BASE_DIR}")
    print(f"📁 Templates 目录: {templates_dir}")
    print(f"📁 Static 目录: {static_dir}")
    print("="*70)
    print("📢 本地运行命令: uvicorn dental_now:app --host 0.0.0.0 --port 8000")
    print("="*70)

    # 检查必要文件
    print("📂 文件检查:")
    print(f"  templates/index.html: {'✅ 存在' if (templates_dir / 'index.html').exists() else '❌ 缺失'}")
    print(f"  templates/clinic_dashboard.html: {'✅ 存在' if (templates_dir / 'clinic_dashboard.html').exists() else '❌ 缺失'}")
    print(f"  templates/admin_dashboard.html: {'✅ 存在' if (templates_dir / 'admin_dashboard.html').exists() else '❌ 缺失'}")
    print("="*70)

    # Render会自动启动，这里只用于本地测试
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"🚀 启动服务器在端口 {port}")
        if os.environ.get("RENDER") is None:
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=port,
                log_level="info",
                reload=True
            )
#        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        print(f"\n💡 调试信息:")
        print(f"   当前目录: {os.getcwd()}")
        print(f"   文件列表: {os.listdir('.')}")
        if os.path.exists("templates"):
            print(f"   templates 内容: {os.listdir('templates')}")

if __name__ == "__main__":
    main()
