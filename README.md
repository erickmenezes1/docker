Este projeto configura um ambiente de monitoramento completo utilizando Docker para hospedar um servidor Zabbix, frontend, banco de dados PostgreSQL, Grafana e agente Zabbix.

## Pré-requisitos

- Docker instalado em sua máquina
- Docker Compose (opcional, se preferir usar um arquivo `docker-compose.yml`)

## Estrutura do Projeto

A estrutura do projeto deve ser organizada da seguinte maneira:

```
.
├── zabbix
│   ├── postgres
│   └── alertscripts
└── setup.py
```

- `zabbix/postgres`: Diretório para armazenar dados do PostgreSQL.
- `zabbix/alertscripts`: Diretório para scripts de alerta do Zabbix.
- `setup.py`: Script Python para iniciar os containers Docker.

## Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/erickmenezes1/docker
   cd docker
   ```

2. Crie os diretórios necessários:

   ```bash
   mkdir -p zabbix/postgres zabbix/alertscripts
   ```

## Uso

Execute o script `setup.py` para criar a network Docker e iniciar os containers:

```bash
python setup.py
```

### Descrição dos Containers

O script cria e configura os seguintes containers:

1. **PostgreSQL**:
   - Armazena os dados do Zabbix.
   - Porta: `5432`

2. **Zabbix Server**:
   - Principal servidor Zabbix.
   - Porta: `10051`

3. **Zabbix Frontend**:
   - Interface web do Zabbix.
   - Portas: `80` (HTTP), `443` (HTTPS)

4. **Grafana**:
   - Ferramenta de visualização e monitoramento.
   - Porta: `3000`

5. **Zabbix Agent**:
   - Agente Zabbix para coleta de dados.
   - Porta: `10050`
