from sqlalchemy import create_engine, text
import os
from collections import defaultdict
import json
import csv
import pandas as pd

db_connection_string = "mysql+pymysql://7e8ex03z9e7w6i2vello:pscale_pw_BHzsATGo0hD5fgiDlLiFy4aCF2fyFH23ox5IpIp5u9r@aws.connect.psdb.cloud/dashboard?charset=utf8mb4"

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def login_user(username, password):
  with engine.connect() as conn:
    result = conn.execute(
      text("SELECT * FROM user WHERE username = :user AND password = :passw"),
      {
        "user": username,
        "passw": password
      })
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return list(rows[0])


def getData():
  with engine.connect() as conn:
    # syr_sec, syr_top, syr_pes, eyr_sec, eyr_top, eyr_pes, , ,  top_con, reg_sec = []
    result = conn.execute(
      text(
        "SELECT intensity, sector FROM mytable WHERE sector IS NOT NULL AND intensity IS NOT NULL"
      ))
    int_sec_list = list(result.all())
    int_sec = [{
      "intensity": intensity,
      "sector": sector
    } for intensity, sector in int_sec_list]

    result2 = conn.execute(
      text(
        "SELECT intensity,topic FROM mytable WHERE topic IS NOT NULL AND intensity IS NOT NULL"
      ))
    int_top_list = list(result2.all())
    int_top = [{
      "intensity": intensity,
      "topic": topic
    } for intensity, topic in int_top_list]

    result3 = conn.execute(
      text(
        "SELECT intensity,pestle FROM mytable WHERE pestle IS NOT NULL AND intensity IS NOT NULL"
      ))
    int_pes_list = list(result3.all())
    int_pes = [{
      "intensity": intensity,
      "pestle": pestle
    } for intensity, pestle in int_pes_list]

    result4 = conn.execute(
      text(
        "SELECT relevance, sector FROM mytable WHERE sector IS NOT NULL AND relevance IS NOT NULL"
      ))
    rel_sec_list = list(result4.all())
    rel_sec = [{
      "relevance": relevance,
      "sector": sector
    } for relevance, sector in rel_sec_list]

    result5 = conn.execute(
      text(
        "SELECT relevance,topic FROM mytable WHERE topic IS NOT NULL AND relevance IS NOT NULL"
      ))
    rel_top_list = list(result5.all())
    rel_top = [{
      "relevance": relevance,
      "topic": topic
    } for relevance, topic in rel_top_list]

    result6 = conn.execute(
      text(
        "SELECT relevance,pestle FROM mytable WHERE pestle IS NOT NULL AND relevance IS NOT NULL"
      ))
    rel_pes_list = list(result6.all())
    rel_pes = [{
      "relevance": relevance,
      "pestle": pestle
    } for relevance, pestle in rel_pes_list]

    result7 = conn.execute(
      text(
        "SELECT country, COUNT(*) AS frequency FROM mytable where country IS NOT NULL GROUP BY country"
      ))
    con_freq_list = list(result7.all())
    con_freq = [{
      "country": country,
      "frequency": frequency
    } for country, frequency in con_freq_list]

    result8 = conn.execute(
      text(
        "SELECT topic, COUNT(*) AS frequency FROM mytable where topic IS NOT NULL GROUP BY topic"
      ))
    top_freq_list = list(result8.all())
    top_freq = [{
      "topic": topic,
      "frequency": frequency
    } for topic, frequency in top_freq_list]

    result9 = conn.execute(
      text(
        "SELECT start_year, COUNT(*) AS frequency FROM mytable WHERE pestle =  'Organization' AND start_year IS NOT NULL GROUP BY pestle, start_year ORDER BY start_year"
      ))
    org_yr_freq_list = list(result9.all())
    org_yr_freq = [{
      "start_year": start_year,
      "frequency": frequency
    } for start_year, frequency in org_yr_freq_list]

    result10 = conn.execute(
      text(
        "SELECT start_year, COUNT(*) AS frequency FROM mytable WHERE pestle =  'Political' AND start_year IS NOT NULL GROUP BY pestle, start_year ORDER BY start_year"
      ))
    pol_yr_freq_list = list(result10.all())
    pol_yr_freq = [{
      "start_year": start_year,
      "frequency": frequency
    } for start_year, frequency in pol_yr_freq_list]

    result11 = conn.execute(
      text(
        "SELECT start_year, COUNT(*) AS frequency FROM mytable WHERE pestle =  'Environmental' AND start_year IS NOT NULL GROUP BY pestle, start_year ORDER BY start_year"
      ))
    env_yr_freq_list = list(result11.all())
    env_yr_freq = [{
      "start_year": start_year,
      "frequency": frequency
    } for start_year, frequency in env_yr_freq_list]

    result12 = conn.execute(
      text(
        "SELECT start_year, COUNT(*) AS frequency FROM mytable WHERE pestle =  'Healthcare' AND start_year IS NOT NULL GROUP BY pestle, start_year ORDER BY start_year"
      ))
    hlt_yr_freq_list = list(result12.all())
    hlt_yr_freq = [{
      "start_year": start_year,
      "frequency": frequency
    } for start_year, frequency in hlt_yr_freq_list]

    result13 = conn.execute(
      text(
        "SELECT start_year, COUNT(*) AS frequency FROM mytable WHERE pestle =  'Lifestyles' AND start_year IS NOT NULL GROUP BY pestle, start_year ORDER BY start_year"
      ))
    lif_yr_freq_list = list(result13.all())
    lif_yr_freq = [{
      "start_year": start_year,
      "frequency": frequency
    } for start_year, frequency in lif_yr_freq_list]

    result14 = conn.execute(
      text(
        "SELECT start_year, COUNT(*) AS frequency FROM mytable WHERE pestle =  'Technological' AND start_year IS NOT NULL GROUP BY pestle, start_year ORDER BY start_year"
      ))
    tech_yr_freq_list = list(result14.all())
    tech_yr_freq = [{
      "start_year": start_year,
      "frequency": frequency
    } for start_year, frequency in tech_yr_freq_list]

    result15 = conn.execute(
      text(
        "SELECT start_year, COUNT(*) AS frequency FROM mytable WHERE pestle =  'Economic' AND start_year IS NOT NULL GROUP BY pestle, start_year ORDER BY start_year"
      ))
    eco_yr_freq_list = list(result15.all())
    eco_yr_freq = [{
      "start_year": start_year,
      "frequency": frequency
    } for start_year, frequency in eco_yr_freq_list]

    result16 = conn.execute(
      text(
        "SELECT start_year, COUNT(*) AS frequency FROM mytable WHERE pestle =  'Industries' AND start_year IS NOT NULL GROUP BY pestle, start_year ORDER BY start_year"
      ))
    ind_yr_freq_list = list(result16.all())
    ind_yr_freq = [{
      "start_year": start_year,
      "frequency": frequency
    } for start_year, frequency in ind_yr_freq_list]

    result17 = conn.execute(
      text(
        "SELECT start_year, COUNT(*) AS frequency FROM mytable WHERE pestle =  'Social' AND start_year IS NOT NULL GROUP BY pestle, start_year ORDER BY start_year"
      ))
    soc_yr_freq_list = list(result17.all())
    soc_yr_freq = [{
      "start_year": start_year,
      "frequency": frequency
    } for start_year, frequency in soc_yr_freq_list]

    result18 = conn.execute(
      text(
        "SELECT country, COUNT(*) AS frequency FROM mytable WHERE country IS NOT NULL AND sector='Government' GROUP BY country"
      ))
    gov_cou_freq_list = list(result18.all())
    gov_cou_freq = [{
      "country": country,
      "frequency": frequency
    } for country, frequency in gov_cou_freq_list]

    result19 = conn.execute(
      text(
        "SELECT country, COUNT(*) AS frequency FROM mytable WHERE country IS NOT NULL AND sector='Transport' GROUP BY country"
      ))
    tra_cou_freq_list = list(result19.all())
    tra_cou_freq = [{
      "country": country,
      "frequency": frequency
    } for country, frequency in tra_cou_freq_list]

    result20 = conn.execute(
      text(
        "SELECT country, COUNT(*) AS frequency FROM mytable WHERE country IS NOT NULL AND sector='Security' GROUP BY country"
      ))
    sec_cou_freq_list = list(result20.all())
    sec_cou_freq = [{
      "country": country,
      "frequency": frequency
    } for country, frequency in sec_cou_freq_list]

    result21 = conn.execute(
      text(
        "SELECT country, COUNT(*) AS frequency FROM mytable WHERE country IS NOT NULL AND sector='Government' GROUP BY country"
      ))
    ene_cou_freq_list = list(result21.all())
    ene_cou_freq = [{
      "country": country,
      "frequency": frequency
    } for country, frequency in ene_cou_freq_list]

    result22 = conn.execute(
      text(
        "SELECT country, COUNT(*) AS frequency FROM mytable WHERE country IS NOT NULL AND sector='Retail' GROUP BY country"
      ))
    ret_cou_freq_list = list(result22.all())
    ret_cou_freq = [{
      "country": country,
      "frequency": frequency
    } for country, frequency in ret_cou_freq_list]

    result23 = conn.execute(text("SELECT country, sector, COUNT(*) AS frequency FROM mytable WHERE country IS NOT NULL AND sector IS NOT NULL GROUP BY country, sector"))
    tuple_list = list(result23.all())
    triple_data = [{
      "country": country,
      "sector": sector,
      "frequency": frequency
    } for country,sector, frequency in tuple_list]


    dict = {
      "int_sec": int_sec,
      "int_top": int_top,
      "int_pes": int_pes,
      "rel_sec": rel_sec,
      "rel_top": rel_top,
      "rel_pes": rel_pes,
      "con_freq": con_freq,
      "top_freq": top_freq,
      "org_yr_freq": org_yr_freq,
      "pol_yr_freq": pol_yr_freq,
      "env_yr_freq": env_yr_freq,
      "hlt_yr_freq": hlt_yr_freq,
      "lif_yr_freq": lif_yr_freq,
      "tech_yr_freq": tech_yr_freq,
      "eco_yr_freq": eco_yr_freq,
      "ind_yr_freq": ind_yr_freq,
      "soc_yr_freq": soc_yr_freq,
      "gov_cou_freq": gov_cou_freq,
      "tra_cou_freq": tra_cou_freq,
      "sec_cou_freq": sec_cou_freq,
      "ene_cou_freq": ene_cou_freq,
      "ret_cou_freq": ret_cou_freq,
      "triple_data": triple_data,
      
    }

    return dict
