import subprocess
import os

def run_docker_containers():
    # Caminho absoluto para os volumes
    current_dir = os.path.abspath(os.getcwd())
    postgres_data_dir = os.path.join(current_dir, 'zabbix', 'postgres')
    alertscripts_dir = os.path.join(current_dir, 'zabbix', 'alertscripts')

    commands = [
        # PostgreSQL 
        [
            "docker", "run", "--name", "some-postgres",
            "--network", "network-zabbix",
            "-p", "5432:5432",
            "-v", f"{postgres_data_dir}:/var/lib/postgresql/data",
            "-e", "POSTGRES_USER=zabbix",
            "-e", "POSTGRES_PASSWORD=zabbix",
            "-e", "POSTGRES_DB=zabbix",
            "-d", "postgres"
        ],
        # Zabbix server 
        [
            "docker", "run", "--name", "zabbix-server",
            "--network", "network-zabbix",
            "--link", "some-postgres",
            "--restart", "always",
            "-p", "10051:10051",
            "-v", f"{alertscripts_dir}:/usr/lib/zabbix/alertscripts",
            "-e", "DB_SERVER_HOST=172.18.0.2",
            "-e", "POSTGRES_USER=zabbix",
            "-e", "POSTGRES_PASSWORD=zabbix",
            "-e", "POSTGRES_DB=zabbix",
            "-e", "ZBX_SERVER_HOST=172.18.0.3",
            "--init",
            "-d", "zabbix/zabbix-server-pgsql:latest"
        ],
        # Zabbix frontend 
        [
            "docker", "run", "--name", "zabbix-frontend",
            "--network", "network-zabbix",
            "--link", "some-postgres",
            "--restart", "always",
            "-p", "80:8080",
            "-p", "443:8443",
            "-e", "DB_SERVER_HOST=172.18.0.2",
            "-e", "POSTGRES_USER=zabbix",
            "-e", "POSTGRES_PASSWORD=zabbix",
            "-e", "POSTGRES_DB=zabbix",
            "-e", "ZBX_SERVER_HOST=172.18.0.3",
            "-e", "PHP_TZ=AMERICA/Sao_Paulo",
            "--init",
            "-d", "zabbix/zabbix-web-apache-pgsql:latest"
        ],
        # Grafana 
        [
            "docker", "run", "--name", "grafana",
            "--network", "network-zabbix",
            "--link", "some-postgres",
            "--link", "zabbix-server",
            "--restart", "always",
            "-p", "3000:3000",
            "-e", "GF_INSTALL_PLUGINS=alexanderzobnin-zabbix-app",
            "-d", "grafana/grafana"
        ],
        # Zabbix agent 
        [
            "docker", "run", "--name", "zabbix-agent-bd",
            "--network", "network-zabbix",
            "--link", "zabbix-server",
            "--restart", "always",
            "--privileged",
            "-v", "/var/run:/var/run",
            "-p", "10050:10050",
            "-e", "ZBX_HOSTNAME=zabbix-server",
            "-e", "ZBX_SERVER_HOST=172.18.0.2",
            "-d", "zabbix/zabbix-agent:latest"
        ]
    ]

    for command in commands:
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print(f"Container '{command[3]}' iniciado com sucesso:", result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Erro ao iniciar o container '{command[3]}':", e.stderr)

# Criação da network
def create_network():
    try:
        subprocess.run(["docker", "network", "create", "network-zabbix"], check=True, capture_output=True, text=True)
        print("Network 'network-zabbix' criada com sucesso.")
    except subprocess.CalledProcessError as e:
        print("Erro ao criar a network 'network-zabbix':", e.stderr)

# Executa o script
create_network()
run_docker_containers()
