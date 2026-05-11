# Ir até a pasta do diretório do projeto
cd C:\projetos\curso_rundeck\

# Ativar ambiente virtual
.\Scripts\activate

# Rodar Ingestion
python .\etl\ingestion.py

# Rodar Modelagem Dimensional
python .\etl\dimensional.py