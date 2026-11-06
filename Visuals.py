# This creates the page for displaying data visualizations.
import os

import streamlit as st
import json
import pandas as pd
import plotly.express as px

st.title("Visuals")

with open("data.json", "r") as f:
    data = json.load(f)

df_json = pd.DataFrame(data)

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")



# PART 1: GRAPHS FROM data.json
import plotly.express as px

fig = px.bar(df_json, x="names", y="rating",
             title="Average Rating of Fast Food",
             labels={"names": "Fast Food", "avg_rating": "Rating"})
st.plotly_chart(fig)


if "min_rating" not in st.session_state:
    st.session_state.min_rating = 3.0

st.slider("Minimum rating", 0.0, 5.0, key="min_calories")

filtered = df_json[df_json["calories"] >= st.session_state.min_calories]
st.scatter_chart(filtered, x="avg_meal_cost", y="calories")



st.header("Survey Results")
df_csv = pd.read_csv("data.csv")
df_csv["visits_per_month"] = pd.to_numeric(df_csv["visits_per_month"], errors="coerce")

# PART 2: GRAPHS FROM data.csv


CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.csv")
MEAL_TIMES = ["Breakfast", "Lunch", "Dinner", "Late night"]


#  Load the CSV (safely, in case nobody has taken the survey yet) 
try:
    df = pd.read_csv(CSV_PATH)
except (FileNotFoundError, pd.errors.EmptyDataError):
    df = pd.DataFrame()

if df.empty:
    st.info("No survey responses yet. Go to the Survey page and add some!")
else:
    df["visits_per_month"] = pd.to_numeric(df["visits_per_month"], errors="coerce")

    # STATIC (advanced, Plotly bar chart): never changes with user input 
    st.subheader("Favorite Chains")
    counts = df["chain"].value_counts().reset_index()
    counts.columns = ["chain", "responses"]
    bar_fig = px.bar(
        counts,
        x="chain",
        y="responses",
        title="Favorite Fast Food Chains (Survey Responses)",
        labels={"chain": "Chain", "responses": "Number of Responses"},
    )
    st.plotly_chart(bar_fig)

    # DYNAMIC (pie chart): changes with the radio button 
    st.subheader("Chain Share by Meal Time")

    # Session state: set a starting value once, then the radio keeps it updated
    if "meal_choice" not in st.session_state:
        st.session_state.meal_choice = "Lunch"

    choice = st.radio("Show responses for:", MEAL_TIMES, key="meal_choice", horizontal=True)
    filtered = df[df["meal_time"] == choice]

    if filtered.empty:
        st.info(f"No responses for {choice} yet.")
    else:
        pie_fig = px.pie(
            filtered,
            names="chain",
            title=f"Favorite Chains for {choice} Eaters",
        )
        st.plotly_chart(pie_fig)

        # EXTRA CREDIT: mean and median that update as the radio changes 
        cur = (filtered["visits_per_month"].mean(), filtered["visits_per_month"].median())

        if "last_choice" not in st.session_state:
            st.session_state.last_choice = choice
            st.session_state.cur_stats = cur
            st.session_state.prev_stats = None
        elif st.session_state.last_choice != choice:
            # The radio changed: current stats become "previous", new stats become "current"
            st.session_state.prev_stats = st.session_state.cur_stats
            st.session_state.cur_stats = cur
            st.session_state.last_choice = choice

        mean_now, median_now = st.session_state.cur_stats
        prev = st.session_state.prev_stats
        mean_delta = None if prev is None else round(mean_now - prev[0], 2)
        median_delta = None if prev is None else round(median_now - prev[1], 2)

        col1, col2 = st.columns(2)
        col1.metric("Mean visits per month", round(mean_now, 2), delta=mean_delta)
        col2.metric("Median visits per month", round(median_now, 2), delta=median_delta)






