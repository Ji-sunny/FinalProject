from sqlalchemy import create_engine
from sqlalchemy import sql
def conn():
    conn = create_engine('oracle+cx_oracle://farmaitest:123456@193.122.124.189:1521/xe')
    # 서버에서 돌릴 때만 세션에 date format 다르게 사용
    # sqlquery = sql.expression.text("alter session set NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'")
    # conn.execute(sqlquery)
    return conn