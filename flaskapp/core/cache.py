from sqlalchemy.sql import text

def insert_into_cache(conn,nummecanografico,resultado,localpicagem,datahora):

    conn.execute(
        text(
            "insert into auditcache.public.raw (nummecanografico,resultado,localpicagem,datahora) values (:nummecanografico,:resultado,:localpicagem,:datahora)"
        ),
        {"nummecanografico":nummecanografico,
        "resultado":resultado,
        "localpicagem":localpicagem,
        "datahora":datahora}
    )
    if resultado=="S":
        sql = text("select * from auditcache.public.entry where nummecanografico= :nummecanografico and hora_saida is null")
        result = conn.execute(sql, {"nummecanografico":nummecanografico}).first()
        if len(result)>1:
            return "ERROR"
        else:
            sql = text("update auditcache.public.entry set hora_saida=:datahora where nummecanografico= :nummecanografico and hora_saida is null")
             
            conn.execute(sql,
        {"datahora":datahora}
    )
    else:
        conn.execute(
        text(
            "insert into auditcache.public.entry (nummecanografico,hora_entrada) values (:nummecanografico,:hora_entrada)"
        ),{
        "nummecanografico":nummecanografico,
        "hora_entrada":datahora}
    )
    return "ok"
        

def check_action(conn,nummecanografico,resultado,localpicagem,datahora):
    pass