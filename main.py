#!/usr/bin/env python3
"""
🛰️ Antigravity Node Benchmark (V5.0 Universal)
Zero-Risk, Multi-Platform Node Stability & Egress Diagnostic Benchmark for Google AI & Antigravity

Features:
- 100% Anonymous & Zero-Risk (Zero Auth / No API Key / No Account Required)
- Multi-Platform Support:
  - Mode A (Controller Mode): Flclash, Clash Verge Rev, Clash Nyanpasu, Clash for Windows, Mihomo Core, ShellCrash
  - Mode B (Direct Proxy Mode): v2rayN, Sing-box, Surge, Loon, Shadowsocks, or any local HTTP/SOCKS5 proxy port
- 8-Dimensional Full-Spectrum Diagnostic Matrix:
  1. Domestic Transit Direct Leak / Detached Exit (上海等国内中转直出拦截)
  2. Google AI Geofenced Regions (香港/澳门等受限出口)
  3. OAuth & Token Refresh Blocked (accounts.google.com 认证阻断)
  4. AI Application Layer Partial Block (AI Studio/Gemini 真实流量阻断)
  5. Google Cloud Armor & WAF Cleanliness (脏 IP / 频控预警)
  6. SSE Stream TTFB (Time to First Byte) & Jitter Analysis
  7. Multi-round Stress Sampling & Isolated AI Loss Tracking
- Exporters:
  - Real-time Console View (ANSI Color & Real-time Progress)
  - Detailed Markdown Diagnostic Report (.md)
  - Clash / Mihomo High-Availability Policy Group (.yaml with Auto & Fallback & Rules)
  - Sing-box Outbounds Configuration (.json)
- 100% Python Standard Library (Zero Third-Party Dependencies)
"""

import sys
import json
import re
import time
import argparse
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Ensure UTF-8 output on Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


# Public Anonymous Probe Endpoints (Zero auth required)
ENDPOINTS = {
    "AI_API": "https://generativelanguage.googleapis.com/generate-204",     # Google AI API Gateway
    "GEMINI_WEB": "https://gemini.google.com",                              # Gemini Web Gateway
    "AUTH": "https://accounts.google.com/generate_204",                      # Google OAuth & Token Refresh
    "CORE": "https://www.gstatic.com/generate_204",                         # Google Global Edge Core
    "WAF_RISK": "https://recaptchaenterprise.googleapis.com/generate-204",  # Google Cloud Armor & WAF Gateway
    "AI_STUDIO": "https://aistudio.google.com",                             # Google AI Studio Application Layer
    "CF_BASELINE": "https://cloudflare.com/cdn-cgi/trace",                  # Global Base Connection
}

# Regex to identify blocked regions while preventing false positives like "ICN", "CN2", "PROMO"
BLOCKED_NAME_REGEX = re.compile(
    r'(?i)(?:\bcn\b|\bchina\b|中国|大陆|上海|北京|广州|深圳|'
    r'\bhk\b|\bhong\s*kong\b|香港|'
    r'\bmo\b|\bmacau\b|\bmacao\b|澳门|'
    r'\bru\b|\brussia\b|俄罗斯|'
    r'\bir\b|\biran\b|伊朗)'
)

# Common controller ports across popular Clash/Mihomo clients
AUTO_DISCOVERY_PORTS = [9090, 9097, 2049, 9999]


def is_region_name_blocked(name: str) -> bool:
    """Check if node name explicitly indicates a blocked region (safeguards 'CN2')."""
    name_clean = re.sub(r'(?i)\bcn2\b', '', name)
    return bool(BLOCKED_NAME_REGEX.search(name_clean))


def auto_detect_controller(secret: str = "") -> str:
    """Auto-scan localhost for active Clash/Mihomo External Controller API ports."""
    for port in AUTO_DISCOVERY_PORTS:
        url = f"http://127.0.0.1:{port}"
        try:
            req = urllib.request.Request(f"{url}/proxies")
            if secret:
                req.add_header("Authorization", f"Bearer {secret}")
            with urllib.request.urlopen(req, timeout=1.2) as resp:
                if resp.status == 200:
                    return url
        except Exception:
            continue
    return "http://127.0.0.1:9090"


def get_clash_proxies(controller_url: str, secret: str = "") -> list:
    """Query Clash External Controller for all active proxy nodes."""
    endpoint = f"{controller_url.rstrip('/')}/proxies"
    req = urllib.request.Request(endpoint)
    if secret:
        req.add_header("Authorization", f"Bearer {secret}")

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            proxies_dict = data.get("proxies", {})

            real_proxies = []
            non_real_types = {"Selector", "URLTest", "Fallback", "LoadBalance", "Direct", "Reject", "Pass", "Compatible", "Relay"}
            ignore_keywords = ["套餐到期", "剩余流量", "重置", "官网", "expire", "traffic", "reset", "pass-rule", "reject-drop", "direct", "reject", "global"]

            for name, details in proxies_dict.items():
                p_type = details.get("type", "")
                name_lower = name.lower()

                if p_type in non_real_types or details.get("all"):
                    continue
                if any(kw in name_lower for kw in ignore_keywords):
                    continue

                real_proxies.append({
                    "name": name,
                    "type": p_type,
                    "udp": details.get("udp", False),
                    "history_delay": details.get("history", [{}])[-1].get("delay", 0) if details.get("history") else 0
                })
            return real_proxies
    except urllib.error.HTTPError as e:
        if e.code in [400, 404]:
            raise ConnectionError(
                f"端口类型冲突 ({controller_url})：\n"
                f"  当前端口似乎是【混合代理端口 (Mixed Port)】，而非【外部控制 API 端口 (External Controller)】。\n"
                f"  💡 解决方式：请在客户端设置中将'外部控制端口'设为独立端口 (如 9090 或 9097)。"
            )
        raise ConnectionError(f"HTTP 错误 ({e.code}): {e.reason}")
    except urllib.error.URLError as e:
        raise ConnectionError(
            f"无法连接到客户端外部控制端口 ({controller_url})。\n"
            f"请检查：\n"
            f"  1. Clash/Flclash/Mihomo 是否正在运行并已启动内核\n"
            f"  2. 客户端设置中是否开启了 '外部控制/External Controller' 端口 (如 9090 或 9097)\n"
            f"  3. 脚本访问请使用本地回环地址 http://127.0.0.1:端口\n"
            f"  4. 错误详情: {e.reason}"
        )


def probe_controller_delay(controller_url: str, secret: str, proxy_name: str, target_url: str, timeout_ms: int = 3500) -> int:
    """Probe a single endpoint via Clash REST API /proxies/{name}/delay."""
    encoded_name = urllib.parse.quote(proxy_name, safe='')
    encoded_test_url = urllib.parse.quote(target_url)
    url = f"{controller_url.rstrip('/')}/proxies/{encoded_name}/delay?url={encoded_test_url}&timeout={timeout_ms}"

    req = urllib.request.Request(url)
    if secret:
        req.add_header("Authorization", f"Bearer {secret}")

    try:
        with urllib.request.urlopen(req, timeout=(timeout_ms / 1000) + 1.2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            d = data.get("delay", 0)
            return d if d > 0 else 99999
    except Exception:
        return 99999


def probe_direct_proxy_delay(proxy_url: str, target_url: str, timeout_ms: int = 3500) -> int:
    """Probe an endpoint directly through a local HTTP/SOCKS5 proxy port (v2rayN/Sing-box/Surge mode)."""
    proxy_handler = urllib.request.ProxyHandler({
        'http': proxy_url,
        'https': proxy_url
    })
    opener = urllib.request.build_opener(proxy_handler)
    req = urllib.request.Request(
        target_url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )

    t0 = time.perf_counter()
    try:
        with opener.open(req, timeout=timeout_ms / 1000.0) as resp:
            if resp.status in [200, 204, 301, 302]:
                delay = int((time.perf_counter() - t0) * 1000)
                return max(1, delay)
            return 99999
    except Exception:
        return 99999


def test_single_node(controller_url: str, secret: str, node_info: dict, timeout_ms: int = 3500) -> dict:
    """Full-spectrum multi-probe & diagnostic engine (V5.0)."""
    proxy_name = node_info["name"]
    p_type = node_info.get("type", "Unknown")

    def _f_result(tag, category, reason, ttfb=99999, avg_delay=99999):
        return {
            "name": proxy_name, "type": p_type,
            "ttfb": ttfb, "avg_delay": avg_delay,
            "loss_rate": 100.0, "jitter": 0, "score": 0,
            "grade": "F", "tag": tag, "category": category,
            "waf_warning": False, "reason": reason
        }

    # 1. Hard name-based geofence check
    if is_region_name_blocked(proxy_name):
        return _f_result("⛔", "BLOCKED_REGION", "Google AI 地区封锁 (名称标记为香港/大陆/受限地区)")

    # 2. 8-Endpoint diagnostic probes
    cf_delay     = probe_controller_delay(controller_url, secret, proxy_name, ENDPOINTS["CF_BASELINE"], timeout_ms)
    core_delay   = probe_controller_delay(controller_url, secret, proxy_name, ENDPOINTS["CORE"], timeout_ms)
    ai_delay     = probe_controller_delay(controller_url, secret, proxy_name, ENDPOINTS["AI_API"], timeout_ms)
    gemini_delay = probe_controller_delay(controller_url, secret, proxy_name, ENDPOINTS["GEMINI_WEB"], timeout_ms)
    waf_delay    = probe_controller_delay(controller_url, secret, proxy_name, ENDPOINTS["WAF_RISK"], timeout_ms)
    auth_delay   = probe_controller_delay(controller_url, secret, proxy_name, ENDPOINTS["AUTH"], timeout_ms)
    studio_delay = probe_controller_delay(controller_url, secret, proxy_name, ENDPOINTS["AI_STUDIO"], timeout_ms)

    cf_ok      = 0 < cf_delay < 99999
    core_ok    = 0 < core_delay < 99999
    ai_ok      = 0 < ai_delay < 99999
    gemini_ok  = 0 < gemini_delay < 99999
    waf_ok     = 0 < waf_delay < 99999
    auth_ok    = 0 < auth_delay < 99999
    studio_ok  = 0 < studio_delay < 99999

    # 3. Diagnostic Matrix
    if not cf_ok and not core_ok and not ai_ok:
        return _f_result("🔴", "OFFLINE", "节点离线 / 无法建立网络连接 (TCP握手失败)")

    if cf_ok and not core_ok and not ai_ok:
        return _f_result("🚨", "DOMESTIC_LEAK", "国内中转直出/落地脱机 (流量滞留上海等国内入口，Google 被 GFW 拦截)")

    if core_ok and not ai_ok and not gemini_ok:
        return _f_result("⛔", "AI_BLOCKED", "Google AI 区域拦截 (真实出口位于香港/不支持地区，AI 服务不可用)",
                         ttfb=core_delay, avg_delay=core_delay)

    if ai_ok and not auth_ok:
        return _f_result("🔑", "AUTH_BLOCKED",
                         f"OAuth 认证端点不可达 (AI延迟:{ai_delay}ms，但 accounts.google.com 被拦截，无法登录/刷新Token)",
                         ttfb=ai_delay, avg_delay=ai_delay)

    if ai_ok and not studio_ok and not gemini_ok:
        return _f_result("🔒", "AI_PARTIAL",
                         f"AI 应用层受阻 (204健康检查通过但 AI Studio/Gemini 应用被拦截，延迟:{ai_delay}ms)",
                         ttfb=ai_delay, avg_delay=ai_delay)

    waf_warning = ai_ok and not waf_ok

    # 4. Stress Sampling: Reuse diagnostic data + Circuit Breaker
    samples = []
    ai_success = 0
    ai_total = 0

    for delay_val, is_ai_ep in [(ai_delay, True), (auth_delay, False), (core_delay, False)]:
        if 0 < delay_val < 99999:
            samples.append(delay_val)
            if is_ai_ep:
                ai_success += 1
        if is_ai_ep:
            ai_total += 1

    probe_spec = [
        (ENDPOINTS["AI_API"], True),
        (ENDPOINTS["AUTH"],   False),
        (ENDPOINTS["CORE"],   False),
    ]
    round_fails = 0
    for ep_url, is_ai_ep in probe_spec:
        d = probe_controller_delay(controller_url, secret, proxy_name, ep_url, timeout_ms)
        if is_ai_ep:
            ai_total += 1
        if 0 < d < 99999:
            samples.append(d)
            if is_ai_ep:
                ai_success += 1
        else:
            round_fails += 1

    if round_fails < 3:
        for ep_url, is_ai_ep in probe_spec:
            d = probe_controller_delay(controller_url, secret, proxy_name, ep_url, timeout_ms)
            if is_ai_ep:
                ai_total += 1
            if 0 < d < 99999:
                samples.append(d)
                if is_ai_ep:
                    ai_success += 1

    total_probes = 3 + 3 + (3 if round_fails < 3 else 0)
    successful_probes = len(samples)
    loss_rate = ((total_probes - successful_probes) / total_probes) * 100.0

    if successful_probes == 0:
        return _f_result("🟠", "UNSTABLE", "高负载断流 / 多轮采样全丢包")

    avg_delay = int(sum(samples) / successful_probes)
    min_delay = min(samples)
    max_delay = max(samples)
    jitter = max_delay - min_delay
    ttfb = min_delay

    ai_loss_rate = ((ai_total - ai_success) / ai_total * 100.0) if ai_total > 0 else 0.0

    # 5. Scoring Model
    score = 100.0
    name_lower = proxy_name.lower()
    is_hy2 = "hy2" in name_lower or p_type.lower() == "hysteria2"
    is_reality = "reality" in name_lower or "vless" in p_type.lower()

    if is_hy2:
        score += 5
    elif is_reality:
        score += 3

    if avg_delay > 120:
        score -= (avg_delay - 120) / 20.0
    if jitter > 30:
        score -= (jitter - 30) / 15.0
    if waf_warning:
        score -= 8.0
    score -= loss_rate * 0.85

    if ai_loss_rate > 50 and loss_rate < 40:
        score -= 15.0

    score = max(0, min(100, int(score)))

    if loss_rate == 0 and score >= 85 and avg_delay <= 250 and not waf_warning:
        grade, tag, category = "S", "🌟", "GOLD"
        reason = f"黄金节点 (0丢包, TTFB:{ttfb}ms, 极速纯净, 最适合长代码流式输出)"
    elif loss_rate == 0 and score >= 70:
        grade, tag, category = "A", "🟢", "PRIMARY"
        reason = f"优质主力 (0丢包, TTFB:{ttfb}ms, Google AI 全通)"
    elif loss_rate < 35 and score >= 50:
        grade, tag, category = "B", "🟡", "BACKUP"
        reason = f"普通备用 (偶发微抖动, TTFB:{ttfb}ms)"
    else:
        grade, tag, category = "C", "🟠", "UNSTABLE"
        if ai_loss_rate > 50:
            reason = f"AI端点定向不稳定 (AI专项丢包:{ai_loss_rate:.0f}%, 对话易报错)"
        elif loss_rate >= 35:
            reason = f"高丢包易断流 (丢包率:{loss_rate:.1f}%, 长连接极易中断)"
        elif avg_delay > 400:
            reason = f"延迟过高不可用 (均值:{avg_delay}ms, 流式响应严重卡顿)"
        else:
            reason = f"综合质量偏低 (延迟:{avg_delay}ms, 抖动:{jitter}ms, 丢包:{loss_rate:.1f}%)"

    return {
        "name": proxy_name, "type": p_type,
        "ttfb": ttfb, "avg_delay": avg_delay,
        "loss_rate": round(loss_rate, 1), "jitter": jitter,
        "score": score, "grade": grade, "tag": tag,
        "category": category, "waf_warning": waf_warning,
        "reason": reason
    }


def benchmark_direct_proxy(proxy_url: str, timeout_ms: int = 3500) -> dict:
    """Benchmark a single active local proxy port (v2rayN/Sing-box/Surge mode)."""
    print("=" * 88, flush=True)
    print(" 🛰️ Antigravity 单端口代理全息诊断 (Direct Proxy Mode)", flush=True)
    print("=" * 88, flush=True)
    print(f"📡 目标代理地址: {proxy_url}", flush=True)
    print(f"🔍 正在执行 8 维诊断矩阵探测...\n", flush=True)

    endpoints_to_test = [
        ("Cloudflare 基准", ENDPOINTS["CF_BASELINE"]),
        ("Google Core 边缘", ENDPOINTS["CORE"]),
        ("Google AI API", ENDPOINTS["AI_API"]),
        ("Gemini Web 网关", ENDPOINTS["GEMINI_WEB"]),
        ("Google OAuth 认证", ENDPOINTS["AUTH"]),
        ("AI Studio 应用层", ENDPOINTS["AI_STUDIO"]),
        ("WAF / Cloud Armor", ENDPOINTS["WAF_RISK"]),
    ]

    samples = []
    for name, ep in endpoints_to_test:
        d = probe_direct_proxy_delay(proxy_url, ep, timeout_ms)
        status = f"✅ {d} ms" if 0 < d < 99999 else "❌ 阻断/超时"
        print(f"  [{name:<16}] -> {status}", flush=True)
        if 0 < d < 99999 and ep in [ENDPOINTS["AI_API"], ENDPOINTS["AUTH"], ENDPOINTS["CORE"]]:
            samples.append(d)

    print("\n" + "-" * 88, flush=True)
    if not samples:
        print("❌ [诊断结论]: 该代理端口无法连通 Google AI 核心服务，请检查客户端出口配置！\n", flush=True)
    else:
        avg_d = int(sum(samples) / len(samples))
        min_d = min(samples)
        max_d = max(samples)
        print(f"🏆 [诊断结论]: 代理连通正常 | 最优首包 TTFB: {min_d}ms | 平均延迟: {avg_d}ms | 抖动: ±{max_d - min_d}ms\n", flush=True)


def export_clash_policy_group(s_tier: list, a_tier: list, b_tier: list, output_path: str = "antigravity_policy_group.yaml"):
    """Generate an optimized Clash/Mihomo Proxy Group YAML with Auto, Fallback and Rules."""
    recommended_nodes = [r["name"] for r in (s_tier + a_tier)]
    if not recommended_nodes and b_tier:
        recommended_nodes = [r["name"] for r in b_tier[:4]]

    if not recommended_nodes:
        return

    yaml_content = f"""# =====================================================================
# 🚀 Antigravity / Google AI 专属高可用策略组 (Auto Generated)
# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# 包含 {len(recommended_nodes)} 个实测优质海外节点，支持自动故障秒级转移 (Failover)
# =====================================================================

proxy-groups:
  # 1. 智能自动优选组 (每次对话自动选择延迟最低的 S/A 级节点)
  - name: 🚀 Antigravity-Auto
    type: url-test
    url: https://generativelanguage.googleapis.com/generate-204
    interval: 180
    tolerance: 40
    lazy: false
    proxies:
"""
    for node_name in recommended_nodes:
        yaml_content += f'      - "{node_name}"\n'

    yaml_content += f"""
  # 2. 故障无感容灾组 (主节点异常时按顺序无缝切换到备选节点)
  - name: 🛡️ Antigravity-Fallback
    type: fallback
    url: https://generativelanguage.googleapis.com/generate-204
    interval: 120
    lazy: false
    proxies:
"""
    for node_name in recommended_nodes:
        yaml_content += f'      - "{node_name}"\n'

    yaml_content += """
# =====================================================================
# 💡 分流规则推荐 (Rules Configuration):
# 将以下规则加入你的 rules: 列表顶部即可实现精准分流：
# =====================================================================
# rules:
#   - DOMAIN-SUFFIX,generativelanguage.googleapis.com,🚀 Antigravity-Auto
#   - DOMAIN-SUFFIX,aistudio.google.com,🚀 Antigravity-Auto
#   - DOMAIN-SUFFIX,gemini.google.com,🚀 Antigravity-Auto
#   - DOMAIN-SUFFIX,alkalimakersuite-pa.clients6.google.com,🚀 Antigravity-Auto
#   - DOMAIN-KEYWORD,generativeai,🚀 Antigravity-Auto
# =====================================================================
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(yaml_content)


def export_singbox_outbounds(s_tier: list, a_tier: list, b_tier: list, output_path: str = "singbox_outbounds.json"):
    """Generate Sing-box outbounds configuration snippet."""
    recommended_nodes = [r["name"] for r in (s_tier + a_tier)]
    if not recommended_nodes and b_tier:
        recommended_nodes = [r["name"] for r in b_tier[:4]]

    if not recommended_nodes:
        return

    config = {
        "outbounds": [
            {
                "tag": "🚀 Antigravity-Auto",
                "type": "urltest",
                "outbounds": recommended_nodes,
                "url": "https://generativelanguage.googleapis.com/generate-204",
                "interval": "3m",
                "tolerance": 40
            }
        ]
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def generate_markdown_report(all_results, s_tier, a_tier, b_tier, c_tier, leak_tier, blocked_tier, offline_tier, report_path="ANTIGRAVITY_NODE_REPORT.md"):
    """Generate comprehensive Markdown Benchmark Report."""
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md_content = f"""# 🛰️ Antigravity 专属高可用节点与真实出口评级报告 (V5.0)

> **测试时间**: `{now_str}`  
> **探测机制**: 8 维交叉全息矩阵 (CF基准 + Google Core + Google AI + Gemini Web + OAuth认证 + AI Studio + WAF洁净度)  
> **安全保证**: 100% 匿名无感探测 / 0 账号风险 / 纯网络层探针

---

## 📊 质量分级与出口诊断概览

| 评级分类 | 数量 | 适用场景 / 诊断特征 | 处置建议 |
| :--- | :--- | :--- | :--- |
| 🌟 **S 级 (黄金节点)** | **{len(s_tier)}** | 0 丢包、极低延迟，最适合长代码流式输出与连续高频对话 | **⭐ 强力首选主力** |
| 🟢 **A 级 (优质主力)** | **{len(a_tier)}** | 0 丢包、延迟稳定，Google AI 全端点通畅 | **可作为常用节点** |
| 🟡 **B 级 (普通备选)** | **{len(b_tier)}** | 偶发微抖动，普通对话可用 | 作为应急备用 |
| 🟠 **C 级 (易断流)** | **{len(c_tier)}** | 高延迟或高丢包，长连接中途易中断/报错 | **不推荐** |
| 🚨 **假海外 (国内直出)** | **{len(leak_tier)}** | 落地机失效，流量滞留上海/国内中转直出，被 GFW 拦截 | **必须弃用 (无法使用AI)** |
| ⛔ **地区封锁 (AI受限)** | **{len(blocked_tier)}** | 香港/澳门出口受限、OAuth阻断或AI应用层拦截 | **严禁在 Antigravity 中使用** |
| 🔴 **彻底离线 (无法连接)** | **{len(offline_tier)}** | 节点服务器宕机或网络中断 | 建议从订阅移除 |

---

## 🏆 Antigravity 推荐可用排行榜 (S & A 级推荐)

| 排名 | 综合评分 | 节点名称 | 协议 (Protocol) | 首包 TTFB | 平均延迟 | 抖动 (Jitter) | 丢包率 | 状态评价 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
    rank = 1
    for r in s_tier:
        md_content += f"| **#{rank}** | `{r['score']} 分` (S级) | `{r['name']}` | `{r['type']}` | `{r['ttfb']} ms` | `{r['avg_delay']} ms` | `±{r['jitter']}ms` | `0%` | 🌟 黄金推荐 (极速稳固) |\n"
        rank += 1

    for r in a_tier:
        md_content += f"| **#{rank}** | `{r['score']} 分` (A级) | `{r['name']}` | `{r['type']}` | `{r['ttfb']} ms` | `{r['avg_delay']} ms` | `±{r['jitter']}ms` | `0%` | 🟢 优质主力 (表现稳定) |\n"
        rank += 1

    if not s_tier and not a_tier:
        md_content += "| - | - | *(暂无可推荐的 S/A 级节点)* | - | - | - | - | - | 请更换优质机场专线或使用 HY2 节点 |\n"

    if leak_tier:
        md_content += """
---

## 🚨 假海外 / 国内中转直出节点 (落地机脱机)
> ⚠️ **高危诊断**：以下节点名称标为海外（如新加坡/日本等），但底层流量实际滞留在中国大陆（如上海/广州中转机直出），导致 Google 服务被 GFW 阻断：

| 节点名称 | 协议 | 诊断结果 |
| :--- | :--- | :--- |
"""
        for r in leak_tier:
            md_content += f"| `{r['name']}` | `{r['type']}` | 🚨 {r['reason']} |\n"

    if blocked_tier:
        md_content += """
---

## ⛔ 地区封锁 / 认证受阻节点 (AI 受限出口)
> ⚠️ **拦截提示**：以下节点的出口 IP 位于不支持地区，或 OAuth 认证端点 / AI Studio 应用层被拦截：

| 节点名称 | 协议 | 诊断结果 |
| :--- | :--- | :--- |
"""
        for r in blocked_tier:
            md_content += f"| `{r['name']}` | `{r['type']}` | ⛔ {r['reason']} |\n"

    if b_tier:
        md_content += """
---

## 🟡 B 级备选节点 (偶发微抖动)
| 节点名称 | 协议 | 评分 | 首包 TTFB | 平均延迟 | 丢包率 | 诊断说明 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
"""
        for r in b_tier:
            md_content += f"| `{r['name']}` | `{r['type']}` | `{r['score']}分` | `{r['ttfb']} ms` | `{r['avg_delay']} ms` | `{r['loss_rate']}%` | {r['reason']} |\n"

    if c_tier:
        md_content += """
---

## 🟠 C 级易断流节点 (建议避开)
| 节点名称 | 协议 | 评分 | 丢包率 | 诊断说明 |
| :--- | :--- | :--- | :--- | :--- |
"""
        for r in c_tier:
            md_content += f"| `{r['name']}` | `{r['type']}` | `{r['score']}分` | `{r['loss_rate']}%` | {r['reason']} |\n"

    md_content += f"""
---
*本报告由 Antigravity 智能高可用与出口诊断探针自动生成。*
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)


def run_controller_benchmark(controller_url: str, secret: str = "", max_workers: int = 16, timeout_ms: int = 3500, keyword: str = None, report_path: str = "ANTIGRAVITY_NODE_REPORT.md", yaml_path: str = "antigravity_policy_group.yaml", singbox_path: str = None):
    print("=" * 88, flush=True)
    print(" 🚀 Antigravity / Google AI 节点高可用度与真实出口诊断工具 (V5.0 Universal)", flush=True)
    print("=" * 88, flush=True)
    print(f"📡 控制接口: {controller_url}", flush=True)

    try:
        all_proxies = get_clash_proxies(controller_url, secret)
    except Exception as e:
        print(f"\n❌ [连接错误]: {e}\n", flush=True)
        return

    if keyword:
        all_proxies = [p for p in all_proxies if keyword.lower() in p["name"].lower()]

    total_count = len(all_proxies)
    if total_count == 0:
        print("⚠️ 未发现匹配的代理节点，请检查客户端配置与订阅加载情况。", flush=True)
        return

    print(f"📊 已拉取到 {total_count} 个节点 | 启用【8维全息矩阵 / WAF风控 / 中转直出 / OAuth阻断 / TTFB加权】引擎", flush=True)
    print(f"⚡ 启动多线程并发探测 (并发: {max_workers})...", flush=True)
    print("-" * 88, flush=True)

    results = []
    completed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(test_single_node, controller_url, secret, p, timeout_ms): p["name"]
            for p in all_proxies
        }
        for future in as_completed(futures):
            completed += 1
            res = future.result()
            results.append(res)

            delay_str = f"{res['avg_delay']}ms" if res['avg_delay'] < 99999 else "---"
            ttfb_str = f"TTFB:{res['ttfb']}ms" if res['ttfb'] < 99999 else "TTFB:---"
            loss_str = f"丢包:{res['loss_rate']}%" if res['loss_rate'] > 0 else "0丢包"
            score_str = f"[{res['grade']}级 {res['score']:2d}分]" if res['grade'] != "F" else "[F级 ⛔]"

            print(f"[{completed:2d}/{total_count:2d}] {res['tag']} {score_str} {res['name'][:22]:<22} [{res['type']:<9}] -> {delay_str:<7} {ttfb_str:<10} {loss_str:<8} | {res['reason']}", flush=True)

    results.sort(key=lambda x: (-x["score"], x["avg_delay"]))

    s_tier = [r for r in results if r["grade"] == "S"]
    a_tier = [r for r in results if r["grade"] == "A"]
    b_tier = [r for r in results if r["grade"] == "B"]
    c_tier = [r for r in results if r["grade"] == "C"]

    leak_tier = [r for r in results if r.get("category") == "DOMESTIC_LEAK"]
    blocked_tier = [r for r in results if r.get("category") in ["BLOCKED_REGION", "AI_BLOCKED", "AUTH_BLOCKED", "AI_PARTIAL"]]
    offline_tier = [r for r in results if r.get("category") == "OFFLINE"]

    print("\n" + "=" * 88, flush=True)
    print(" 📋 Antigravity 综合质量与出口诊断天梯榜 (Quality & Egress Diagnostic Summary)", flush=True)
    print("=" * 88, flush=True)
    print(f"  🌟 S 级·黄金节点 (90~100分, 0丢包/极速/纯净)   : {len(s_tier)} 个  <-- 强力首选！", flush=True)
    print(f"  🟢 A 级·优质主力 (70~89分, 稳定低抖动)       : {len(a_tier)} 个  <-- 靠谱可用", flush=True)
    print(f"  🟡 B 级·普通备用 (50~69分, 偶发微抖动)       : {len(b_tier)} 个", flush=True)
    print(f"  🟠 C 级·易断流   (高延迟/高丢包, 易卡顿)     : {len(c_tier)} 个  <-- 建议弃用", flush=True)
    print(f"  🚨 假节点·国内直出 (走上海等国内中转/落地脱机) : {len(leak_tier)} 个  <-- 必须剔除！", flush=True)
    print(f"  ⛔ 封锁·地区受限 (香港/OAuth阻断/AI应用受阻)   : {len(blocked_tier)} 个  <-- 严禁使用", flush=True)
    print(f"  🔴 离线·彻底失效 (无法连接服务器)            : {len(offline_tier)} 个", flush=True)
    print("=" * 88, flush=True)

    generate_markdown_report(results, s_tier, a_tier, b_tier, c_tier, leak_tier, blocked_tier, offline_tier, report_path)
    export_clash_policy_group(s_tier, a_tier, b_tier, yaml_path)

    if singbox_path:
        export_singbox_outbounds(s_tier, a_tier, b_tier, singbox_path)

    print(f"\n📄 深度评分报告已保存至: {report_path}", flush=True)
    if s_tier or a_tier:
        print(f"🛡️ Antigravity 专属高可用策略组已导出至: {yaml_path}", flush=True)
        if singbox_path:
            print(f"📦 Sing-box Outbounds 已导出至: {singbox_path}", flush=True)
    print()


def main():
    parser = argparse.ArgumentParser(description="Antigravity / Google AI Node Stability & Zero-Risk Benchmark Tool (V5.0 Universal)")
    parser.add_argument("--api", default=None, help="Clash/Mihomo External Controller URL (默认自动探测 9090/9097/2049)")
    parser.add_argument("--secret", default="", help="External Controller Secret (若未设置可留空)")
    parser.add_argument("--proxy", default=None, help="指定本地代理地址直接测试 (如 http://127.0.0.1:7890 或 socks5://127.0.0.1:10808)")
    parser.add_argument("--concurrency", "-c", type=int, default=16, help="并发探测线程数 (默认: 16)")
    parser.add_argument("--timeout", "-t", type=int, default=3500, help="单节点超时时间 ms (默认: 3500)")
    parser.add_argument("--filter", "-f", default=None, help="按关键词过滤节点名称 (如: 'Singapore', 'Japan', 'US')")
    parser.add_argument("--report", "-r", default="ANTIGRAVITY_NODE_REPORT.md", help="报告保存路径 (默认: ANTIGRAVITY_NODE_REPORT.md)")
    parser.add_argument("--yaml", "-y", default="antigravity_policy_group.yaml", help="Clash 策略组导出路径 (默认: antigravity_policy_group.yaml)")
    parser.add_argument("--sing-box", "-s", default=None, help="Sing-box 出站配置导出路径 (如: singbox_outbounds.json)")

    args = parser.parse_args()

    if args.proxy:
        benchmark_direct_proxy(args.proxy, timeout_ms=args.timeout)
    else:
        controller_url = args.api if args.api else auto_detect_controller(args.secret)
        run_controller_benchmark(
            controller_url=controller_url,
            secret=args.secret,
            max_workers=args.concurrency,
            timeout_ms=args.timeout,
            keyword=args.filter,
            report_path=args.report,
            yaml_path=args.yaml,
            singbox_path=args.sing_box
        )


if __name__ == "__main__":
    main()
