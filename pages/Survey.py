# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os  # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# Lists for the survey questions (use the same chains you put in data.json for Part 1)
CHAINS = ["McDonald's", "Chick-fil-A", "Wendy's", "Taco Bell", "Burger King", "Chipotle", "Other"]
MEAL_TIMES = ["Breakfast", "Lunch", "Dinner", "Late night"]
HEADER = ["chain", "meal_time", "visits_per_month", "go_to_order"]

# PAGE TITLE AND USER DIRECTIONS
st.title("Fast Food Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create input widgets for the user to enter data.
    # The first argument is the label that appears above the input.
    chain_input = st.selectbox("What is your favorite fast food chain?", CHAINS)
    meal_time_input = st.radio("When do you usually eat fast food?", MEAL_TIMES)
    visits_input = st.text_input("About how many times per month do you eat fast food? (whole number)")
    order_input = st.text_input("What is your go-to order?")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # Make sure the answers are valid before saving anything
        if not visits_input.strip().isdigit():
            st.error("Please enter the number of visits as a whole number, like 4.")
        elif order_input.strip() == "":
            st.error("Please enter your go-to order.")
        else:
            # 1. Create a new row of data from the inputs.
            new_row = [chain_input, meal_time_input, visits_input.strip(), order_input.strip()]

            # If the file is new or empty, write the header row first.
            file_is_empty = (not os.path.exists("data.csv")) or os.path.getsize("data.csv") == 0

            # 2. Append this new row to the 'data.csv' file.
            # 'a' = append mode, so earlier responses are kept.
            # newline="" lets the csv module add the newline at the end of each row for us.
            with open("data.csv", "a", newline="") as file:
                writer = csv.writer(file)
                if file_is_empty:
                    writer.writerow(HEADER)
                writer.writerow(new_row)

            st.success("Your data has been submitted!")
            st.write(
                f"You entered: **Chain:** {chain_input}, **Meal time:** {meal_time_input}, "
                f"**Visits per month:** {visits_input.strip()}, **Go-to order:** {order_input.strip()}"
            )


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider()  # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv("data.csv")
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")




