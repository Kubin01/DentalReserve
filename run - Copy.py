#!/usr/bin/env python3
"""
DentalReserve 启动脚本
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def check_requirements():
    """检查Python版本和依赖"""
    import platform
    python_version = platform.python_version()
    print(f"🐍 Python版本: {python_version}")

    if sys.version_info < (3, 9):
        print("❌ 需要Python 3.9或更高版本")
        sys.exit(1)

    return True

def install_dependencies():
    """安装依赖"""
    print("📦 正在安装依赖...")

    requirements_file = BASE_DIR / "backend" / "requirements.txt"

    if not requirements_file.exists():
        print(f"❌ 依赖文件不存在: {requirements_file}")
        return False

    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install",
            "-r", str(requirements_file)
        ], check=True)
        print("✅ 依赖安装完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖安装失败")
        return False

def create_env_file():
    """创建环境变量文件"""
    env_file = BASE_DIR / ".env"

    if env_file.exists():
        print("✅ .env文件已存在")
        return True

    env_content = """# 数据库配置（文件存储，无需数据库）
DATA_DIR=./data

# JWT配置
SECRET_KEY=your-super-secret-jwt-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Twilio配置（可选，用于真实电话功能）
# TWILIO_ACCOUNT_SID=your_twilio_account_sid
# TWILIO_AUTH_TOKEN=your_twilio_auth_token
# TWILIO_PHONE_NUMBER=+14165551234

# 地图服务（可选）
# GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# 前端URL
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000

# 环境
ENVIRONMENT=development
DEBUG=true
"""

    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ 已创建 .env 文件")
        return True
    except Exception as e:
        print(f"❌ 创建 .env 文件失败: {e}")
        return False

def create_data_directory():
    """创建数据目录"""
    data_dir = BASE_DIR / "data"
    uploads_dir = BASE_DIR / "backend" / "uploads"

    for directory in [data_dir, uploads_dir]:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def start_backend():
    """启动后端服务"""
    print("🚀 正在启动后端服务...")

    backend_dir = BASE_DIR / "backend"
    os.chdir(backend_dir)

    # 使用uvicorn启动FastAPI应用
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload"
    ]

    try:
        subprocess.Popen(cmd)
        print("✅ 后端服务已启动: http://localhost:8000")
        print("📚 API文档: http://localhost:8000/docs")
        return True
    except Exception as e:
        print(f"❌ 启动后端服务失败: {e}")
        return False

def setup_frontend():
    """设置前端（如果存在）"""
    frontend_dir = BASE_DIR / "frontend"

    if frontend_dir.exists():
        print("🌐 检测到前端目录")

        # 检查package.json
        package_json = frontend_dir / "package.json"
        if package_json.exists():
            print("📦 前端依赖已配置")
            print("💡 提示：进入 frontend 目录运行 'npm start' 启动前端")
        else:
            print("⚠️  frontend/package.json 不存在")

    return True

def open_browser():
    """打开浏览器"""
    import time
    time.sleep(2)  # 等待服务启动

    urls = [
        "http://localhost:8000",
        "http://localhost:8000/docs",
    ]

    for url in urls:
        try:
            webbrowser.open(url)
            print(f"🌐 已打开: {url}")
        except:
            print(f"⚠️  无法打开浏览器: {url}")

def print_welcome():
    """打印欢迎信息"""
    print("\n" + "="*60)
    print("🦷 欢迎使用 DentalReserve 牙医预约平台")
    print("="*60)
    print("\n🔧 系统状态:")
    print(f"  后端API: http://localhost:8000")
    print(f"  API文档: http://localhost:8000/docs")
    print(f"  数据目录: {BASE_DIR / 'data'}")
    print("\n👥 测试账户:")
    print("  患者: patient@example.com / Patient123!")
    print("  医生: dr.smith@torontodental.com / Doctor123!")
    print("  管理员: admin@dentalreserve.ca / Admin123!")
    print("\n🚀 快速开始:")
    print("  1. 访问 http://localhost:8000/docs")
    print("  2. 使用测试账户登录")
    print("  3. 探索API接口")
    print("="*60 + "\n")

def main():
    """主函数"""
    print("🔧 DentalReserve 初始化...")

    # 检查Python版本
    if not check_requirements():
        return

    # 创建目录
    create_data_directory()

    # 创建.env文件
    if not create_env_file():
        return

    # 安装依赖
    if not install_dependencies():
        return

    # 设置前端
    setup_frontend()

    # 启动后端
    if not start_backend():
        return

    # 打印欢迎信息
    print_welcome()

    # 打开浏览器
    open_browser()

    print("✅ 初始化完成！按 Ctrl+C 停止服务")

if __name__ == "__main__":
    try:
        main()
        # 保持主线程运行
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)