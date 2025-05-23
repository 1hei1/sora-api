FROM python:3.10-slim

WORKDIR /app

# 设置Python环境
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p /app/src/static/images && \
    chmod -R 777 /app/src/static

# 暴露端口
EXPOSE 8890

# 设置健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8890/health || exit 1

# 启动应用
CMD ["python", "run.py"] 