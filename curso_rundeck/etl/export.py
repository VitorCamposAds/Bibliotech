import pandas as pd
from json import loads
from glob import glob
from xmltodict import parse
from datetime import datetime
from sqlalchemy import create_engine

logs_path = "C:/projetos/rundeck/var/logs/rundeck/prod/job/*"
host = "dpg-d7prd0l7vvec73fh8l00-a.oregon-postgres.render.com"
user = "admin123"
pswd = "Zfqw6iRCvkK538qgEUGMddFDCro6Exp6"
database = "rundeck"
string_conn = f"postgresql+psycopg2://{user}:{pswd}@{host}/{database}"
engine = create_engine(string_conn)

jsons, xmls = [], []
for job_path in glob(logs_path):
    job_path = job_path.replace("\\", "/")
    job_id = job_path.split("/")[-1]

    xml_paths = glob(f"{job_path}/logs/*.xml")
    json_paths = glob(f"{job_path}/logs/*.json")

    xml_data = []
    for xml_path in xml_paths:
        with open(xml_path, "r") as xml:
            xml_dict = parse("\n".join(xml.readlines()))
            xml_dict = xml_dict["executions"]["execution"]
            
            xml_data.append({
                "job_id": xml_dict["jobId"],
                "execution_id": int(xml_dict["@id"]),
                "project": xml_dict["project"],
                "job_user": xml_dict["user"] 
            })

    json_data = []
    for json_path in json_paths:
        with open(json_path, "r") as json:
            json_dict = loads(json.readlines()[0])
            
            json_data.append({
                "job_id": job_id,
                "execution_id": int(json_dict["executionId"]),
                "execution_state": json_dict["executionState"],
                "completed": json_dict["completed"],
                "update_time": json_dict["updateTime"],
                "start_time": json_dict["startTime"],
                "end_time": json_dict["endTime"]
            })

    jsons.extend(json_data)
    xmls.extend(xml_data)

dfj = pd.DataFrame(jsons)
dfx = pd.DataFrame(xmls)

df = dfj.merge(
    dfx,
    on=["job_id", "execution_id"],
    how="inner"
)

df["start_time"] = pd.to_datetime(df["start_time"])
df["end_time"] = pd.to_datetime(df["end_time"])
df["update_time"] = pd.to_datetime(df["end_time"])
df["collection_time"] = datetime.now()

df.to_sql("rundeck_file_logs", schema="public", index=False, if_exists="replace", con=engine)
