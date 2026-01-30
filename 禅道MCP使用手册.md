# 禅道 MCP 服务器使用手册

## 目录
1. [概述](#概述)
2. [快速开始](#快速开始)
3. [配置指南](#配置指南)
4. [可用工具](#可用工具)
5. [使用示例](#使用示例)
6. [故障排除](#故障排除)
7. [附录](#附录)

---

## 概述

禅道 MCP 服务器是一个基于 Model Context Protocol (MCP) 的服务端实现，它允许 AI 助手（如 Claude、Kimi 等）通过标准化的接口与禅道项目管理系统进行交互。

### 功能特性

- 🔌 **完整 API 覆盖**：支持禅道 RESTful API 的所有核心功能
- 🛠 **20+ MCP 工具**：提供项目集、产品、项目、迭代、需求、任务、Bug、用户等管理功能
- 📚 **标准化接口**：遵循 MCP 协议，兼容所有支持 MCP 的 AI 客户端
- 🔐 **安全认证**：自动处理 Token 认证和刷新
- ⚡ **高效开发**：基于 Python 3.11+ 和异步架构

### 支持的禅道实体

| 实体 | 操作 |
|------|------|
| 项目集 (Program) | 查询、创建、更新、删除 |
| 产品 (Product) | 查询、创建、更新、删除、获取需求列表、获取 Bug 列表 |
| 项目 (Project) | 查询、创建、更新、删除、获取执行列表 |
| 执行/迭代 (Execution) | 查询、创建、更新、删除、获取需求列表、获取任务列表 |
| 需求 (Story) | 查询、创建、更新、删除、变更 |
| 任务 (Task) | 查询、创建、更新、删除 |
| Bug | 查询、创建、更新、删除 |
| 用户 (User) | 查询、获取当前用户信息 |

---

## 快速开始

### 环境要求

- **Python 3.11** 或更高版本
- **UV 包管理器**（推荐）或 pip
- **禅道服务器** 访问权限（版本 15.x+）

### 第一步：安装 UV 包管理器

UV 是一个超快的 Python 包管理器，比 pip 快 10-100 倍。

#### Windows 用户

**使用 PowerShell（推荐）：**

```powershell
# 管理员权限运行 PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**或使用 scoop：**

```powershell
scoop install uv
```

**或使用 pip：**

```cmd
pip install uv
```

#### macOS/Linux 用户

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**验证安装：**

```bash
uv --version  # 应输出版本号如 uv 0.1.0
```

### 第二步：克隆/下载项目并安装依赖

#### 使用 UV（推荐）

```bash
# Windows PowerShell
cd C:\development\Projects\mcp
uv sync

# macOS/Linux
cd /path/to/mcp
uv sync
```

**UV 的优势：**
- 自动创建虚拟环境
- 自动安装所有依赖
- 自动锁定版本（保证可重现构建）
- 速度快 10 倍

#### 使用 pip 作为备选

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 第三步：配置环境变量

创建 `.env` 文件并配置禅道服务器信息：

```bash
# 复制示例文件
cp .env.example .env  # macOS/Linux
copy .env.example .env  # Windows cmd

# 或手动创建 .env，内容如下：
```

编辑 `.env` 文件（禅道登录凭证）：

```env
# 禅道服务器地址（去掉末尾的 /）
ZENTAO_BASE_URL=http://172.16.0.193:8088

# 禅道登录账号
ZENTAO_USERNAME=your_username

# 禅道登录密码
ZENTAO_PASSWORD=your_password
```

**⚠️ 安全提示：**
- 不要将 `.env` 提交到 Git（应已在 `.gitignore` 中）
- 不要在多人环境中共享明文密码，考虑使用环境变量或 secrets 管理

### 第四步：本地测试连接

```bash
# 使用 UV 运行
uv run python run_zentao_mcp.py

# 或先激活虚拟环境再运行
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python run_zentao_mcp.py
```

**正常输出示例：**
```
INFO: Zentao MCP Server initialized
INFO: Ready to accept connections
```

按 `Ctrl+C` 停止服务

---

## 配置指南

### 环境变量说明

| 变量名 | 必填 | 说明 | 示例 |
|--------|------|------|------|
| `ZENTAO_BASE_URL` | 是 | 禅道服务器地址（去掉末尾的 `/`） | `http://172.16.0.193:8088` |
| `ZENTAO_USERNAME` | 是 | 禅道登录账号 | `jiangyong` |
| `ZENTAO_PASSWORD` | 是 | 禅道登录密码 | `your_password` |

### MCP 客户端配置详解

MCP 配置的关键是找到正确的 Python 可执行文件路径和 MCP 服务脚本路径。以下为各种情况的配置方案：

#### 配置原理

MCP 配置需要指定：
- **command**: Python 可执行文件的完整路径
- **args**: MCP 服务脚本的完整路径
- **env**: 环境变量（禅道认证信息）

#### 确定 Python 路径

##### 使用 UV 的情况

如果用 `uv sync` 创建的虚拟环境，Python 路径为：

```bash
# Windows
uv python find  # 查看 Python 路径
# 或手动查找：项目目录\.venv\Scripts\python.exe

# macOS/Linux
uv python find
# 或：项目目录/.venv/bin/python
```

##### 自己创建虚拟环境的情况

```bash
# Windows
# 路径：项目目录\.venv\Scripts\python.exe

# macOS/Linux
# 路径：项目目录/.venv/bin/python
```

##### 使用全局 Python 的情况

```bash
# 查找 Python 路径
which python3     # macOS/Linux
where python      # Windows PowerShell
python -c "import sys; print(sys.executable)"  # 所有平台通用
```

#### Kimi Code CLI 配置

配置文件位置：`~/.kimi/mcp.json`

**Windows 示例（使用 UV）：**

```json
{
  "mcpServers": {
    "zentao": {
      "command": "your\\path\\mcp\\.venv\\Scripts\\python.exe",
      "args": ["your\\path\\mcp\\run_zentao_mcp.py"],
      "env": {
        "ZENTAO_BASE_URL": "http://172.16.0.193:8088",
        "ZENTAO_USERNAME": "your_username",
        "ZENTAO_PASSWORD": "your_password"
      }
    }
  }
}
```

**macOS/Linux 示例：**

```json
{
  "mcpServers": {
    "zentao": {
      "command": "/Users/yourname/projects/mcp/.venv/bin/python",
      "args": ["/Users/yourname/projects/mcp/run_zentao_mcp.py"],
      "env": {
        "ZENTAO_BASE_URL": "http://172.16.0.193:8088",
        "ZENTAO_USERNAME": "your_username",
        "ZENTAO_PASSWORD": "your_password"
      }
    }
  }
}
```

**验证配置：**

```bash
# 列出 MCP 服务器
kimi mcp list

# 测试连接
kimi mcp test zentao

# 查看日志
kimi mcp logs zentao
```

#### Claude Desktop 配置

配置文件位置：
- **Windows**: `%APPDATA%\Claude\settings.json`
  - 或直接输入：`C:\Users\{username}\AppData\Roaming\Claude\settings.json`
- **macOS**: `~/Library/Application Support/Claude/settings.json`
- **Linux**: `~/.config/Claude/settings.json`

**Windows 完整配置示例：**

```json
{
  "mcpServers": {
    "zentao": {
      "command": "your\\path\\mcp\\.venv\\Scripts\\python.exe",
      "args": ["your\\path\\mcp\\run_zentao_mcp.py"],
      "env": {
        "ZENTAO_BASE_URL": "http://172.16.0.193:8088",
        "ZENTAO_USERNAME": "your_username",
        "ZENTAO_PASSWORD": "your_password"
      }
    }
  }
}
```

**macOS 完整配置示例：**

```json
{
  "mcpServers": {
    "zentao": {
      "command": "/Users/yourname/projects/mcp/.venv/bin/python",
      "args": ["/Users/yourname/projects/mcp/run_zentao_mcp.py"],
      "env": {
        "ZENTAO_BASE_URL": "http://172.16.0.193:8088",
        "ZENTAO_USERNAME": "your_username",
        "ZENTAO_PASSWORD": "your_password"
      }
    }
  }
}
```

> **修改后重启 Claude Desktop 才能生效**

#### VS Code (Claude Dev / Cline) 配置

编辑 `.vscode/settings.json` 或 VS Code 设置：

**Windows 示例：**

```json
{
  "cline.mcpServers": [
    {
      "name": "zentao",
      "command": "your\\path\\mcp\\.venv\\Scripts\\python.exe",
      "args": ["your\\path\\mcp\\run_zentao_mcp.py"],
      "env": {
        "ZENTAO_BASE_URL": "http://172.16.0.193:8088",
        "ZENTAO_USERNAME": "your_username",
        "ZENTAO_PASSWORD": "your_password"
      }
    }
  ]
}
```

**macOS/Linux 示例：**

```json
{
  "cline.mcpServers": [
    {
      "name": "zentao",
      "command": "/Users/yourname/projects/mcp/.venv/bin/python",
      "args": ["/Users/yourname/projects/mcp/run_zentao_mcp.py"],
      "env": {
        "ZENTAO_BASE_URL": "http://172.16.0.193:8088",
        "ZENTAO_USERNAME": "your_username",
        "ZENTAO_PASSWORD": "your_password"
      }
    }
  ]
}
```

#### 通用 MCP 客户端配置（Python SDK）

如果使用 Python MCP SDK 或其他支持 MCP 的工具：

```python
import subprocess
import os

client = MCPClient(
    name="zentao",
    command=".venv/Scripts/python.exe",  # 或 .venv/bin/python
    args=["run_zentao_mcp.py"],
    env={
        "ZENTAO_BASE_URL": "http://172.16.0.193:8088",
        "ZENTAO_USERNAME": "your_username",
        "ZENTAO_PASSWORD": "your_password"
    },
    cwd="/path/to/mcp"  # 项目目录
)
```

#### 快速诊断配置问题

如果 MCP 连接失败，按以下步骤诊断：

**1. 验证 Python 路径是否正确**

```bash
# 直接运行 Python 看是否可用
C:\development\Projects\mcp\.venv\Scripts\python.exe --version

# 或
/Users/yourname/projects/mcp/.venv/bin/python --version
```

**2. 验证脚本路径是否正确**

```bash
# 检查 run_zentao_mcp.py 是否存在
ls -la C:\development\Projects\mcp\run_zentao_mcp.py  # Windows
ls -la /Users/yourname/projects/mcp/run_zentao_mcp.py  # macOS
```

**3. 直接运行测试连接**

```bash
# Windows
C:\development\Projects\mcp\.venv\Scripts\python.exe C:\development\Projects\mcp\run_zentao_mcp.py

# macOS/Linux
/Users/yourname/projects/mcp/.venv/bin/python /Users/yourname/projects/mcp/run_zentao_mcp.py
```

**4. 检查环境变量是否加载**

```bash
# 运行时看是否有配置错误提示
uv run python run_zentao_mcp.py
```

---

## 可用工具

### 工具覆盖现状

**当前版本**仅实现开发者相关的工具，共 **38 个工具**（覆盖 46% 的 API），未来版本会补充项目经理和测试人员的工具。

#### ✅ 完全实现的模块（开发者优先）

| 模块 | 工具数 | 用途 |
|------|--------|------|
| **项目集** (Program) | 5 | 项目框架管理 |
| **产品** (Product) | 5 | 产品信息查询 |
| **项目** (Project) | 8 | 项目管理 |
| **执行/迭代** (Execution) | 6 | 迭代规划 |
| **需求** (Story) | 5 | 需求追踪 |
| **任务** (Task) | 3 | 开发任务分配 |
| **Bug** | 3 | Bug 跟踪修复 |
| **用户** (User) | 3 | 团队成员信息 |

#### 🔮 规划中的功能（非开发者）

以下功能在后续版本中实现：
- **测试用例** (TestCase) - 测试人员使用
- **测试任务** (TestTask) - 测试人员使用
- **用户反馈** (Feedback) - 产品经理使用
- **工单管理** (Ticket) - 支持工单
- **版本/构建** (Build/Release) - 发布管理

---

### 项目集 (Programs)

#### list_programs
获取所有项目集列表。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| order | string | 否 | 排序方式，如 `order_asc` 或 `order_desc` |

**示例：**
```json
{
  "order": "order_asc"
}
```

---

#### get_program
获取指定项目集的详细信息。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| program_id | integer | 是 | 项目集 ID |

**示例：**
```json
{
  "program_id": 1
}
```

---

### 产品 (Products)

#### list_products
获取所有产品列表。

**参数：** 无

---

#### get_product
获取指定产品的详细信息。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| product_id | integer | 是 | 产品 ID |

---

#### create_product
创建新产品。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 产品名称 |
| code | string | 是 | 产品代号 |
| program | integer | 否 | 所属项目集 ID |
| PO | string | 否 | 产品负责人账号 |
| desc | string | 否 | 产品描述 |

**示例：**
```json
{
  "name": "企业管理系统",
  "code": "EMS",
  "program": 1,
  "PO": "productManager",
  "desc": "用于企业内部管理的综合系统"
}
```

---

### 项目 (Projects)

#### list_projects
获取所有项目列表。

**参数：**
| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| page | integer | 否 | 1 | 页码 |
| limit | integer | 否 | 20 | 每页数量 |

---

#### get_project
获取指定项目的详细信息。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| project_id | integer | 是 | 项目 ID |

---

#### create_project
创建新项目。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 项目名称 |
| code | string | 是 | 项目代号 |
| begin | string | 是 | 开始日期 (YYYY-MM-DD) |
| end | string | 是 | 结束日期 (YYYY-MM-DD) |
| products | array | 是 | 关联产品 ID 列表，如 `[1, 2]` |

**示例：**
```json
{
  "name": "2024年官网改版",
  "code": "WEB2024",
  "begin": "2024-01-01",
  "end": "2024-06-30",
  "products": [1]
}
```

---

#### get_project_executions
获取指定项目下的所有执行（迭代）。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| project_id | integer | 是 | 项目 ID |

---

### 执行/迭代 (Executions)

#### list_executions
获取所有执行列表。

**参数：** 无

---

#### get_execution
获取指定执行的详细信息。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| execution_id | integer | 是 | 执行 ID |

---

#### get_execution_tasks
获取指定执行下的所有任务。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| execution_id | integer | 是 | 执行 ID |

---

### 需求 (Stories)

#### get_story
获取指定需求的详细信息。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| story_id | integer | 是 | 需求 ID |

---

#### create_story
创建新需求。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| title | string | 是 | 需求标题 |
| product | integer | 是 | 产品 ID |
| pri | integer | 是 | 优先级 (1-4) |
| category | string | 是 | 类型：feature/interface/performance/safe/experience/improve/other |
| spec | string | 否 | 需求描述 |
| verify | string | 否 | 验收标准 |

**示例：**
```json
{
  "title": "用户登录功能优化",
  "product": 1,
  "pri": 1,
  "category": "feature",
  "spec": "支持手机号、邮箱、企业微信三种登录方式",
  "verify": "1. 手机号验证码登录正常\n2. 邮箱密码登录正常\n3. 企业微信扫码登录正常"
}
```

---

### 任务 (Tasks)

#### get_task
获取指定任务的详细信息。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| task_id | integer | 是 | 任务 ID |

---

#### create_task
创建新任务。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| execution_id | integer | 是 | 执行/迭代 ID |
| name | string | 是 | 任务名称 |
| type | string | 是 | 类型：design/devel/request/test/study/discuss/ui/affair/misc |
| assignedTo | array | 是 | 指派给的用户账号列表，如 `["dev1", "dev2"]` |
| estStarted | string | 是 | 预计开始日期 (YYYY-MM-DD) |
| deadline | string | 是 | 截止日期 (YYYY-MM-DD) |
| pri | integer | 否 | 优先级 (1-4) |
| estimate | number | 否 | 预计工时 |

**示例：**
```json
{
  "execution_id": 10,
  "name": "实现用户登录接口",
  "type": "devel",
  "assignedTo": ["zhangsan"],
  "estStarted": "2024-01-15",
  "deadline": "2024-01-20",
  "pri": 1,
  "estimate": 16
}
```

---

### Bug

#### get_bug
获取指定 Bug 的详细信息。

**参数：**
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| bug_id | integer | 是 | Bug ID |

---

### 用户 (Users)

#### list_users
获取所有用户列表。

**参数：** 无

---

#### get_my_info
获取当前登录用户的信息。

**参数：** 无

---

## 使用示例

### 开发者工作流场景

#### 场景1：查看当前迭代的任务

**背景**: 早上到公司，想查看今天要做哪些任务。

```
用户: "查看迭代10的所有任务"

AI执行:
1. get_execution(execution_id=10)  # 获取迭代信息
2. get_execution_tasks(execution_id=10)  # 获取所有任务
```

**返回示例**:
```json
{
  "tasks": [
    {
      "id": 101,
      "name": "实现用户登录接口",
      "type": "devel",
      "status": "doing",
      "assignedTo": "zhangsan",
      "deadline": "2024-01-20"
    },
    {
      "id": 102,
      "name": "修复登录页面样式",
      "type": "devel",
      "status": "wait",
      "assignedTo": "zhangsan",
      "deadline": "2024-01-22"
    }
  ]
}
```

---

#### 场景2：查看需要修复的 Bug

**背景**: 周会上分配了新的 Bug，想查看详情。

```
用户: "获取 Bug 123 的详细信息"

AI执行:
get_bug(bug_id=123)
```

**返回示例**:
```json
{
  "id": 123,
  "title": "登录页面在移动端显示错乱",
  "product": 1,
  "type": "bug",
  "status": "active",
  "severity": "serious",
  "assignedTo": "zhangsan",
  "desc": "在 iPhone 6S 上测试，登录表单显示超出屏幕范围...",
  "createdBy": "tester1",
  "createdDate": "2024-01-15"
}
```

---

#### 场景3：创建开发任务并分配

**背景**: 完成了代码审查，需要为团队成员创建开发任务。

```
用户: "在迭代10中创建一个任务：
- 名称：实现商品搜索功能
- 指派给：李四和王五
- 预计3天完成
- 优先级：高"

AI执行:
create_task(
  execution_id=10,
  name="实现商品搜索功能",
  type="devel",
  assignedTo=["lisi", "wangwu"],
  estStarted="2024-01-18",
  deadline="2024-01-21",
  pri=1,
  estimate=24
)
```

---

#### 场景4：创建需求并跟踪

**背景**: 产品经理提出新需求，开发团队需要记录并跟踪。

```
用户: "创建一个新的需求：
- 产品：移动App
- 标题：支持指纹登录
- 优先级：中等
- 描述：在 Android 和 iOS 上实现生物识别登录
- 验收标准：支持指纹和人脸识别"

AI执行:
create_story(
  title="支持指纹登录",
  product=2,
  pri=2,
  category="feature",
  spec="在 Android 和 iOS 上实现生物识别登录",
  verify="1. 指纹识别登录成功\n2. 人脸识别登录成功\n3. 降级到密码登录"
)
```

**后续跟踪**:
```
用户: "需求15当前的状态是什么？"

AI执行:
get_story(story_id=15)
```

---

#### 场景5：项目进度总结

**背景**: 每周五做周会汇报，需要查看项目总体进度。

```
用户: "查看项目7的基本信息和所有迭代"

AI执行:
1. get_project(project_id=7)  # 获取项目基本信息
2. get_project_executions(project_id=7)  # 获取所有迭代
```

**返回示例**:
```json
{
  "project": {
    "id": 7,
    "name": "企业管理系统",
    "code": "EMS",
    "status": "doing",
    "progress": 45,
    "begin": "2024-01-01",
    "end": "2024-06-30"
  },
  "executions": [
    {
      "id": 10,
      "name": "迭代1",
      "status": "doing",
      "begin": "2024-01-15",
      "end": "2024-01-29",
      "progress": 60
    },
    {
      "id": 11,
      "name": "迭代2",
      "status": "wait",
      "begin": "2024-01-30",
      "end": "2024-02-13"
    }
  ]
}
```

---

### 场景1：查看所有产品

**用户提问：**
> 列出禅道中所有的产品

**AI 执行：**
```json
{
  "name": "list_products",
  "arguments": {}
}
```

**返回示例：**
```json
{
  "total": 3,
  "products": [
    {
      "id": 1,
      "name": "企业官网",
      "code": "website",
      "PO": {"realname": "张三"},
      "status": "normal"
    },
    {
      "id": 2,
      "name": "内部管理系统",
      "code": "ims",
      "PO": {"realname": "李四"},
      "status": "normal"
    }
  ]
}
```

---

### 场景2：创建新项目

**用户提问：**
> 创建一个新产品叫"移动APP"，代号"app"

**AI 执行：**
```json
{
  "name": "create_product",
  "arguments": {
    "name": "移动APP",
    "code": "app"
  }
}
```

---

### 场景3：查看项目进度

**用户提问：**
> 查看项目ID为7的执行进度

**AI 执行：**
```json
{
  "name": "get_project",
  "arguments": {
    "project_id": 7
  }
}
```

**然后：**
```json
{
  "name": "get_project_executions",
  "arguments": {
    "project_id": 7
  }
}
```

---

### 场景4：创建开发任务

**用户提问：**
> 在迭代10中创建一个开发任务，叫"实现登录功能"，指派给张三，预计3天完成

**AI 执行：**
```json
{
  "name": "create_task",
  "arguments": {
    "execution_id": 10,
    "name": "实现登录功能",
    "type": "devel",
    "assignedTo": ["zhangsan"],
    "estStarted": "2024-01-15",
    "deadline": "2024-01-18",
    "estimate": 24
  }
}
```

---

### 场景5：查看当前用户信息

**用户提问：**
> 我是谁？在禅道中的权限是什么？

**AI 执行：**
```json
{
  "name": "get_my_info",
  "arguments": {}
}
```

---

## 故障排除

### 问题1：连接失败

**症状：**
```
Connection failed: Client failed to connect
```

**解决方案：**
1. 检查环境变量是否正确设置
2. 验证禅道服务器地址是否可访问
3. 确认用户名和密码正确
4. 检查网络连接

**验证命令：**
```bash
# 测试网络连接
curl http://172.16.0.193:8088/api.php/v1/tokens \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"account":"your_username","password":"your_password"}'
```

---

### 问题2：环境变量未加载

**症状：**
```
Zentao configuration is incomplete
```

**解决方案：**

确保 `python-dotenv` 已安装：
```bash
uv add python-dotenv
```

确认 `.env` 文件格式正确：
```env
ZENTAO_BASE_URL=http://172.16.0.193:8088
ZENTAO_USERNAME=jiangyong
ZENTAO_PASSWORD=your_password
```

---

### 问题3：编码错误

**症状：**
```
UnicodeEncodeError: 'gbk' codec can't encode character
```

**解决方案：**

在 Windows PowerShell 中设置 UTF-8 编码：
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

或在运行命令前设置：
```powershell
$env:PYTHONIOENCODING="utf-8"
```

---

### 问题4：权限不足

**症状：**
```
HTTP 403 Forbidden
```

**解决方案：**
1. 确认用户有 API 访问权限
2. 检查禅道后台的 API 设置
3. 确认用户所属角色有相应权限

---

### 问题5：模块未找到

**症状：**
```
No module named 'zentao_mcp'
```

**解决方案：**

使用启动脚本 `run_zentao_mcp.py`，它会自动设置 `PYTHONPATH`。

或者手动设置：
```bash
set PYTHONPATH=C:\development\Projects\mcp\src
python -m zentao_mcp
```

---

## 附录

### B. 常用命令速查

#### UV 相关命令

```bash
# 同步依赖（首次安装或更新 pyproject.toml 后运行）
uv sync

# 运行 MCP 服务
uv run python run_zentao_mcp.py

# 运行测试脚本
uv run python examples/test_zentao_client.py

# 添加新的依赖包
uv add requests

# 查看已安装的包
uv pip list

# 删除虚拟环境
uv venv --python 3.11 --upgrade

# 更新 UV 本身
uv self update
```

#### MCP 相关命令

```bash
# Kimi Code CLI
kimi mcp list                 # 列出所有 MCP 服务
kimi mcp test zentao          # 测试 zentao MCP 连接
kimi mcp logs zentao          # 查看 zentao MCP 日志
kimi mcp remove zentao        # 移除 zentao MCP 配置

# 其他 CLI（需要支持 MCP）
# 根据你使用的 AI 工具而定
```

#### 诊断和调试

```bash
# 直接运行 MCP 服务（调试模式）
python run_zentao_mcp.py

# 验证环境变量是否加载
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('ZENTAO_BASE_URL'))"

# 测试禅道服务器连接
curl http://172.16.0.193:8088/api.php/v1/tokens \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"account":"username","password":"password"}'

# 查看当前 Python 路径（用于配置 MCP）
python -c "import sys; print(sys.executable)"

# 查看虚拟环境中的 Python 路径
uv python find
```

### C. 为其他开发者配置使用指南

如果你想让团队其他成员使用这个 MCP 工具，按以下步骤操作：

#### 第1步：分享项目代码

确保团队成员有项目代码副本。可以通过以下方式：

```bash
# 方式1: 从 Git 克隆
git clone <your-repo-url>
cd mcp

# 方式2: 下载压缩包
# 解压到本地目录
cd C:\development\Projects\mcp
```

#### 第2步：让他们安装 UV 并同步依赖

发送以下命令给团队成员：

**Windows PowerShell：**
```powershell
# 安装 UV
irm https://astral.sh/uv/install.ps1 | iex

# 同步依赖
cd C:\path\to\mcp
uv sync
```

**macOS/Linux：**
```bash
# 安装 UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 同步依赖
cd /path/to/mcp
uv sync
```

#### 第3步：配置环境变量

让他们创建 `.env` 文件：

```bash
# 进入项目目录
cd C:\development\Projects\mcp  # Windows
cd /path/to/mcp                 # macOS/Linux

# 创建 .env 文件（已提供 .env.example 作为模板）
cp .env.example .env              # macOS/Linux
copy .env.example .env            # Windows cmd
```

编辑 `.env` 文件：

```env
ZENTAO_BASE_URL=http://172.16.0.193:8088
ZENTAO_USERNAME=their_username
ZENTAO_PASSWORD=their_password
```

#### 第4步：确定 Python 路径

让他们运行以下命令找出 Python 路径（不同电脑路径会不同）：

```bash
# 推荐方式：使用 UV 查找
uv python find

# 或者手动查找
python -c "import sys; print(sys.executable)"
```

**输出示例：**
```
C:\Users\john\Projects\mcp\.venv\Scripts\python.exe  # Windows
/Users/john/Projects/mcp/.venv/bin/python            # macOS
```

#### 第5步：配置 MCP 客户端

根据实际的 Python 路径修改 MCP 配置。以下是配置模板：

**Claude Desktop (Windows 示例)**:

假设 Python 路径为 `C:\Users\john\Projects\mcp\.venv\Scripts\python.exe`

配置文件：`%APPDATA%\Claude\settings.json`

```json
{
  "mcpServers": {
    "zentao": {
      "command": "C:\\Users\\john\\Projects\\mcp\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\john\\Projects\\mcp\\run_zentao_mcp.py"],
      "env": {
        "ZENTAO_BASE_URL": "http://172.16.0.193:8088",
        "ZENTAO_USERNAME": "their_username",
        "ZENTAO_PASSWORD": "their_password"
      }
    }
  }
}
```

**Kimi Code CLI (macOS 示例)**:

假设 Python 路径为 `/Users/john/Projects/mcp/.venv/bin/python`

配置文件：`~/.kimi/mcp.json`

```json
{
  "mcpServers": {
    "zentao": {
      "command": "/Users/john/Projects/mcp/.venv/bin/python",
      "args": ["/Users/john/Projects/mcp/run_zentao_mcp.py"],
      "env": {
        "ZENTAO_BASE_URL": "http://172.16.0.193:8088",
        "ZENTAO_USERNAME": "their_username",
        "ZENTAO_PASSWORD": "their_password"
      }
    }
  }
}
```

**VS Code / Cline：**

在项目的 `.vscode/settings.json` 中添加：

```json
{
  "cline.mcpServers": [
    {
      "name": "zentao",
      "command": "/Users/john/Projects/mcp/.venv/bin/python",
      "args": ["/Users/john/Projects/mcp/run_zentao_mcp.py"],
      "env": {
        "ZENTAO_BASE_URL": "http://172.16.0.193:8088",
        "ZENTAO_USERNAME": "their_username",
        "ZENTAO_PASSWORD": "their_password"
      }
    }
  ]
}
```

#### 第6步：验证配置

运行以下命令测试：

```bash
# 直接运行看是否正常启动
uv run python run_zentao_mcp.py

# 按 Ctrl+C 停止

# 然后在 AI 工具中测试连接
# 例如在 Claude Desktop 或 Kimi Code 中列出工具
```

#### 常见问题

**Q: 每个人的 Python 路径都不一样，怎么办？**

A: 是的，不同电脑上 Python 路径不同。但 `.env` 文件中的环境变量是相同的，只需要修改 MCP 配置中的 `command` 和 `args` 路径即可。

**Q: 能不能统一 Python 路径？**

A: 可以考虑以下方案：
1. 使用相对路径（但需要从项目目录运行）
2. 在 PATH 环境变量中添加 Python，这样可以直接用 `python` 代替完整路径
3. 创建一个启动脚本自动找到 Python 路径

**Q: 安全性怎么保证？**

A:
- `.env` 文件包含敏感信息，不要提交到 Git（应已在 `.gitignore`）
- MCP 配置中的密码也是敏感的，建议使用环境变量或 secrets 管理
- 企业环境可以考虑使用统一的 LDAP/SSO 认证

---

### C. 类型对照表

| 禅道字段 | 类型 | 说明 |
|----------|------|------|
| story.category | string | feature/interface/performance/safe/experience/improve/other |
| story.stage | string | wait/planned/projected/developing/developed/testing/tested/verified/released/closed |
| story.status | string | draft/active/closed/changed |
| task.type | string | design/devel/request/test/study/discuss/ui/affair/misc |
| task.status | string | wait/doing/done/closed/cancel |
| bug.status | string | active/resolved/closed |
| project.model | string | scrum/waterfall |
| project.status | string | wait/doing/suspend/closed |

### D. 联系方式

如有问题或建议，请通过以下方式联系：
- 项目地址：https://github.com/your-repo/zentao-mcp
- 问题反馈：https://github.com/your-repo/zentao-mcp/issues

---

**文档版本：** 1.1
**最后更新：** 2026-01-30
**兼容禅道版本：** 15.x+
**兼容操作系统：** Windows, macOS, Linux
