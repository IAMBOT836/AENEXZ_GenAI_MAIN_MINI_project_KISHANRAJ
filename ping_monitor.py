"""
SmartGen AI — Local Ping Monitor
---------------------------------
Runs locally to keep the Streamlit Cloud app alive by pinging it
every 30 minutes. Logs each ping with timestamp and HTTP status.

Usage:
    python ping_monitor.py
    python ping_monitor.py --url https://your-app.streamlit.app --interval 20

The GitHub Actions workflow (.github/workflows/keep_alive.yml)
does the same thing automatically in the cloud — no need to run
this locally unless you want an extra layer of reliability.
"""

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("❌ requests not found. Install with: pip install requests")
    sys.exit(1)

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
DEFAULT_URL      = os.environ.get("APP_URL", "https://your-app.streamlit.app")
DEFAULT_INTERVAL = 30   # minutes
LOG_FILE         = "ping_monitor.log"

# ─────────────────────────────────────────────
# Logging Setup
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("PingMonitor")

BANNER = r"""
  ╔══════════════════════════════════════════════╗
  ║       SmartGen AI — Ping Monitor 🏓          ║
  ║  Keeping your Streamlit app alive 24/7       ║
  ╚══════════════════════════════════════════════╝
"""


def ping(url: str, timeout: int = 30) -> dict:
    """
    Sends a GET request to the given URL and returns status info.
    Also pings the Streamlit health endpoint.
    """
    result = {
        "url": url,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "main_status": None,
        "health_status": None,
        "alive": False,
        "error": None,
    }

    try:
        # 1. Ping main app URL
        resp = requests.get(url, timeout=timeout, allow_redirects=True)
        result["main_status"] = resp.status_code
        result["alive"] = 200 <= resp.status_code < 400

        # 2. Ping Streamlit health endpoint
        health_url = url.rstrip("/") + "/_stcore/health"
        try:
            h_resp = requests.get(health_url, timeout=15)
            result["health_status"] = h_resp.status_code
        except Exception:
            result["health_status"] = "N/A"

    except requests.exceptions.ConnectionError as e:
        result["error"] = f"Connection error: {e}"
    except requests.exceptions.Timeout:
        result["error"] = "Request timed out"
    except Exception as e:
        result["error"] = str(e)

    return result


def format_status(result: dict) -> str:
    """Formats a ping result into a readable string."""
    if result["error"]:
        icon = "❌"
        status = f"ERROR — {result['error']}"
    elif result["alive"]:
        icon = "✅"
        status = f"ALIVE  (HTTP {result['main_status']} | Health: {result['health_status']})"
    else:
        icon = "⚠️ "
        status = f"SLOW WAKE (HTTP {result['main_status']} | Health: {result['health_status']})"
    return f"{icon} {result['timestamp']} — {status}"


def run_monitor(url: str, interval_minutes: int):
    """Main monitoring loop — pings indefinitely."""
    print(BANNER)
    log.info("━" * 58)
    log.info("  SmartGen AI Ping Monitor Starting")
    log.info(f"  🔗 Target URL : {url}")
    log.info(f"  ⏱️  Interval   : Every {interval_minutes} minutes")
    log.info(f"  📝 Log file   : {LOG_FILE}")
    log.info("  Press Ctrl+C to stop")
    log.info("━" * 58)

    ping_count = 0
    success_count = 0
    fail_count = 0

    try:
        while True:
            ping_count += 1
            log.info(f"📡 Ping #{ping_count} starting...")

            result = ping(url)
            status_line = format_status(result)
            log.info(status_line)

            if result["alive"]:
                success_count += 1
            else:
                fail_count += 1

            # Stats summary every 10 pings
            if ping_count % 10 == 0:
                uptime_pct = (success_count / ping_count) * 100
                log.info("─" * 58)
                log.info(f"  📊 Stats — Total: {ping_count} | ✅ OK: {success_count} | ❌ Fail: {fail_count} | Uptime: {uptime_pct:.1f}%")
                log.info("─" * 58)

            # Wait for next ping
            next_time = datetime.now().strftime("%H:%M:%S")
            log.info(f"⏳ Next ping in {interval_minutes} minutes... (current: {next_time})\n")
            time.sleep(interval_minutes * 60)

    except KeyboardInterrupt:
        log.info("\n🛑 Ping monitor stopped by user.")
        log.info(f"📊 Final stats — Pings: {ping_count} | OK: {success_count} | Fail: {fail_count}")
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description="SmartGen AI — Ping Monitor to keep Streamlit app alive",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ping_monitor.py
  python ping_monitor.py --url https://your-app.streamlit.app
  python ping_monitor.py --url https://your-app.streamlit.app --interval 20
        """
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Streamlit app URL to ping (default: {DEFAULT_URL})",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL,
        help=f"Ping interval in minutes (default: {DEFAULT_INTERVAL})",
    )
    args = parser.parse_args()

    if "your-app.streamlit.app" in args.url:
        print("⚠️  WARNING: You're using the placeholder URL.")
        print("   Update --url with your actual Streamlit Cloud URL.")
        print("   e.g.: python ping_monitor.py --url https://myapp.streamlit.app\n")

    run_monitor(url=args.url, interval_minutes=args.interval)


if __name__ == "__main__":
    main()
