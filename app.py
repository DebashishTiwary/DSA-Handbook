import streamlit as st
from google import genai
import pymongo
import re
import requests
from datetime import datetime,timedelta,timezone
import pandas as pd
import streamlit.components.v1 as components
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
st.markdown(custom_html, unsafe_allow_html=True)

@st.cache_resource
def init_connections():
  client_db = pymongo.MongoClient(st.secrets["mongo"]["uri"])
  # client_gem=genai.Client(api_key=st.secrets["gemini"]["api_key"])
  return client_db

client_mongo=init_connections()
db=client_mongo["dsa_platform"]

def extract_problem_title(url):
  match = re.search(r"/problems/([^/]+)", url)
  if match:
    slug = match.group(1)
    return slug.replace("-", " ").title()
  return "DSA Problem"

def generate_code_explanation(problem_title, code, language):
  try:
    client = genai.Client(api_key=st.secrets["gemini"]["api_key"])
    prompt = f"""
        Analyze this {language} solution for the DSA problem '{problem_title}':
        
        Code:
        {code}
        
        Provide:
        1. A brief summary of the approach (1-2 sentences).
        2. Step-by-step breakdown of how the logic works.
        3. Time and Space Complexity.
        Keep it clean, concise, and formatted using Markdown.
        """
    response = client.models.generate_content(model="gemini-3.8-flash",contents=prompt)
    return response.text
  except Exception as e:
    return f"Could not generate explanation automatically: {e}"
#contests
def convert2IST(timestamp):
  seconds=timestamp/1000
  utc= datetime.fromtimestamp(seconds,timezone.utc)
  ist_timezone = timezone(timedelta(hours=5, minutes=30))
  ist_time = utc.astimezone(ist_timezone)
  return ist_time.strftime('%Y-%m-%d %I:%M %p')


if not st.user.is_logged_in:
  st.warning("Please log in to access your personal DSA handbook.")
  if st.button("Log in"):
    st.login()
else:
  st.sidebar.success(f"Logged in as: {st.user.name}")
  if st.sidebar.button("Log out"):
    st.logout()
# -------------------------------------------------------------------------

  tab1,tab2,tab3=st.tabs(["Upcomig Contests","My Solutions","Gymkhana"])
  with tab1:
    header={
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
    data=requests.get("https://competeapi.vercel.app/contests/upcoming/",headers=header).json()
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
            width="stretch",
        )



  with tab2:
        tab2a,tab2b=st.tabs(["Add new Solution","Topics"])
        with tab2a:
            

            with st.form("link_solution_form", clear_on_submit=True):
                problem_url = st.text_input(
                "Problem Link (e.g., https://leetcode.com/problems/two-sum/)"
                )
                language = st.selectbox("Language", ["Python", "Java", "C++"])
                topic=st.selectbox("Topic",["Select One","Sorting","Arrays","Hashing","Binary Search","Strings","Recursion","Linked List","Bit Manipulation","Greedy","Sliding Window","Stack/Queue","Binary Tree","Binary Search Tree","Heaps","Graph","Dynamic Programming"])
                code_solution = st.text_area(
                "Paste your code here", height=200
            )

                submitted = st.form_submit_button("Generate Explanation & Save")

                if submitted:
                    if problem_url and code_solution:
                        with st.spinner(
                            "Your notes for the code is being prepared..."
                                ):
            
                            problem_title = extract_problem_title(problem_url)

            
                            explanation = generate_code_explanation(
                            problem_title, code_solution, language
                        )

            # Save document to MongoDB
                            solution_doc = {
                        "problem_title": problem_title,
                        "problem_url": problem_url,
                        "language": language,
                        "topic":topic,
                        "code": code_solution,
                        "explanation": explanation,
                        "author_email": st.user.email,
                            }
                            db.solutions.insert_one(solution_doc)
                            st.success("Successfully added to your personal handbook!")
                            st.rerun()
                    else:
                        st.error("Please provide both the problem link and your code.")
        with tab2b:
            user_solutions=list(db.solutions.find({"author_email":st.user.email}))
            sorting,array,hashing,binarysearch,strings,recursion,linkedlist,bitman,greedy,slidingwind,stackQueue,bt,bst,heaps,graph,dp=st.tabs(["Sorting","Arrays","Hashing","Binary Search","Strings","Recursion","Linked List","Bit Manipulation","Greedy","Sliding Window","Stack/Queue","Binary Tree","Binary Search Tree","Heaps","Graph","Dynamic Programming"])
            with array:
               for sol in user_solutions:
                  if sol['topic']=="Arrays":
                     with st.container(border=True):
                        col1,col2=st.columns([3,1])
                        with col1:
                           st.link_button(sol["problem_title"],sol["problem_url"])
                        with col2:
                          st.caption(f"Language: **{sol['language']}**")
                        exp,code=st.tabs(["Explanaion","Code"])
                        with exp:
                          #  st.link_button("Get my solution","https://gemini.google.com/?hl=en-IN")
                           st.write(sol["explanation"])
                        with code:
                           st.code(sol["code"])
                        if st.button("Delete Problem Card", key=str(sol["_id"])):
                          db.solutions.delete_one({"_id": sol["_id"]})
                          st.success("Card deleted!")
                          st.rerun()

