#!/usr/bin/env python3
"""
🛰️ Antigravity Node Benchmark (个人 Flclash 定制入口)
自动将测试产物 (报告与策略组) 定向保存至个人文件夹: backup_flclash_custom_v4.5/
"""

import os
import sys
import argparse
from main import (
    auto_detect_controller,
    benchmark_direct_proxy,
    run_controller_benchmark
)

# 定位个人专属数据文件夹
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PERSONAL_DIR = os.path.join(CURRENT_DIR, "backup_flclash_custom_v4.5")
os.makedirs(PERSONAL_DIR, exist_ok=True)

DEFAULT_REPORT_PATH = os.path.join(PERSONAL_DIR, "ANTIGRAVITY_NODE_REPORT.md")
DEFAULT_YAML_PATH = os.path.join(PERSONAL_DIR, "antigravity_policy_group.yaml")
DEFAULT_SINGBOX_PATH = os.path.join(PERSONAL_DIR, "singbox_outbounds.json")


def main():
    parser = argparse.ArgumentParser(description="Antigravity / Google AI Node Stability & Exit IP Fraud Audit Benchmark (个人自用入口)")
    parser.add_argument("--api", default=None, help="Clash/Mihomo External Controller URL (默认自动探测 9090/9097/2049)")
    parser.add_argument("--secret", default="", help="External Controller Secret (若未设置可留空)")
    parser.add_argument("--proxy", default=None, help="指定本地代理地址直接测试 (如 http://127.0.0.1:7890 或 socks5://127.0.0.1:10808)")
    parser.add_argument("--concurrency", "-c", type=int, default=16, help="并发探测线程数 (默认: 16)")
    parser.add_argument("--timeout", "-t", type=int, default=3500, help="单节点超时时间 ms (默认: 3500)")
    parser.add_argument("--filter", "-f", default=None, help="按关键词过滤节点名称 (如: 'Singapore', 'Japan', 'US')")
    parser.add_argument("--report", "-r", default=DEFAULT_REPORT_PATH, help=f"报告保存路径 (默认个人目录: {DEFAULT_REPORT_PATH})")
    parser.add_argument("--yaml", "-y", default=DEFAULT_YAML_PATH, help=f"Clash 策略组导出路径 (默认个人目录: {DEFAULT_YAML_PATH})")
    parser.add_argument("--sing-box", "-s", default=None, help="Sing-box 出站配置导出路径 (可指定个人目录)")

    args = parser.parse_args()

    print(f"📁 [个人定制模式] 测试产物将自动归档至个人目录: {PERSONAL_DIR}\n", flush=True)

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
