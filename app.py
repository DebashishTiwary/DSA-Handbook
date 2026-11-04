import streamlit as st
from google import genai
import pymongo
import re
import requests
from datetime import datetime,timedelta,timezone
import pandas as pd
import streamlit.components.v1 as components
import urllib.parse
import time
import pickle
import math
import random
# st.code("for i in range(8): foo()")
st.set_page_config(page_icon=":ledger:",page_title="DSA-Handbook",layout="wide")
custom_html = """
<style>
    /* Container styling */
    .dsa-header {
        position: relative;
        width: 100%;
        padding: 50px 20px 60px;
        background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
        margin-bottom: 40px;
        overflow: hidden;
    }

    /* Ambient background glow behind header */
    .dsa-header::before {
        content: '';
        position: absolute;
        top: -50px;
        left: 50%;
        transform: translateX(-50%);
        width: 300px;
        height: 150px;
        background: rgba(56, 189, 248, 0.15);
        filter: blur(80px);
        border-radius: 50%;
        pointer-events: none;
    }

    /* Animated Gradient Title */
    .dsa-title {
        font-size: 3.6rem !important;
        font-weight: 900 !important;
        letter-spacing: -1px;
        background: linear-gradient(270deg, #38bdf8, #818cf8, #c084fc, #38bdf8);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 40px !important;
        animation: gradient-shift 6s ease infinite;
    }

    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Cycle Flow Layout */
    .cycle-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 12px;
        max-width: 1100px;
        margin: 0 auto;
        flex-wrap: wrap;
        position: relative;
    }

    /* Step Cards */
    .cycle-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid #334155;
        padding: 20px 24px;
        border-radius: 16px;
        font-size: 1.1rem;
        font-weight: 600;
        color: #f1f5f9;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 180px;
    }

    /* Number Badge on Cards */
    .step-badge {
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 2px 10px;
        border-radius: 20px;
        margin-bottom: 8px;
    }

    /* Hover Animation */
    .cycle-card:hover {
        transform: translateY(-6px) scale(1.03);
        border-color: #38bdf8;
        box-shadow: 0 10px 30px rgba(56, 189, 248, 0.25);
        color: #ffffff;
    }

    /* Highlight specifically for Repeat step */
    .repeat-card:hover {
        border-color: #c084fc;
        box-shadow: 0 10px 30px rgba(192, 132, 252, 0.3);
    }
    
    .repeat-card .step-badge {
        color: #c084fc;
        background: rgba(192, 132, 252, 0.1);
        border-color: rgba(192, 132, 252, 0.3);
    }

    /* Animated Pulsing Arrows */
    .arrow {
        font-size: 1.5rem;
        color: #64748b;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulse-arrow 2s infinite ease-in-out;
    }

    @keyframes pulse-arrow {
        0%, 100% { transform: translateX(0); opacity: 0.6; }
        50% { transform: translateX(4px); opacity: 1; color: #38bdf8; }
    }

    .repeat-arrow {
        color: #c084fc;
    }

    /* Mobile Responsive view */
    @media (max-width: 850px) {
        .cycle-container {
            flex-direction: column;
            gap: 12px;
        }
        .arrow {
            transform: rotate(90deg);
            animation: pulse-down 2s infinite ease-in-out;
        }
        @keyframes pulse-down {
            0%, 100% { transform: rotate(90deg) translateX(0); opacity: 0.6; }
            50% { transform: rotate(90deg) translateX(4px); opacity: 1; color: #38bdf8; }
        }
        .dsa-title {
            font-size: 2.5rem !important;
        }
    }
</style>

<div class="dsa-header">
    <h1 class="dsa-title">My DSA-Handbook<br><p>Everything  is  an  Algorithm !</p></h1>
    
    
    <div class="cycle-container">
        <div class="cycle-card">
            <span class="step-badge">STEP 01</span>
            <span>Code</span>
        </div>
        
        <div class="arrow">&#10140;</div>
        
        <div class="cycle-card">
            <span class="step-badge">STEP 02</span>
            <span>Create Notes</span>
            
        </div>
        
        <div class="arrow">&#10140;</div>
        <div class="cycle-card">
                    <span class="step-badge">STEP 03</span>
                    <span>Revise</span>
                </div>
         <div class="arrow">&#10140;</div>
        <div class="cycle-card">
            <span class="step-badge">STEP 03</span>
            <span>Crack Interviews</span>
        </div>
        
        <div class="arrow repeat-arrow">&#10227;</div>
        
        <div class="cycle-card repeat-card">
            <span class="step-badge">Perfect Loop</span>
            <span>Repeat</span>
        </div>
    </div>
</div>
"""
st.html(custom_html)
# st.image('bcgImg.jpg')
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
        
        1.Give approach as if you are explaning to layman and it should be clear idea.(more focus)
        2. Very Brief explanation of the code
        3. Time and Space Complexity.
        4.All in higlish and understandable to layman
        5.No followup question

        Keep it clean, concise,and formatted using Markdown and be fast.
        """
    response = client.models.generate_content(model="gemini-3.8-flash",contents=prompt)
    return response.text
  except Exception as e:
    print(e)
    return f"Your friend is sick buddy!:( Please take AI-help in Edit Explanation."
#contests
def convert2IST(timestamp):
  seconds=timestamp/1000
  utc= datetime.fromtimestamp(seconds,timezone.utc)
  ist_timezone = timezone(timedelta(hours=5, minutes=30))
  ist_time = utc.astimezone(ist_timezone)
  return ist_time.strftime('%Y-%m-%d %I:%M %p')


if not st.user.is_logged_in:
  st.warning("Please log in/Sign Up to access your personal DSA handbook.")
  if st.button("Sign Up/Log in"):
    st.login()
else:
  st.sidebar.success(f"Logged in as: {st.user.name}")
  if st.sidebar.button("Log out"):
    st.logout()
# -------------------------------------------------------------------------

  tab1,tab2,tab3=st.tabs(["Upcomig Contests","My Solutions","Gymkhana"])
  with tab1:
   try:
    @st.cache_data(ttl=3600)
    def getprocesseddata():
      header={
         # without headers it can Sir katey ka aatank
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
      return filtered_df
    # learn about this column_config more
    filtered_df=getprocesseddata()
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
   except Exception as e:
      st.write("Please try in some time!")
      print(e)



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
        user_solutions=list(db.solutions.find({"author_email":st.user.email}))
        
        user_solutions_array=[]
        user_solutions_sorting=[]
        user_solutions_hashing=[]
        user_solutions_binarysearch=[]
        user_solutions_recursion=[]
        user_solutions_strings=[]
        user_solutions_linkedlist=[]
        user_solutions_bitman=[]
        user_solutions_greedy=[]
        user_solutions_slidingwind=[]
        user_solutions_stackQueue=[]
        user_solutions_bt=[]
        user_solutions_bst=[]
        user_solutions_heaps=[]
        user_solutions_graph=[]
        user_solutions_dp=[]
        user_solutions_others=[]

        for sol in user_solutions:
           val=sol['topic']
           if val=="Arrays":
              user_solutions_array.append(sol)
           elif val=="Sorting":
              user_solutions_sorting.append(sol)
           elif val=="Hashing":
              user_solutions_hashing.append(sol)
           elif val=="Binary Search":
              user_solutions_binarysearch.append(sol)
           elif val=="Strings":
              user_solutions_strings.append(sol)
           elif val=="Recursion":
              user_solutions_recursion.append(sol)
           elif val=="Linked List":
              user_solutions_linkedlist.append(sol)
           elif val=="Bit Manipulation":
              user_solutions_bitman.append(sol)
           elif val=="Greedy":
              user_solutions_greedy.append(sol)
           elif val=="Sliding Window":
              user_solutions_slidingwind.append(sol)
           elif val=="Stack/Queue":
              user_solutions_stackQueue.append(sol)
           elif val=="Binary Tree":
              user_solutions_bt.append(sol)
           elif val=="Binary Search Tree":
              user_solutions_bst.append(sol)
           elif val=="Heaps":
              user_solutions_heaps.append(sol)
           elif val=="Graph":
              user_solutions_graph.append(sol)
           elif val=="Dynamic Programming":
              user_solutions_dp.append(sol)
           else:
              user_solutions_others.append(sol)
        @st.fragment
        def createCard(sol):
            sol_id_str = str(sol["_id"])
            editing_key = f"editing_{sol_id_str}"
            text_key = f"text_input_{sol_id_str}"

            if editing_key not in st.session_state:
               st.session_state[editing_key] = False
            with st.container(border=True):
                                   col1,col2=st.columns([3,1])
                                   with col1:
                                      st.link_button(sol["problem_title"],sol["problem_url"])
                                   with col2:
                                     st.caption(f"Language: **{sol['language']}**")
                                   exp,code=st.tabs(["Explanaion","Code"])
                                   with exp:
                                      # Claude comes into play
                                    #   st.write(sol['explanation'])
                                      if not st.session_state[editing_key]:
                                       st.markdown(sol["explanation"])
                                       if st.button("Edit Explanation", key=f"edit_btn_{sol_id_str}"):
                                          st.session_state[editing_key] = True
                                      else:
                                          updated_explanation = st.text_area(
                                                            "Edit Explanation:",
                                                            value=sol["explanation"],
                                                            height=200,
                                                            key=text_key,
                                                               )
                                          col_save, col_cancel,col_ask = st.columns(3)
                                          with col_ask:
                                       
                                             
                                             encoded_prompt=f"""Analyze this {sol['language']} solution for the DSA problem {sol['problem_title']}:
                                                 
                                                 Code:
                                                 {sol['code']}
                                                 
                                                 Provide:
                                                 1.Give approach used in code as if you are explaning to layman and it should be clear idea.(more focus)
                                                 2. Very Brief explanation of the code
                                                 3. Time and Space Complexity of the code provided.
                                                 4.No dry run required
                                                 5.All in higlish and understandable to layman
                                                 6.No followup question
                                                 
                                                Keep it clean, concise,and formatted using Markdown and be fast
                                                 """
                                             safe_prompt = urllib.parse.quote(encoded_prompt)
                                             claude_url = f"https://claude.ai/new?q={safe_prompt}"
                                             st.link_button("AI Help!!",claude_url)
                                          with col_save:
                                             if st.button("Save Changes", key=f"save_{sol_id_str}"):
                                                db.solutions.update_one(
                                                      {"_id": sol["_id"]},
                                                      {"$set": {"explanation": updated_explanation}},
                                                      )
                                                st.session_state[editing_key] = False
                                                st.success("Explanation updated!")
                                                st.rerun()
                                          with col_cancel:
                                             if st.button("Cancel", key=f"cancel_{sol_id_str}"):
                                                st.session_state[editing_key] = False
                                         
                                   with code:
                                      st.code(sol["code"])
                                   if st.button("Delete Problem Card", key=str(sol["_id"])):
                                     db.solutions.delete_one({"_id": sol["_id"]})
                                     st.success("Card deleted!")
                                     st.rerun()
                                  
                                   
        with tab2b:
            
            sorting,array,hashing,binarysearch,strings,recursion,linkedlist,bitman,greedy,slidingwind,stackQueue,bt,bst,heaps,graph,dp=st.tabs(["Sorting","Arrays","Hashing","Binary Search","Strings","Recursion","Linked List","Bit Manipulation","Greedy","Sliding Window","Stack/Queue","Binary Tree","Binary Search Tree","Heaps","Graph","Dynamic Programming"])
            with array:
               for sol in user_solutions_array:
                  createCard(sol)
            with sorting:
               for sol in user_solutions_sorting:
                    createCard(sol)
            with hashing:
               for sol in user_solutions_hashing:
                  createCard(sol)
            with binarysearch:
               for sol in user_solutions_binarysearch:
                  createCard(sol)
            with strings:
               for sol in user_solutions_strings:
                  createCard(sol)
            with recursion:
               for sol in user_solutions_recursion:
                  createCard(sol)
            with linkedlist:
               for sol in user_solutions_linkedlist:
                  createCard(sol)
            with bitman:
               for sol in user_solutions_bitman:
                  createCard(sol)
            with greedy:
               for sol in user_solutions_greedy:
                  createCard(sol)
            with slidingwind:
               for sol in user_solutions_slidingwind:
                  createCard(sol)
            with stackQueue:
               for sol in user_solutions_stackQueue:
                  createCard(sol)
            with bt:
               for sol in user_solutions_bt:
                  createCard(sol)
            with bst:
               for sol in user_solutions_bst:
                  createCard(sol)
            with heaps:
               for sol in user_solutions_heaps:
                  createCard(sol)
            with graph:
               for sol in user_solutions_graph:
                  createCard(sol)
            with dp:
               for sol in user_solutions_dp:
                  createCard(sol)

  with tab3:
     @st.cache_resource
     def load_model_beg():
        with open("beginner_model.pkl","rb") as file:
           model=pickle.load(file)
        return model
     
     @st.cache_resource
     def load_model_inter():
        with open("Intermediate_model.pkl","rb") as file:
                   model=pickle.load(file)
        return model
     
        
     surprise,comp=st.tabs(["Let's Test","Company Wise"])
     with surprise:
        def challenge(df,linkfile,lev):
         df=df.sample(n=1)             
         row_level=df.index[0]
         link=linkfile.loc[row_level]
         if hasattr(link, "values"):
            link = link.values[0]
         time.sleep(2)        
         if lev=="Beginner":
            model=load_model_beg()
         elif lev=="Intermediate":
            model=load_model_inter()
         est_time=model.predict(df)
         st.write(f'Estimated Max Time: {math.ceil(est_time[0])} mins for you')
         st.link_button("Embrace the Surprise",str(link))
         st.balloons()
        
        
        level=st.selectbox("Select your level",("Saved Solutions","Beginner","Intermediate","Expert"))
        if level=="Saved Solutions":
           problem=random.randint(0,len(user_solutions)-1)          
           time.sleep(2)
           st.link_button("Embrace the Surprise",str(user_solutions[problem]['problem_url']))
           time.sleep(1)
         #   st.balloons()
        else:
         topic=st.selectbox("Select Topic",("Sorting","Array","Binary Search","Strings","Recursion","Linked List","Bit Manipulation","Greedy","Sliding Window","Stack","Queue","Tree","Binary Search Tree","Graph","Dynamic Programming","Other Patterns"))
         df_beg=pd.read_csv('beginner_striver.csv')
         df_beg_link=pd.read_csv('beg_link.csv')
         df_inter=pd.read_csv('Intermediate_striver.csv')
         df_inter_link=pd.read_csv('inter_link.csv')
         df=pd.DataFrame()
         df_link=pd.DataFrame()
         if level=="Beginner":
            df=df_beg
            df_link=df_beg_link
         elif level=="Intermediate":
            df=df_inter
            df_link=df_inter_link

         if topic=="Sorting":
            df=df[df['Sorting']==1]
           
              
         elif topic=="Array":
            df=df[df['Array']==1]
              
         elif topic=="Dynamic Programming":
            df=df[(df['Dynamic Programming']==1)|(df['Memoization']==1)|(df['Backtracking']==1)]
              
         elif topic=="Binary Search":
            df=df[df['Binary Search']==1]
              
         elif topic=="Stack":
            df=df[df['Monotonic Stack']==1]
              
         elif topic=="Queue":
            df=df[df['Heap (Priority Queue)']==1]
              
         elif topic=="Strings":
            df=df[(df['String']==1)|(df['String Matching']==1)]
           
         elif topic=="Graph":
            df=df[(df['Breadth-First Search']==1)|(df['Depth-First Search']==1)|(df['Graph']==1)|(df['Topological Sort']==1)]
           
         elif topic=="Recursion":
            df=df[df['Recursion']==1]  
           
         elif topic=="Tree":
            df=df[(df['Binary Tree']==1)|(df['Tree']==1)]
           
         elif topic=="Binary Search Tree":
           df=df[df['Binary Search Tree']==1]
           
         elif topic=="Linked List":
           df=df[df['Linked List']==1]
           
         elif topic=="Greedy":
           df=df[df['Greedy']==1]
           
         elif topic=="Sliding Window":
           df=df[df['Sliding Window']==1]
           
         elif topic=="Bit Manipulation":
           df=df[df['Bit Manipulation']==1]
           
         elif topic=="Other Patterns":
           df=df[(df['Two Pointers']==1)|(df['Prefix Sum']==1)|(df['Union']==1)]

         challenge(df,df_link,level)
         
           
     
              
              

     with comp:
        def data_table(file):
           data=pd.read_csv(file)
           st.dataframe(data,column_config={
                "Difficulty": st.column_config.TextColumn(
                    width="medium",
                ),
                "title": st.column_config.TextColumn(
                    "Title",
                    width="large",
                ),
                "Frequency": st.column_config.TextColumn(
                    "Frequency",
                      
                    width="medium",
                ),
                "Acceptance Rate": st.column_config.TextColumn(
                                    "Acceptance Rate",
                                      
                                    width="medium",
                                ),
                "Link": st.column_config.LinkColumn(
                    label="Link",
                    display_text="Conqure it",
                    width="medium",
                ),
                "Topics": st.column_config.TextColumn(
                                    "Topics",
                                      
                                    width="medium",
                                ),
            },
            hide_index=True,
            width="stretch",)
        company=st.selectbox("Select your destination",("Acko","Apple","Atlassian","Blinkit","Google"))
        
        val=f'{company}.csv'
        data_table(val)
with st.bottom:
   LINKEDIN_URL="https://www.linkedin.com/in/debashishtiwary/"
   Github="https://github.com/DebashishTiwary"
   _, center_col, _ = st.columns([1, 2, 1])
    
   with center_col:
        # 2. Combine the link and the text into a single centered HTML block
        st.markdown(
    f"""
    <div style="text-align: center; font-size: 14px; color: #808495;">
        <a href="{Github}" target="_blank" style="color: #FFFF00; text-decoration: none; font-weight: bold;">Github</a>
        &nbsp;·&nbsp;
        <a href="{LINKEDIN_URL}" target="_blank" style="color: #0077b5; text-decoration: none; font-weight: bold;">LinkedIn</a>
        &nbsp;·&nbsp;
        <span>Made with 🧡 from 
            <span style="font-weight: bold;">
                <span style="color: #FF9933;">IN</span><span style="color: #FFFFFF; text-decoration: line-through #000080; text-decoration-thickness: 2px;">D</span><span style="color: #138808;">IA</span>
            </span>
            · All rights reserved
        </span>
    </div>
    """, 
    unsafe_allow_html=True
)


     
               
                  

