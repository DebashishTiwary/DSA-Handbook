import streamlit as st
from google import genai
import pymongo
import re
import requests
from datetime import datetime,timedelta,timezone
# st.code("for i in range(8): foo()")
st.set_page_config(page_icon=":ledger:",page_title="DSA-Handbook",layout="wide")
# st.image("logo.JPG")
custom_html = """
<div style="
    display: flex; 
    align-items: center; 
    background-color: #f0f2f6; 
    padding: 20px; 
    border-radius: 10px; 
    width: 100%;
    border: 2px solid #ff5733;
">
   
    <div style="flex-grow: 1; text-align: center; margin-right: 60px;">
        <h2 style="margin: 0; padding: 0;">My DSA Handbook</h2>
       <p>Everything is an Algorithm</p>
    </div>
</div>
"""
st.html(custom_html)
# -------------------------------------------------------------------------
#contests
st.subheader("Upcoming Contests")
def convert2IST(timestamp):
  seconds=timestamp/1000
  utc= datetime.fromtimestamp(seconds,timezone.utc)
  ist_timezone = timezone(timedelta(hours=5, minutes=30))
  ist_time = utc.astimezone(ist_timezone)
  return ist_time.strftime('%Y-%m-%d %I:%M %p')


data=requests.get("https://competeapi.vercel.app/contests/upcoming/").json()
# st.dataframe(data)
for contest in data:
  contest['startTime']=convert2IST(contest['startTime'])
  contest['endTime']=convert2IST(contest['endTime'])
  contest['duration']=contest['duration']/(1000*60)
  # contest['url']=st.page_link(contest['url'], label="Home")
# st.dataframe(data)

header_cols = st.columns([1.5, 3, 2.5, 1.5])
header_cols[0].markdown("**Platform**")
header_cols[1].markdown("**Title**")
header_cols[2].markdown("**Date & Time**")
header_cols[3].markdown("**Participate**")
# header_cols[4].markdown("**End Time**")
# header_cols[5].markdown("**Action**")
st.divider()

for contest in data:
    row_cols = st.columns([1.5, 3, 2.5, 1.5])
    
    # Fill in the text data fields
    row_cols[0].write(contest['site'].upper())
    row_cols[1].write(contest['title'])
    row_cols[2].write(str(contest['startTime']))
    row_cols[3].link_button("Go to Contest", contest['url'], use_container_width=True)

tab1,tab2=st.tabs(["My Solutions","Gymkhana"])
with tab1:
   taba,tabb,tabc,tabd=st.tabs(["Arrays","Binary Search","Hashing","Sorting"])
with taba:
     st.title("Array Solutions")
     tabaa,tabab=st.tabs(["My Solutions","Add new Solution"])
with tabb:
   st.title("Binary Search")