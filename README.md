# OpenAI兼容的Sora API服务

这是一个为Sora提供OpenAI兼容接口的API服务。该服务使用cloudscraper绕过Cloudflare验证，支持多key轮询、并发处理和标准的OpenAI接口格式。

## 功能特点

- **OpenAI兼容接口**：完全兼容OpenAI的`/v1/chat/completions`接口
- **CF验证绕过**：使用cloudscraper库成功绕过Cloudflare验证
- **多key轮询**：支持多个Sora认证token，根据权重和速率限制智能选择
- **并发处理**：支持多个并发请求
- **流式响应**：支持SSE格式的流式响应
- **图像处理**：支持文本到图像生成和图像到图像生成（Remix）
- **异步处理**：支持异步生成图像，返回立即响应，防止请求超时
- **状态查询**：提供API端点查询异步任务的状态和结果
- **优化性能**：经过代码优化，提高请求处理速度和资源利用率
- **健康检查**：支持容器健康检查功能

## 环境要求

- Python 3.8+
- FastAPI 0.95.0+
- cloudscraper 1.2.71+
- 其他依赖见requirements.txt

## 快速部署指南


你可以直接运行不指定任何环境变量，所有环境变量都可以在面板里面配置


管理员登录密钥默认：sk-123456


api请求密钥不设置默认和管理员登录密钥相同


docker 一键运行
   ```bash
   docker run -d -p 8890:8890 --name sora-api 1hei1/sora-api:latest
   ```



### 方法一：直接运行

1. 克隆仓库
   ```bash
   git clone https://github.com/1hei1/sora-api.git
   cd sora-api
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置API Keys（两种方式）
   - **方式1**: 创建api_keys.json文件
     ```json
     [
       {"key": "Bearer your-sora-token-1", "weight": 1, "max_rpm": 60},
       {"key": "Bearer your-sora-token-2", "weight": 2, "max_rpm": 60}
     ]
     ```
   - **方式2**: 设置环境变量
     ```bash
     # Linux/macOS
     export API_KEYS='[{"key": "Bearer your-sora-token-1", "weight": 1, "max_rpm": 60}, {"key": "Bearer your-sora-token-2", "weight": 2, "max_rpm": 60}]'  
     
     # Windows (PowerShell)
     $env:API_KEYS='[{"key": "Bearer your-sora-token-1", "weight": 1, "max_rpm": 60}, {"key": "Bearer your-sora-token-2", "weight": 2, "max_rpm": 60}]'
     
     # Windows (CMD)
     set API_KEYS=[{"key": "Bearer your-sora-token-1", "weight": 1, "max_rpm": 60}, {"key": "Bearer your-sora-token-2", "weight": 2, "max_rpm": 60}]  
     ```

4. 配置代理（可选，如果需要）
   ```bash
   # Linux/macOS - 基本代理
   export PROXY_HOST=127.0.0.1
   export PROXY_PORT=7890
   
   # Linux/macOS - 带认证的代理
   export PROXY_HOST=127.0.0.1
   export PROXY_PORT=7890
   export PROXY_USER=username
   export PROXY_PASS=password
   
   # Windows (PowerShell) - 基本代理
   $env:PROXY_HOST="127.0.0.1"
   $env:PROXY_PORT="7890"
   
   # Windows (PowerShell) - 带认证的代理
   $env:PROXY_HOST="127.0.0.1"
   $env:PROXY_PORT="7890"
   $env:PROXY_USER="username"
   $env:PROXY_PASS="password"
   
   # Windows (CMD) - 基本代理
   set PROXY_HOST=127.0.0.1
   set PROXY_PORT=7890
   
   # Windows (CMD) - 带认证的代理
   set PROXY_HOST=127.0.0.1
   set PROXY_PORT=7890
   set PROXY_USER=username
   set PROXY_PASS=password
   ```

5. 启动服务
   ```bash
   python run.py
   ```

6. 访问服务
   - API服务地址: http://localhost:8890
   - 后台管理面板: http://localhost:8890/admin

### 方法二：Docker部署

1. 构建Docker镜像
   ```bash
   docker build -t sora-api .
   ```

2. 运行Docker容器（不同配置选项）

   **基本运行方式**:
   ```bash
   docker run -d -p 8890:8890 --name sora-api sora-api
   ```

   **使用预打包镜像**:
   ```bash
   docker run -d -p 8890:8890 --name sora-api 1hei1/sora-api:latest
   ```

   **使用预打包镜像并配置API密钥**:
   ```bash
   docker run -d -p 8890:8890 \
     -e API_KEYS='[{"key": "Bearer your-sora-token-1", "weight": 1, "max_rpm": 60}, {"key": "Bearer your-sora-token-2", "weight": 2, "max_rpm": 60}]' \
     --name sora-api \
     1hei1/sora-api:v0.1
   ```

   **使用预打包镜像并配置代理**:
   ```bash
   docker run -d -p 8890:8890 \
     -e API_KEYS='[{"key": "Bearer your-sora-token-1", "weight": 1, "max_rpm": 60}]' \
     -e PROXY_HOST=host.docker.internal \
     -e PROXY_PORT=7890 \
     --name sora-api \
     1hei1/sora-api:v0.1
   ```

   **带API密钥配置**:
   ```bash
   docker run -d -p 8890:8890 \
     -e API_KEYS='[{"key": "Bearer your-sora-token-1", "weight": 1, "max_rpm": 60}, {"key": "Bearer your-sora-token-2", "weight": 2, "max_rpm": 60}]' \
     --name sora-api \
     sora-api
   ```

   **带基本代理配置**:
   ```bash
   docker run -d -p 8890:8890 \
     -e API_KEYS='[{"key": "Bearer your-sora-token-1", "weight": 1, "max_rpm": 60}]' \
     -e PROXY_HOST=host.docker.internal \
     -e PROXY_PORT=7890 \
     --name sora-api \
     sora-api
   ```

   **带认证代理配置**:
   ```bash
   docker run -d -p 8890:8890 \
     -e API_KEYS='[{"key": "Bearer your-sora-token-1", "weight": 1, "max_rpm": 60}]' \
     -e PROXY_HOST=host.docker.internal \
     -e PROXY_PORT=7890 \
     -e PROXY_USER=username \
     -e PROXY_PASS=password \
     --name sora-api \
     sora-api
   ```

   **使用外部配置文件**:
   ```bash
   # 首先确保api_keys.json文件已正确配置
   docker run -d -p 8890:8890 \
     -v $(pwd)/api_keys.json:/app/api_keys.json \
     -e PROXY_HOST=host.docker.internal \
     -e PROXY_PORT=7890 \
     --name sora-api \
     sora-api
   ```

   **挂载本地目录保存图片**:
   ```bash
   docker run -d -p 8890:8890 \
     -v /your/local/path:/app/src/static/images \
     --name sora-api \
     sora-api
   ```

   **启用详细日志**:
   ```bash
   docker run -d -p 8890:8890 \
     -e API_KEYS='[{"key": "Bearer your-sora-token-1", "weight": 1, "max_rpm": 60}]' \
     -e VERBOSE_LOGGING=true \
     --name sora-api \
     sora-api
   ```

   **注意**: 在Docker中使用宿主机代理时，请使用`host.docker.internal`而不是`127.0.0.1`作为代理主机地址。

3. 检查容器状态
   ```bash
   docker ps
   docker logs sora-api
   ```

4. 停止和移除容器
   ```bash
   docker stop sora-api
   docker rm sora-api
   ```

## 环境变量说明

| 环境变量 | 描述 | 默认值 | 示例 |
|---------|------|--------|------|
| `API_HOST` | API服务监听地址 | `0.0.0.0` | `127.0.0.1` |
| `API_PORT` | API服务端口 | `8890` | `9000` |
| `BASE_URL` | API基础URL（生成图片的时候需要用到） | `http://0.0.0.0:8890` | `https://api.example.com` |  
| `PROXY_HOST` | HTTP代理主机 | 空（不使用代理） | `127.0.0.1` |
| `PROXY_PORT` | HTTP代理端口 | 空（不使用代理） | `7890` |
| `PROXY_USER` | HTTP代理用户名 | 空（不使用认证） | `username` |
| `PROXY_PASS` | HTTP代理密码 | 空（不使用认证） | `password` |
| `IMAGE_SAVE_DIR` | 图片保存目录 | `src/static/images` | `/data/images` |
| `IMAGE_LOCALIZATION` | 是否启用图片本地化 | `False` | `True` |
| `ADMIN_KEY` | 管理员API密钥（登录界面输入的密码） | `sk-123456` | `sk-youradminkey` |
| `API_AUTH_TOKEN` | API认证令牌（使用api服务传入的key） | 空 | `your-auth-token` |
| `VERBOSE_LOGGING` | 是否启用详细日志 | `False` | `True` |

## API密钥配置说明

API密钥配置采用JSON格式，每个密钥包含以下属性：

- `key`: Sora认证令牌（必须包含Bearer前缀）
- `weight`: 轮询权重，数字越大被选中概率越高
- `max_rpm`: 每分钟最大请求数（速率限制）

示例:
```json
[
  {
    "key": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5MzQ0ZTY1LWJiYzktNDRkMS1hOWQwLWY5NTdiMDc5YmQwZSIsInR5cCI6IkpXVCJ9...",
    "weight": 1,
    "max_rpm": 60
  },
  {
    "key": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5MzQ0ZTY1LWJiYzktNDRkMS1hOWQwLWY5NTdiMDc5YmQwZSIsInR5cCI6IkpXVCJ9...",
    "weight": 2,
    "max_rpm": 60
  }
]
```

## 使用示例

### 使用curl发送请求

```bash
# 文本到图像请求（非流式）
curl -X POST http://localhost:8890/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "sora-1.0",
    "messages": [
      {"role": "user", "content": "生成一只在草地上奔跑的金毛犬"}
    ],
    "n": 1,
    "stream": false
  }'

# 文本到图像请求（流式）
curl -X POST http://localhost:8890/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "sora-1.0",
    "messages": [
      {"role": "user", "content": "生成一只在草地上奔跑的金毛犬"}
    ],
    "n": 1,
    "stream": true
  }'

# 查询异步任务状态
curl -X GET http://localhost:8890/v1/generation/chatcmpl-123456789abcdef \
  -H "Authorization: Bearer your-api-key"
```

## 常见问题排查

1. **连接超时或无法连接**
   - 检查代理配置是否正确
   - 如使用代理认证，确认用户名密码正确
   - 确认Sora服务器是否可用
   - 检查本地网络连接

2. **API密钥加载失败**
   - 确认api_keys.json格式正确
   - 检查环境变量API_KEYS是否正确设置
   - 查看日志中的错误信息

3. **图片生成失败**
   - 确认Sora令牌有效性
   - 查看日志中的错误信息
   - 检查是否超出账户额度限制

4. **Docker容器启动失败**
   - 检查端口是否被占用
   - 确认环境变量设置正确
   - 查看Docker日志中的错误信息
   
5. **环境变量API_AUTH_TOKEN和ADMIN_KEY的区别**
   - 环境变量 API_AUTH_TOKEN代表你在cheery studio 或者newapi里调用填写的令牌
   - 环境变量 ADMIN_KEY 代表你管理面板的登录密码
   - 当不设置API_AUTH_TOKE时 其值默认等于ADMIN_KEY的值
   
6. **环境变量BASE_URL的作用**
   - 这个是图片本地化时设置的，比如生成了一张图片，获取到图片原始url，由于有的客户端不能访问sora，所以要本地化，这个base_url就是指定本地化图片的url前缀。
   
6. **token无效**
   - 首次使用的token需要设置用户名，可以使用下面的脚本批量设置用户名：
 ```python
import random
import string
import logging
import cloudscraper

# Configure logging
tlogging = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Configuration ---
PROXY = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}
PROFILE_API = "https://sora.chatgpt.com/backend/me"
TOKENS_FILE = "tokens.txt"  # 每行一个 Bearer token
RESULTS_FILE = "update_results.txt"  # 保存更新结果
USERNAME_LENGTH = 8  # 随机用户名长度

# --- Utilities ---
def random_username(length: int = USERNAME_LENGTH) -> str:
    """生成全小写随机用户名"""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def sanitize_headers(headers: dict) -> dict:
    """
    移除所有非 Latin-1 字符，确保 headers 可以被底层 HTTP 库正确编码。
    """
    new = {}
    for k, v in headers.items():
        if isinstance(v, str):
            new[k] = v.encode('latin-1', 'ignore').decode('latin-1')
        else:
            new[k] = v
    return new


class SoraBatchUpdater:
    def __init__(self, proxy: dict = None):
        self.proxy = proxy or {}

    def update_username_for_token(self, token: str) -> tuple[bool, str]:
        """
        针对单个 Bearer token，生成随机用户名并发送更新请求。
        返回 (success, message)。
        """
        scraper = cloudscraper.create_scraper()
        if self.proxy:
            scraper.proxies = self.proxy

        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }
        headers = sanitize_headers(headers)

        new_username = random_username()
        payload = {"username": new_username}

        try:
            resp = scraper.post(
                PROFILE_API,
                headers=headers,
                json=payload,
                allow_redirects=False,
                timeout=15
            )
            status = resp.status_code
            if resp.ok:
                msg = f"OK ({new_username})"
                logging.info("Token %s: updated to %s", token[:6], new_username)
                return True, msg
            else:
                text = resp.text.replace('\n', '')
                msg = f"Failed {status}: {text}"  # 简要错误信息
                logging.warning("Token %s: %s", token[:6], msg)
                return False, msg
        except Exception as e:
            msg = str(e)
            logging.error("Token %s exception: %s", token[:6], msg)
            return False, msg

    def batch_update(self, tokens: list[str]) -> None:
        """
        对一组 Bearer token 批量更新用户名，并将结果写入 RESULTS_FILE。
        """
        results = []
        for token in tokens:
            success, message = self.update_username_for_token(token)
            results.append((token, success, message))

        # 写入结果文件
        with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
            for token, success, msg in results:
                status = 'SUCCESS' if success else 'ERROR'
                f.write(f"{token} ---- {status} ---- {msg}\n")
        logging.info("Batch update complete. Results saved to %s", RESULTS_FILE)


def load_tokens(filepath: str) -> list[str]:
    """从文件加载每行一个 token 的列表"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error("Tokens file not found: %s", filepath)
        return []


if __name__ == '__main__':
    tokens = load_tokens(TOKENS_FILE)
    if not tokens:
        logging.error("No tokens to update. Exiting.")
    else:
        updater = SoraBatchUpdater(proxy=PROXY)
        updater.batch_update(tokens)

```


## 性能优化

最新版本包含以下性能优化：

1. **代码重构**：简化了代码结构，提高可读性和可维护性
2. **内存优化**：减少不必要的内存使用，优化大型图像处理
3. **异步处理**：全面使用异步处理提高并发性能
4. **错误处理**：改进了错误处理和日志记录
5. **密钥管理**：优化了密钥轮询算法，提高了可靠性
6. **容器优化**：增强了Docker容器配置，支持健康检查

## 贡献

欢迎提交问题报告和改进建议！

## 许可证

MIT 
