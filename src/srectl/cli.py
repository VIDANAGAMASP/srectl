import math
import sys

from srectl.checks.tcp import check_tcp_connectivity


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    prog = sys.argv[0] if sys.argv else "srectl"

    if len(args) not in (2, 3):
        print(f"Usage: {prog} <host> <port> [timeout]", file=sys.stderr)
        return 2

    host = args[0]

    try:
        
        port_raw = args[1].strip()
        if not port_raw or port_raw.lower() in {"true", "false"}:
            raise ValueError(f"invalid port: {args[1]!r}")
        port = int(port_raw)

        if len(args) == 3:
            timeout = float(args[2])
            if not math.isfinite(timeout):
                raise ValueError(f"timeout must be finite, got {args[2]!r}")
        else:
            timeout = 3.0
    except ValueError as exc:
        print(f"Error: invalid argument ({exc})", file=sys.stderr)
        return 2

    try:
        result = check_tcp_connectivity(host=host, port=port, timeout=timeout)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    status = "UP" if result["reachable"] else "DOWN"
    print(
        f"[{status}] {result['host']}:{result['port']} "
        f"(latency={result['latency_ms']}ms, error={result['error']})"
    )
    return 0 if result["reachable"] else 1


if __name__ == "__main__":
    sys.exit(main())