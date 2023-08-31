from sqlalchemy.sql import text
import joblib
import pandas as pd
from datetime import datetime

enc_filename="encoder.sav"
enc = joblib.load(enc_filename)

model_filename="outlier_model.sav"
loaded_model = joblib.load(model_filename)

if_filename="isolation_model.sav"
if_model = joblib.load(if_filename)

def create_date_elements(x):
   # print(x)
    data=x["_source.dataaccao"]
    dt=datetime.strptime(data, '%Y-%m-%dT%H:%M:%S.000Z')
    return dt.year, dt.month, dt.day, dt.hour,dt.minute,dt.second,dt.weekday()

def create_is_weekday(x):
    if x["dtac_weekday"]<5:
        return 1
    else:
        return 0



def insert_into_cache(conn,nummecanografico,resultado,localpicagem,datahora):

    conn.execute(
        text(
            "insert into auditcache.public.raw (nummecanografico,resultado,localpicagem,datahora) values (:nummecanografico,:resultado,:localpicagem,:datahora) ON CONFLICT (nummecanografico, resultado,localpicagem,datahora) DO NOTHING;"
        ),
        {"nummecanografico":nummecanografico,
        "resultado":resultado,
        "localpicagem":localpicagem,
        "datahora":datahora}
    )
    if resultado=="S":
        sql = text("""select * from auditcache.public.entry where nummecanografico= :nummecanografico and hora_saida is null and local_picagem= :localpicagem and DATE_PART('day', :datahora ::timestamp - hora_entrada::timestamp) * 24 +
              DATE_PART('hour', :datahora ::timestamp - hora_entrada::timestamp) between 1 and 24;""")
        #print(sql)
        result = conn.execute(sql, {"nummecanografico":nummecanografico,"localpicagem":localpicagem, "datahora":datahora}).fetchall()
        if len(result)==0:
            return "ERROR,saida sem entrada registada"
        elif len(result)>1:
            print(result)
            return "ERROR, more than one record"
        else:
            print("updating")
            sql = text("""update auditcache.public.entry set hora_saida=:datahora where nummecanografico= :nummecanografico and hora_saida is null and local_picagem= :localpicagem and DATE_PART('day', :datahora ::timestamp - hora_entrada::timestamp) * 24 +
              DATE_PART('hour', :datahora ::timestamp - hora_entrada::timestamp) between 1 and 24""")
             
            conn.execute(sql,
        {"datahora":datahora,"nummecanografico":nummecanografico,"localpicagem":localpicagem}
    )
    else:
        conn.execute(
        text(
            "insert into auditcache.public.entry (nummecanografico,hora_entrada,local_picagem) values (:nummecanografico,:hora_entrada,:localpicagem)  ON CONFLICT (nummecanografico,hora_entrada,local_picagem) DO NOTHING;"
        ),{
        "nummecanografico":nummecanografico,
        "hora_entrada":datahora,"localpicagem":localpicagem}
    )
    return "ok"
        

def check_action(conn,nummecsonho,ADLOCPC_2,ADLOCPC_4,desunidade,dataaccao):
    sql = text("""select * from auditcache.public.entry where nummecanografico= :nummecsonho and hora_entrada <= :dataaccao and DATE_PART('day', :dataaccao ::timestamp - hora_entrada::timestamp) * 24 +
              DATE_PART('hour', :dataaccao ::timestamp - hora_entrada::timestamp) between 0 and 24 and (DATE_PART('day', :dataaccao ::timestamp - hora_saida::timestamp) * 24 +
              DATE_PART('hour', :dataaccao ::timestamp - hora_saida::timestamp) between -24 and 0 or hora_saida is null)""")
   # print(sql)
    result = conn.execute(sql, {"nummecsonho":nummecsonho,"dataaccao":dataaccao}).fetchall()
  #  print(result)
    if len(result)==0:
        #print("eeeee")
        return "Alerta: sem registo de entrada"
    elif len(result)>1:
        #print(result)
        return "ERROR, more than one record"
    elif len(result)==1:
        print(result)
        localpicagem=result[0][3]
        result_local=check_match_picagem(localpicagem,ADLOCPC_4)
        if result_local=="ok":
            return "ok"
        else:
            return "Alerta: Local diferente registado na entrada"
    else:
       # print(result is None)
       # print(len(result))
        return "what??"
    


def check_match_picagem(localpicagem,ADLOCPC_4):
   # print(localpicagem,ADLOCPC_4)
    dict_match={"AVEIRO":["CHBV Computadores","Hospital Aveiro"]}
    print(dict_match[localpicagem])

    if ADLOCPC_4 in dict_match[localpicagem]:
        print("in here")
        return "ok"
    else:
        return "ERROR"
    

def truncate_date():
    pass


def outlier_check(row):

    out_cols=['_source.numfuncionario', '_source.Caminhofunc:0',
       '_source.Caminhofunc:4', '_source.desunidade', '_source.ADLOCPC:1',
       '_source.adtipofuncionario', '_source.mudulo', '_source.descaplicacao',
       '_source.codacesso', '_source.Caminhofunc:5', '_source.ADLOCPC:4',
       '_source.dnsname', '_source.ADLOCPC:5', '_source.ADLOCPC:0',
       '_source.nummecsonho', '_source.addepfuncionario', '_source.ADLOCPC:2',
       '_source.Caminhofunc:1', '_source.codintituicao',
       '_source.nomeaplicacao', '_source.desaplicacao',
       '_source.desgrupofuncsonho', '_source.activosonho',
       '_source.ipcomputador', '_source.ADLOCPC:3', '_source.ADLOCPC:6',
       '_source.codgrupofuncsonho', '_source.Caminhofunc:2',
       '_source.Caminhofunc:3', '_source.adestadofuncionario',
       '_source.ADLOCPC:7', '_source.ADLOCPC:8', '_source.Caminhofunc:6',
       '_source.ADLOCPC:9', '_source.ADLOCPC:10', 'dtac_year', 'dtac_month',
       'dtac_day', 'dtac_hour', 'dtac_minute', 'dtac_second', 'dtac_weekday',
       'isweekday']
    #print(row)
    #row_df=pd.DataFrame(row)
    #print(row_df)
    df =pd.json_normalize([row])
    print(df)
    df[["dtac_year","dtac_month","dtac_day","dtac_hour","dtac_minute","dtac_second","dtac_weekday"]]=df.apply(create_date_elements,axis=1,result_type="expand")
    df["isweekday"]=df.apply(create_is_weekday,axis=1)
    X=enc.transform(df[out_cols])
    dect=loaded_model.predict(X)
    ifpred=if_model.predict(X)
    if dect==[0] and ifpred==1:
        return "ok"
    elif dect==[1] or ifpred==-1: #um apenas
        return "Aviso: Possivel outlier"
    else: 
        return "Alerta: Outlier"