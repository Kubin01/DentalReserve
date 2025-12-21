#!/bin/bash
# start.sh
set -e

# 安装依赖
pip install -r requirements.txt

# 启动应用
uvicorn dental_now:app --host 0.0.0.0 --port ${PORT:-8000}