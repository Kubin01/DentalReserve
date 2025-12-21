#!/usr/bin/env python3
"""
DentalReserve 单文件启动器
解决所有导入和路径问题
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os

# 创建应用实例
app = FastAPI(
    title="DentalReserve API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 允许所有CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根路由
@app.get("/")
def root():
    return {
        "message": "🎉 DentalReserve API 运行成功！",
        "status": "online",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "clinics": "/api/clinics"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy", "service": "dentalreserve"}

# 模拟诊所数据
clinics = [
    {
        "id": 1,
        "name": "多伦多市中心牙科诊所",
        "address": "123 Bay St, Toronto",
        "phone": "+1-416-555-1234",
        "rating": 4.5
    },
    {
        "id": 2,
        "name": "温哥华牙科中心",
        "address": "456 Granville St, Vancouver",
        "phone": "+1-604-555-5678",
        "rating": 4.8
    }
]

@app.get("/api/clinics")
def get_clinics():
    return {"clinics": clinics}

@app.get("/api/clinics/{clinic_id}")
def get_clinic(clinic_id: int):
    for clinic in clinics:
        if clinic["id"] == clinic_id:
            return clinic
    return {"error": "诊所不存在"}

def main():
    """主函数"""
    print("=" * 60)
    print("🦷 DentalReserve 牙医预约平台")
    print("=" * 60)
    print(f"🐍 Python 版本: {sys.version}")
    print(f"📁 当前目录: {os.getcwd()}")
    print("🚀 启动服务器...")
    print("\n🌐 访问地址:")
    print("   1. http://localhost:8000")
    print("   2. http://127.0.0.1:8000")
    print("   3. http://0.0.0.0:8000")
    print("\n📚 API文档:")
    print("   http://localhost:8000/docs")
    print("=" * 60)

    # 启动服务器
    uvicorn.run(
        app=app,  # 直接传入app实例，避免导入问题
        host="0.0.0.0",  # 重要！使用 0.0.0.0 而不是 127.0.0.1
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 请检查：")
        print("   1. 端口8000是否被占用")
        print("   2. 是否有权限运行")
        print("   3. Python环境是否正常")