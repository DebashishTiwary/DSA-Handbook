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
  client_gem=genai.Client(api_key=st.secrets["gemini"]["api_key"])
  return client_db,client_gem

client_mongo,client_gemini=init_connections()
db=client_mongo["dsa_platform"]

def extract_problem_title(url):
  match = re.search(r"/problems/([^/]+)", url)
  if match:
    slug = match.group(1)
    return slug.replace("-", " ").title()
  return "DSA Problem"

def generate_code_explanation(problem_title, code, language):
  try:
    model = genai.GenerativeModel("gemini-3.8-flash")
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
    response = client_gemini.generate_content(model="gemini-3.8-flash",contents=prompt)
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
            width="stretch",
        )



#   with tab2:
#         tab2a,tab2b=st.tabs(["Add new Solution","Topics"])
#         with tab2a:
#             # st.subheader("Add New Solution via Link")

#             with st.form("link_solution_form", clear_on_submit=True):
#                 problem_url = st.text_input(
#                 "Problem Link (e.g., https://leetcode.com/problems/two-sum/)"
#                 )
#                 language = st.selectbox("Language", ["Python", "Java", "C++"])
#                 topic=st.selectbox("Topic",["Select One","Sorting","Arrays","Hashing","Binary Search","Strings","Recursion","Linked List","Bit Manipulation","Greedy","Sliding Window","Stack/Queue","Binary Tree","Binary Search Tree","Heaps","Graph","Dynamic Programming"])
#                 code_solution = st.text_area(
#                 "Paste your code here", height=200
#             )

#                 submitted = st.form_submit_button("Generate Explanation & Save")

#                 if submitted:
#                     if problem_url and code_solution:
#                         with st.spinner(
#                             "Your notes for the code is being prepared..."
#                                 ):
            
#                             problem_title = extract_problem_title(problem_url)

            
#                             explanation = generate_code_explanation(
#                             problem_title, code_solution, language
#                         )

#             # 3. Save document to MongoDB
#                             solution_doc = {
#                         "problem_title": problem_title,
#                         "problem_url": problem_url,
#                         "language": language,
#                         "topic":topic,
#                         "code": code_solution,
#                         "explanation": explanation,
#                         "author_email": st.user.email,
#                             }
#                             db.solutions.insert_one(solution_doc)
#                             st.success("Successfully added to your personal handbook!")
#                             st.rerun()
#                     else:
#                         st.error("Please provide both the problem link and your code.")
#         with tab2b:
#             sorting,array,hashing,binarysearch,strings,recursion,linkedlist,bitman,greedy,slidingwind,stackQueue,bt,bst,heaps,graph,dp=st.tabs(["Sorting","Arrays","Hashing","Binary Search","Strings","Recursion","Linked List","Bit Manipulation","Greedy","Sliding Window","Stack/Queue","Binary Tree","Binary Search Tree","Heaps","Graph","Dynamic Programming"])

#   with tab3:
#     st.title("🎡 Interactive Wheel Spinner")

#     items_input = st.text_input("Enter items (comma-separated):", "Apples, Bananas, Cherries, Donuts, Eclairs")
#     items = [item.strip() for item in items_input.split(",") if item.strip()]

#     if len(items) < 2:
#         st.warning("Please enter at least 2 items to spin the wheel.")
#     else:
   
#         wheel_html = f"""
#     <div style="display: flex; flex-direction: column; align-items: center; font-family: sans-serif;">
#         <canvas id="wheel" width="400" height="400" style="border-radius: 50%; box-shadow: 0 4px 10px rgba(0,0,0,0.3);"></canvas>
#         <button id="spinBtn" style="margin-top: 20px; padding: 10px 25px; font-size: 16px; font-weight: bold; background-color: #FF4B4B; color: white; border: none; border-radius: 5px; cursor: pointer;">SPIN!</button>
#         <h2 id="winner" style="margin-top: 15px; color: #333;"></h2>
#     </div>

#     <script>
#         const sectors = {repr(items)};
#         const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];
        
#         const rand = (m, M) => Math.random() * (M - m) + m;
#         const tot = sectors.length;
#         const elSpin = document.querySelector("#spinBtn");
#         const ctx = document.getElementById("wheel").getContext("2d");
#         const dia = ctx.canvas.width;
#         const rad = dia / 2;
#         const PI = Math.PI;
#         const TAU = 2 * PI;
#         const arc = TAU / tot;
        
#         let friction = 0.991; 
#         let angVel = 0;       
#         let ang = 0;          

#         const getIndex = () => Math.floor(tot - (ang / TAU) * tot) % tot;

#         function drawSector(sector, i) {{
#             let ang1 = arc * i;
#             ctx.save();
#             ctx.beginPath();
#             ctx.moveTo(rad, rad);
#             ctx.arc(rad, rad, rad, ang1, ang1 + arc);
#             ctx.lineTo(rad, rad);
#             ctx.fillStyle = colors[i % colors.length];
#             ctx.fill();
            
#             // Text placement
#             ctx.translate(rad, rad);
#             ctx.rotate(ang1 + arc / 2);
#             ctx.textAlign = "right";
#             ctx.fillStyle = "#fff";
#             ctx.font = "bold 16px sans-serif";
#             ctx.fillText(sector, rad - 10, 10);
#             ctx.restore();
#         }}

#         function rotate() {{
#             const sector = sectors[getIndex()];
#             ctx.canvas.style.transform = `rotate(${{ang - PI / 2}}rad)`;
#             if (!angVel && elSpin.textContent === "SPINNING...") {{
#                 elSpin.textContent = "SPIN!";
#                 document.getElementById("winner").innerText = "🎉 Winner: " + sector;
#             }}
#         }}

#         function frame() {{
#             if (!angVel) return;
#             angVel *= friction; 
#             if (angVel < 0.002) angVel = 0; 
#             ang += angVel; 
#             ang %= TAU; 
#             rotate();
#         }}

#         function engine() {{
#             frame();
#             requestAnimationFrame(engine);
#         }}

#         // Init
#         sectors.forEach(drawSector);
#         rotate();
#         engine();

#         elSpin.addEventListener("click", () => {{
#             if (angVel) return;
#             document.getElementById("winner").innerText = "";
#             angVel = rand(0.25, 0.45);
#             elSpin.textContent = "SPINNING...";
#         }});
#     </script>
#     """
    
#     components.html(wheel_html, height=500)
     
