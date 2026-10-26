import streamlit as st
from google import genai
import pymongo
import re
import requests
from datetime import datetime,timedelta,timezone
import pandas as pd
# st.code("for i in range(8): foo()")
st.set_page_config(page_icon=":ledger:",page_title="DSA-Handbook",layout="wide")
# st.image("logo.JPG")
custom_html = """
<div style="display: flex; align-items: center; padding: 10px; border-radius: 10px; width: 100%; border-bottom: 2px solid #ff5733;"> 
    <div style="flex-grow: 1; text-align: center; margin-right: 60px; border:1px #000080;backgroud-color:red"> 
        <h2 style="margin: 0; padding: 0; font-family: 'Times New Roman', Times, serif;">My DSA Handbook</h2> 
        <p style="margin: 5px 0 0 0;">Everything is an Algorithm</p> 
    </div> 
</div>
"""

# Render the HTML safely inside your Streamlit app
st.markdown(custom_html, unsafe_allow_html=True)
# -------------------------------------------------------------------------
#contests
def convert2IST(timestamp):
  seconds=timestamp/1000
  utc= datetime.fromtimestamp(seconds,timezone.utc)
  ist_timezone = timezone(timedelta(hours=5, minutes=30))
  ist_time = utc.astimezone(ist_timezone)
  return ist_time.strftime('%Y-%m-%d %I:%M %p')




tab1,tab2,tab3=st.tabs(["Upcomig Contests","My Solutions","Gymkhana"])
with tab1:
    data=requests.get("https://competeapi.vercel.app/contests/upcoming/").json()
    # st.dataframe(data)

    df = pd.DataFrame(data)


    df["site"] = df["site"].str.upper()

    df["startTime"] = df["startTime"].apply(convert2IST)
    df["endTime"] = df["endTime"].apply(convert2IST)
    df["duration"] = df["duration"] / (1000 * 60)
    

    filtered_df = df[["site", "title", "startTime", "url"]]
    # learn about this column_config more
    st.dataframe(
        filtered_df,
        column_config={
            "site": st.column_config.TextColumn(
                "Platform",
                help="Coding platform hosting the contest",
                width="medium",
            ),
            "title": st.column_config.TextColumn(
                "Contest Title",
                width="large",
            ),
            "startTime": st.column_config.DatetimeColumn(
                "Date & Time",
                format="D MMM YYYY, h:mm A",  
                width="medium",
            ),
            "url": st.column_config.LinkColumn(
                label="Go to Contest ",
                display_text="Register Here",
                width="medium",
            ),
        },
        hide_index=True,
        use_container_width=True,
    )



with tab2:
    tab2a,tab2b=st.tabs(["Add new Solution","Topics"])

    with tab2b:
        sorting,array,hashing,binarysearch,strings,recursion,linkedlist,bitman,greedy,slidingwind,stackQueue,bt,bst,heaps,graph,dp=st.tabs(["Sorting","Arrays","Hashing","Binary Search","Strings","Recursion","Linked List","Bit Manipulation","Greedy","Sliding Window","Stack/Queue","Binary Tree","Binary Search Tree","Heaps","Graph","Dynamic Programming"])

