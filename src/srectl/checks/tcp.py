import socket
import time

def check_tcp_connectivity(host: str ,port: int ,timeout: float= 3.0)-> dict:
    """
    attempt a tcp 3-way handshake (SYN-> SYN-ACK-> ACK) to host:port.
    returns a structured dictionary representing the operational result.
    """
    host= host.strip()
    if not host:
        raise ValueError("Host cannor be empty")
    if isinstance(port,bool) or not isinstance(port,int) or (1<= port<= 65536):
        raise ValueError("Port should be an intege")
    if timeout<= 0:
        raise ValueError("Time cant be zero and negative")
    start_time= time.monotonic()
    try:
        with socket.create_connection((host,port),timeout):
            latency_ms= round((time.monotonic()-start_time)*1000,2)
            return {
                "host": host,
                "port": port,
                "reachable": True,
                "latency_ms": latency_ms,
                "error": None,
            }

    except OSError as exc:
        latency_ms = round((time.monotonic()-start_time)*1000,2)
        return {
            "host": host,
            "port": port,
            "reachable": False,
            "latency_ms": latency_ms,
            "error": f"{type(exc).__name__}: {exc}"
        }