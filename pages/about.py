import streamlit as st

# Hero Header
st.title("My DSA Handbook")
st.caption("A personalized platform designed to simplify and streamline your Data Structures and Algorithms journey.")

st.markdown("---")

# Core Philosophy
st.markdown("""
Mastering DSA isn't about grinding hundreds of random questions—it requires **consistent, targeted practice** and **effective revision**. That is where **DSA Handbook** steps in.
""")

# Problem vs Solution Columns
col1, col2 = st.columns(2)

with col1:
    st.error("### The Problem We Solve")
    st.write("""
    When solving complex DSA problems, developers invest hours of deep thinking and effort. Yet, most skip taking notes. 
    
    Months later, when revising for interviews or exams, they start from scratch—struggling to recall the exact logic, edge cases, and approaches they had already mastered.
    """)

with col2:
    st.success("### Our Solution")
    st.write("""
    DSA Handbook automates the revision process through structured problem tracking and personalized record-keeping. 
    
    Simply provide basic details, and comprehensive notes for your solved problem are created in no time—ensuring every insight and approach is saved automatically.
    """)

st.info(" **When it's time to revise**, don't waste time re-solving problems. Review your personalized handbook and jump straight to the core logic you used in your code!")

st.markdown("---")

# Features Section
st.header(" Other Exciting Features")

# Feature 1: Contests
st.subheader("Upcoming Contests")
st.write("Stay ahead of schedule with real-time listings of upcoming coding contests on **LeetCode**, **Codeforces**, and **CodeChef**.")

# Feature 2: Gymkhana
st.subheader(" Gymkhana Practice Arena")
st.write("An interactive arena designed to test your problem-solving speed and reinforce key concepts.")

st.markdown("#### **1. Level Selection**")
st.markdown("""
* **Solved Solutions:** Automatically picks a random problem from your saved library so you can re-solve and solidify your past logic.
* **Beginner:** Generates foundational problems focused on core data structures and basic algorithmic patterns for a chosen topic.
* **Intermediate:** Delivers moderate-complexity challenges testing optimization and multi-step logic.
* **Expert:** Presents high-difficulty, interview-level challenges tailored to your topic.
""")

st.markdown("#### **2. Key Capabilities**")
st.markdown("""
* **Predictive Time Estimator:** Predicts the estimated time required to solve a problem, helping you benchmark speed against interview settings.
* **Targeted Skill Building:** Focus your energy on specific weak areas with tailored problem sets.
""")

st.markdown("---")

# Why Choose Section
st.header("Why Choose DSA Handbook?")
st.write("""
Whether you are preparing for technical interviews, studying for computer science coursework, or sharpening your competitive programming skills, **DSA Handbook** provides an organized, intelligent workspace built to maximize your learning efficiency.
""")