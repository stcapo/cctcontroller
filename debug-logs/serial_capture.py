#!/usr/bin/env python3
"""Timestamped serial capture for Matter / Apple Home debugging."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import time
from pathlib import Path

import serial

INTERESTING = re.compile(
    r"(wifi|wlan|sta|ip|ipv6|dhcp|mdns|dns|matter|chip|case|pase|fabric|"
    r"session|subscribe|unavail|disconnect|reconnect|fail|error|timeout|"
    r"rssi|assoc|auth|beacon|mrp|secure|commission|fabric|node|"
    r"apple|homekit|operational|route|ndp|ra\b|offline|online|keepalive|"
    r"light_matter|zero_code|esp_netif|got ip|disconnected)",
    re.IGNORECASE,
)

FILTERS = {
    "factory-reset": re.compile(
        r"(ESP-ROM|"
        r"rst:0x|"
        r"Reboot count|"
        r"Resetting reboot count|"
        r"^factory_reset:|"
        r"Starting factory reset|"
        r"Factory reset completed|"
        r"Factory reset triggered|"
        r"nvs partition erase|"
        r"Last fabric removed|"
        r"Already commissioned|"
        r"WiFi station (not |already )?provisioned)",
        re.IGNORECASE,
    ),
}
SKIP_LINE = re.compile(r"Product Config:")


def now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def open_serial(port: str, baud: int) -> serial.Serial:
    ser = serial.Serial(
        port,
        baud,
        timeout=0.2,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        xonxoff=False,
        rtscts=False,
        dsrdtr=False,
    )
    ser.dtr = False
    ser.rts = False
    return ser


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default="/dev/cu.usbserial-14220")
    parser.add_argument("--baud", type=int, default=74880)
    parser.add_argument(
        "--out",
        default="/Users/apple/projects/cctcontroller/debug-logs/factory-reset-watch.log",
    )
    parser.add_argument(
        "--filter",
        choices=sorted(FILTERS),
        help="Only print matching lines. Full raw log still goes to --out.",
    )
    args = parser.parse_args()
    line_filter = FILTERS.get(args.filter) if args.filter else None

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    interesting_path = out_path.with_name(out_path.stem + ".interesting.log")

    ser = open_serial(args.port, args.baud)

    header = (
        f"# serial capture start {now()}\n"
        f"# port={args.port} baud={args.baud} filter={args.filter or 'all'}\n"
    )
    print(header, end="", flush=True)
    with out_path.open("a", encoding="utf-8") as raw, interesting_path.open(
        "a", encoding="utf-8"
    ) as interesting:
        raw.write(header)
        interesting.write(header)
        raw.flush()
        interesting.flush()
        buf = b""
        try:
            while True:
                try:
                    chunk = ser.read(1024)
                except serial.SerialException as exc:
                    print(f"# serial dropped: {exc}; reconnecting...\n", end="", flush=True)
                    try:
                        ser.close()
                    except Exception:
                        pass
                    while True:
                        try:
                            ser = open_serial(args.port, args.baud)
                            print(f"# serial reconnected {now()}\n", end="", flush=True)
                            buf = b""
                            break
                        except (serial.SerialException, OSError):
                            time.sleep(0.3)
                            continue
                    continue
                if not chunk:
                    continue
                buf += chunk
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    text = line.replace(b"\r", b"").decode("utf-8", errors="replace")
                    stamped = f"{now()} | {text}\n"
                    raw.write(stamped)
                    raw.flush()
                    if SKIP_LINE.search(text):
                        continue
                    if line_filter is None or line_filter.search(text):
                        print(stamped, end="", flush=True)
                    if INTERESTING.search(text):
                        interesting.write(stamped)
                        interesting.flush()
        except KeyboardInterrupt:
            footer = f"# serial capture stop {now()}\n"
            raw.write(footer)
            interesting.write(footer)
            print(footer, end="", flush=True)
            return 0


if __name__ == "__main__":
    sys.exit(main())
