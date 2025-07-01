import time

def wait_for_healthy_containers(machine_ip, ssh_key, timeout=1200, interval=10):
    """
    Polls the health status of all running Docker containers on the given machine.
    
    :param machine_ip: IP address of the remote machine
    :param ssh_key: SSH private key path
    :param timeout: Maximum time to wait in seconds (default 20 minutes)
    :param interval: Polling interval in seconds (default 10 seconds)
    """
    start_time = time.time()
    while True:
        health_cmd = "docker container ls --format '{{.Names}} {{.Status}}'"
        result = ParamikoWrapper.ssh_cmd(machine_ip, health_cmd, ssh_key, 'duser', 22)['stdout']
        if isinstance(result, bytes):
            result = result.decode()
        LOGGER.info("Docker health check on %s:\n%s", machine_ip, result.strip())

        lines = result.strip().splitlines()
        healthy_lines = [line for line in lines if 'zabbix-docker-monitor' not in line.lower()]
        if healthy_lines and all('(healthy)' in line.lower() for line in healthy_lines):
            LOGGER.info("✅ All containers healthy on %s", machine_ip)
            break

        if time.time() - start_time > timeout:
            LOGGER.warning("⏱️ Timeout waiting for healthy containers on %s", machine_ip)
            break

        time.sleep(interval)
