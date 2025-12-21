from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import json
from datetime import datetime
from typing import Optional
import sys

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
        "hours": "周一至周五: 9:00 AM - 6:00 PM"
    },
    {
        "id": "2",
        "name": "Vancouver Dental Care",
        "address": "456 Granville Street, Vancouver, BC V6C 1T2",
        "phone": "+1 (604) 555-5678",
        "email": "contact@vancouverdental.com",
        "rating": 4.8,
        "services": ["牙齿矫正", "种植牙", "牙齿美白"],
        "hours": "周一至周六: 8:30 AM - 7:00 PM"
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

@app.get("/", response_class=HTMLResponse)
def home():
    """主页"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DentalReserve - 牙医预约平台</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            h1 {{ color: #2563eb; }}
            .status {{ background: #10b981; color: white; padding: 5px 10px; border-radius: 4px; }}
            .endpoint {{ background: #f3f4f6; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .method {{ color: #059669; font-weight: bold; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🦷 DentalReserve API</h1>
            <p><span class="status">✓ 在线</span> 服务正在运行</p>

            <h2>🌐 访问地址</h2>
            <ul>
                <li><a href="http://localhost:8000/docs" target="_blank">API文档 (Swagger)</a></li>
                <li><a href="http://localhost:8000/health" target="_blank">健康检查</a></li>
                <li><a href="http://localhost:8000/api/clinics" target="_blank">诊所列表</a></li>
            </ul>

            <h2>📡 API 接口</h2>
            <div class="endpoint">
                <span class="method">GET</span> <code>/</code> - 主页（当前页面）
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <code>/health</code> - 健康检查
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <code>/api/clinics</code> - 获取诊所列表
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <code>/api/clinics/{'{id}'}</code> - 获取诊所详情
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <code>/api/login</code> - 用户登录
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <code>/api/appointments</code> - 创建预约
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <code>/api/calls/initiate</code> - 发起电话
            </div>

            <h2>👥 测试账户</h2>
            <table border="1" cellpadding="10" cellspacing="0">
                <tr><th>邮箱</th><th>密码</th><th>角色</th></tr>
                <tr><td>patient@example.com</td><td>Patient123!</td><td>患者</td></tr>
                <tr><td>admin@dentalreserve.ca</td><td>Admin123!</td><td>管理员</td></tr>
                <tr><td>dr.smith@torontodental.com</td><td>Doctor123!</td><td>医生</td></tr>
            </table>

            <h2>📊 系统信息</h2>
            <p><strong>Python版本:</strong> {sys.version}</p>
            <p><strong>当前时间:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>诊所数量:</strong> {len(clinics_data)}</p>
            <p><strong>API状态:</strong> <span style="color: green;">正常</span></p>
        </div>
    </body>
    </html>
    """

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

    # 找到诊所
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

    # 生成虚拟电话号码
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
    # 找到预约
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

        # 城市筛选
        if city and city.lower() not in clinic.get("address", "").lower():
            match = False

        # 服务筛选
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
    print("🚀 立即启动版本 - 无需任何配置")
    print("="*70)
    print()
    print("🌐 服务器启动中...")
    print()
    print("📢 访问地址:")
    print("   主页:     http://localhost:8000")
    print("   API文档:  http://localhost:8000/docs")
    print("   备用地址: http://127.0.0.1:8000")
    print()
    print("📱 核心功能:")
    print("   • 诊所搜索和预约")
    print("   • 虚拟电话系统")
    print("   • 用户认证")
    print("   • 预约管理")
    print()
    print("👥 立即使用的测试账户:")
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
        print("\n💡 请尝试:")
        print("   1. 检查端口8000是否被占用")
        print("   2. 尝试其他端口: python dental_now.py --port 8080")

if __name__ == "__main__":
    main()