from sqlalchemy.sql import text

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
        {"datahora":datahora,"nummecanografico":nummecanografico,"localpicagem":localpicagem,"datahora":datahora}
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
        return "sem registo"
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
            return "local errado"
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