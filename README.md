# 🛰️ Antigravity Node Benchmark (V7.0 Pragmatic)

> **Zero-Risk, Multi-Platform Pragmatic Node Stability & Egress Diagnostic Benchmark for Google AI & Antigravity IDE**  
> *专为 Google AI 与 Antigravity 打造的高可用代理节点稳定性与真实可用度基准测试天梯榜 (实用版)*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0%20External%20Libs-blue.svg)]()
[![Privacy](https://img.shields.io/badge/Security-100%25%20Anonymous%20%26%20Zero--Risk-success.svg)]()

---

## 🌟 核心亮点 (Key Highlights)

- 🔒 **100% 匿名无感探测 (Zero Account / Zero Auth Required)**  
  不涉及任何 Google API Key、OAuth Token 或账号凭证。纯网络层探针，**0 账号封禁风险**。
- ⚡ **零第三方依赖 (Zero External Dependencies)**  
  纯 Python 标准库开发，开箱即用，无需 `pip install` 任何额外依赖。
- 🎯 **直连 Antigravity 真实生产网关 (Production Gateway Probes)**  
  直击 `generativelanguage.googleapis.com` 模型网关与 `accounts.google.com` OAuth 认证链路，彻底杜绝消费级 Web 前端反爬虫带来的误杀。
- 🛡️ **实用主义分级体系 (Pragmatic Grading & 0 False Positives)**  
  - 🌟 **S 级 (黄金首选)**：`0 丢包` + `均延 < 280ms`（极速流畅输出，强力推荐主力）
  - 🟢 **A 级 (优质主力)**：`0 丢包` + `均延 < 480ms`（稳定全通，全天候开发主力）
  - 🟡 **B 级 (普通备选)**：`微丢包 (<=20%)` 或长距离跨大洲可用节点（日常应急）
  - 🟠 **C 级 (易断流)**：`丢包率 > 20%`（会话易断流，建议避开）
  - ⛔ **F 级 (受限/失效)**：香港/大陆等封锁地区、OAuth 阻断或落地脱机（一票否决）
- 🌐 **全代理客户端兼容 (Universal Multi-Platform Support)**  
  - **模式 A (Controller API 模式)**：原生支持 **Flclash、Clash Verge Rev、Clash Nyanpasu、Clash for Windows、Mihomo Core、ShellCrash**。
  - **模式 B (Direct Proxy 模式)**：原生支持 **v2rayN、Sing-box、Surge、Loon、Shadowsocks** 等任意本地 HTTP/SOCKS5 代理端口。
- 📦 **自动生成可用资产**：
  - 终端彩色实时天梯榜 (Real-time Console View)
  - 深度 Markdown 评估报告 (`ANTIGRAVITY_NODE_REPORT.md`)
  - Clash / Mihomo 专属高可用策略组 YAML (`antigravity_policy_group.yaml`)
  - Sing-box Outbounds 路由配置 JSON (`singbox_outbounds.json`)

---

## 🚀 快速上手 (Quick Start)

### 环境要求
- Python 3.8 或更高版本（Windows / macOS / Linux 全平台支持）

### 运行方式

#### 1. Clash / Mihomo / Flclash / Clash Verge 客户端（推荐）
保持代理客户端运行，直接在终端执行：

```bash
# 自动探测活跃的控制端口 (9090 / 9097 / 2049) 并开始实测
python main.py
```

#### 2. v2rayN / Sing-box / Surge / 任意本地代理端口
如果你使用 v2rayN、Sing-box 或 Surge，指定本地代理端口即可运行单端口全息诊断：

```bash
# 测试本地 HTTP 代理端口
python main.py --proxy http://127.0.0.1:7890

# 测试本地 SOCKS5 代理端口
python main.py --proxy socks5://127.0.0.1:10808
```

---

## 📊 诊断链路与分级逻辑 (Diagnostic Flow)

```mermaid
graph TD
    A[候选节点/代理链路] --> B{CF 基准 + Google Core 通畅?}
    B -- 否 --> F1[🚨 判定: 彻底离线 / 国内中转直出脱机]
    B -- 是 --> C{generativelanguage API 通畅?}
    C -- 否 --> F2[⛔ 判定: 香港/受限地区地理围栏拦截]
    C -- 是 --> D{accounts.google.com 认证通畅?}
    D -- 否 --> F3[🔑 判定: OAuth 认证端点阻断, 无法登录/刷新Token]
    D -- 是 --> E{0 丢包 + 均延 < 280ms?}
    E -- 是 --> S[🌟 S 级·黄金首选 (极速流畅)]
    E -- 否 --> G{0 丢包 + 均延 < 480ms?}
    G -- 是 --> A_TIER[🟢 A 级·优质主力 (稳定可靠)]
    G -- 否 --> H{丢包率 <= 20%?}
    H -- 是 --> B_TIER[🟡 B 级·普通备用]
    H -- 否 --> C_TIER[🟠 C 级·易断流]
```

---

## ⚙️ CLI 命令行参数 (Command-line Options)

```text
用法: main.py [-h] [--api API] [--secret SECRET] [--proxy PROXY]
               [--concurrency CONCURRENCY] [--timeout TIMEOUT]
               [--filter FILTER] [--report REPORT] [--yaml YAML]
               [--sing-box SING_BOX]

选项:
  --api API             Clash/Mihomo 控制端口 URL (默认自动探测 9090/9097/2049)
  --secret SECRET       控制端口 Secret 鉴权密钥 (未设置可留空)
  --proxy PROXY         指定单代理端口直接测试 (如 http://127.0.0.1:7890)
  --concurrency, -c     并发探测线程数 (默认: 16)
  --timeout, -t         单节点超时时间 ms (默认: 3500)
  --filter, -f          按关键词过滤节点名称 (如 'Japan', 'Singapore', 'US')
  --report, -r          Markdown 报告保存路径 (默认: ANTIGRAVITY_NODE_REPORT.md)
  --yaml, -y            Clash 高可用策略组导出路径 (默认: antigravity_policy_group.yaml)
  --sing-box, -s        Sing-box 出站配置导出路径 (如: singbox_outbounds.json)
```

---

## 🛡️ Clash / Flclash 高可用策略组配置示例

运行完成后，脚本会自动生成 `antigravity_policy_group.yaml`。将其加入配置即可享受**智能自动优选 + 秒级故障无感容灾**：

```yaml
proxy-groups:
  # 1. 智能自动优选组 (每次对话自动选择延迟最低的 S/A 级节点)
  - name: 🚀 Antigravity-Auto
    type: url-test
    url: https://generativelanguage.googleapis.com/v1beta/models
    interval: 180
    tolerance: 40
    proxies:
      - "🇸🇬 Singapore-01"
      - "🇺🇸 UnitedStates-01"
      - "🇯🇵 Japan-01"

  # 2. 故障无感容灾组 (主节点异常时按顺序无缝切换到备选节点)
  - name: 🛡️ Antigravity-Fallback
    type: fallback
    url: https://generativelanguage.googleapis.com/v1beta/models
    interval: 120
    proxies:
      - "🇸🇬 Singapore-01"
      - "🇺🇸 UnitedStates-01"
      - "🇯🇵 Japan-01"

rules:
  - DOMAIN-SUFFIX,generativelanguage.googleapis.com,🚀 Antigravity-Auto
  - DOMAIN-SUFFIX,cloudaicompanion.googleapis.com,🚀 Antigravity-Auto
  - DOMAIN-SUFFIX,cloudcode-pa.googleapis.com,🚀 Antigravity-Auto
  - DOMAIN-SUFFIX,alkalimakersuite-pa.clients6.google.com,🚀 Antigravity-Auto
  - DOMAIN-KEYWORD,generativeai,🚀 Antigravity-Auto
```

---

## 📄 License & Disclaimer

- **License**: 本项目基于 [MIT License](LICENSE) 开源。
- **Disclaimer**: 本工具仅用于网络可达性与服务连通性诊断，不收集任何用户隐私或账号数据，探测过程 100% 匿名无感。
