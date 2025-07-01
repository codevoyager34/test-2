import time

def wait_for_healthy_containers(machine_ip, ssh_key, timeout=1200, interval=10):
    """
    Polls the health status of all running Docker containers on the given machine.

    :param machine_ip: IP address of the remote machine
    :param ssh_key: path to SSH private key used for authentication
    :param timeout: max number of seconds to wait (default: 1200s / 20 minutes)
    :param interval: polling interval in seconds (default: 10s)
    """
    LOGGER.info("Waiting for healthy Docker containers on %s", machine_ip)
    start_time = time.time()

    health_cmd = "docker inspect --format='{{{{.Name}}}} {{{{.State.Health.Status}}}}' $(docker ps -q)"

    while True:
        result = ParamikoWrapper.ssh_cmd(machine_ip, health_cmd, ssh_key, 'duser', 22)
        output = result.get('stdout', b'')
        if isinstance(output, bytes):
            output = output.decode()

        LOGGER.info("Health status on %s:\n%s", machine_ip, output.strip())
        lines = output.strip().splitlines()

        if lines and all('healthy' in line for line in lines):
            LOGGER.info("✅ All containers are healthy on %s", machine_ip)
            break

        if time.time() - start_time > timeout:
            LOGGER.error("❌ Timeout: Not all containers became healthy on %s within %s seconds", machine_ip, timeout)
            break

        time.sleep(interval)
