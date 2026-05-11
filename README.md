<h1>📚 Bibliotech Data Platform</h1>

## 📌 Problema de Negócio

A **Bibliotech** é um marketplace que conecta empresas de e-commerce e varejo com publicadores de livros. As análises de negócio eram realizadas diretamente no banco de dados de produção, gerando dois problemas críticos:

- **Lentidão** nas consultas analíticas
- **Risco de derrubar o banco de produção**

A solução foi construir uma **infraestrutura/plataforma de dados dedicada**, capaz de suportar a tomada de decisão sem impactar o ambiente operacional. O principal processo de negócio acompanhado são as **vendas de livros por publicador**.
---

## 🏗️ Arquitetura da Solução

```text
[FTP / GitHub (Excel/CSV)]
    ↓
[Extração - Python]
    ↓
[Staging - PostgreSQL (Render)]
    ↓
[Transformação - SQL (DBeaver)]
    ↓
[DataMart - Modelagem Dimensional (Star Schema)]
    ↓
[Visualização - Metabase]
    ↓
[Agendamento - Rundeck]
    ↓
[Produção - AWS EC2 Windows]
```
---

## 🔄 Etapas do ETL

### 1. 🐄 Extração
- Dados originados em arquivos **CSV/Excel** disponibilizados via **FTP/SFTP/GitHub**
- Script Python (`ingestion.py`) lê os arquivos da URL e carrega no schema `staging` do PostgreSQL

### 2. 🥩 Transformação
- Dados brutos da staging são modelados via **SQL no DBeaver**
- Modelagem dimensional baseada em **Ralph Kimball** (Star Schema)
- Schemas organizados em:
  - `staging` → dados crus
  - `datamart` → tabelas modeladas (Fatos + Dimensões)

### 3. 🍽️ Carga
- Tabelas finais armazenadas no **Data Warehouse PostgreSQL hospedado no Render**

---

## 📊 Modelagem Dimensional (Star Schema)

| Tabela | Tipo | Descrição |
|---|---|---|
| `F_VENDA` | Fato | Vendas de livros (métricas: preço, desconto, datas) |
| `D_LIVRO` | Dimensão | Dados do livro (título, gênero, autor, série) |
| `D_PUBLICADOR` | Dimensão | Dados do publicador (nome, cidade, país, investimento em marketing) |
| `D_FORMATO` | Dimensão | Formato do livro (ex: digital, físico) |

> A modelagem segue os princípios de **Fatos e Dimensões** de Ralph Kimball.

---

## ⏱️ Agendamento com Rundeck

O [Rundeck](https://docs.rundeck.com/) é utilizado para orquestrar e agendar os jobs de ETL automaticamente.

- **Jobs**: Definem o fluxo de execução do ETL
- **Steps**: Comandos Python/Shell executados em cada job
- **Nodes**: Máquina EC2 Windows como executor
- **Monitoramento**: Logs de execução exportados para o banco de dados PostgreSQL (`rundeck_file_logs`)
- **Backend**: PostgreSQL no Render (migrado do H2 padrão)

<img width="886" height="535" alt="image" src="https://github.com/user-attachments/assets/cdb71a23-0851-4fd5-bed8-2c7684668cc7" />
<img width="885" height="375" alt="image" src="https://github.com/user-attachments/assets/0d575d2f-a188-4a2f-bcf3-01107c3ad379" />
<img width="885" height="375" alt="image" src="https://github.com/user-attachments/assets/365c03f7-8fa4-4c79-a9fc-112fdeb605c2" />

---

## ☁️ Deploy em Produção — AWS EC2

A aplicação foi implantada em uma instância **EC2 Windows (m5.xlarge — 4 vCPUs / 16 GB RAM)** na AWS para eliminar a dependência de máquinas locais.

### Stack na EC2

| Componente | Função |
|---|---|
| **Java 11 (JDK)** | Runtime para Rundeck e Metabase |
| **Rundeck** | Orquestrador e agendador de jobs ETL |
| **Metabase** | Dashboard e visualização de dados |
| **Python 3.13** | Scripts de extração e transformação |
| **ETL Script** | `ingestion.py` + `export.py` |

### Configuração de Rede

- Portas **3000** (Metabase) e **4440** (Rundeck) liberadas nos **Security Groups da AWS**
- Firewall do Windows desativado para acesso externo via IP público

<img width="885" height="452" alt="image" src="https://github.com/user-attachments/assets/d07ed28f-b2ce-46ec-8c7c-9eb295638e72" />

<img width="886" height="522" alt="image" src="https://github.com/user-attachments/assets/6f8734f6-43ea-4cbd-869d-43bf25bbe853" />

<img width="886" height="413" alt="image" src="https://github.com/user-attachments/assets/f38dea1a-ee61-4cb6-a7c0-583d5035f59d" />

---

## 📁 Estrutura do Projeto

- `bibliotech-data-platform/`
  - `ingestion.py` — Script de extração e carga na Staging
  - `export.py` — Script de coleta e exportação de logs do Rundeck
  - `requirements.txt` — Dependências Python
  - `requirements_virtualenv.txt`
  - `sql/`
    - `create_staging.sql` — Criação dos schemas e tabelas staging
    - `create_datamart.sql` — Modelagem dimensional (D_ e F_)
    - `queries_negocio.sql` — Consultas analíticas respondendo perguntas de negócio

---

## 🛠️ Stack Tecnológica

<p align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white"/>
  <img src="https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>
  <img src="https://img.shields.io/badge/Metabase-509EE3?style=for-the-badge&logo=metabase&logoColor=white"/>
  <img src="https://img.shields.io/badge/Rundeck-EF2D5E?style=for-the-badge&logo=rundeck&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white"/>
  <img src="https://img.shields.io/badge/DBeaver-372923?style=for-the-badge&logo=dbeaver&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white"/>
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"/>
</p>

Versionamento do código: feito com Git e hospedado no GitHub (https://github.com/VitorCamposAds/bibliotech-data-platform).

Controle de versão: Git (local) → Push para repositório remoto no GitHub.

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.13+
- Java 11 (JDK)
- PostgreSQL
- Conta no Render
- Rundeck 5.8+
- Metabase (JAR)

### 1. Clonar o repositório

```bash
git clone https://github.com/VitorCamposAds/bibliotech-data-platform.git
cd bibliotech-data-platform
```

### 2. Criar ambiente virtual e instalar dependências

```bash
pip install virtualenv
virtualenv venv
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 3. Configurar credenciais do banco

Edite as variáveis de conexão em `ingestion.py`:

```python
host = "SEU_HOST_RENDER"
user = "SEU_USUARIO"
pswd = "SUA_SENHA"
database = "SEU_BANCO"
```

### 4. Executar a extração

```bash
python ingestion.py
```

### 5. Criar a modelagem dimensional

Execute os scripts em `sql/create_datamart.sql` no **DBeaver** conectado ao seu PostgreSQL.

### 6. Ajuste para o Rundeck (`.war` não versionado)

O arquivo `rundeck-5.8.0-20241205.war` **não é armazenado no repositório Git**, pois excede o limite de tamanho permitido. Você deve baixá‑lo manualmente na versão `5.8.0` do site oficial do Rundeck e colocá‑lo na pasta `rundeck/` do projeto, mantendo o mesmo nome. O comando `java -jar rundeck-5.8.0-20241205.war` continua o mesmo, mas o `.war` deve existir fisicamente no seu ambiente local.

### 7. Iniciar o Metabase

```bash
java -jar metabase.jar
# Acesse: http://localhost:3000
```

### 8. Iniciar o Rundeck

```bash
java -jar rundeck-5.8.0-20241205.war
# Acesse: http://localhost:4440 | Login: admin / admin
```

---

## 📈 Perguntas de Negócio Respondidas

- Quais publicadores vendem mais livros do gênero SciFi/Fantasy?
- Qual o preço total, mínimo e máximo por livro e publicador?
- Em quantos dias únicos determinado livro foi vendido?
- Quando foi a última venda registrada de um livro específico?

---

## 👨‍💻 Desenvolvido por

<table>
  <tr>
    <td align="center">
      <b>Vitor Campos</b><br/>
      <sub>Analista de Dados</sub><br/>
      <a href="https://www.linkedin.com/in/vitor-campos-tech">
        <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
      </a>
    </td>
  </tr>
</table>

---

<p align="center">
  Feito por <a href="https://www.linkedin.com/in/vitor-campos-tech"><strong>Vitor Campos</strong></a>
</p>
