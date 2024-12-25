import os
import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime, date

# Title of the Streamlit app
st.title("Invoice generator")

# Basic settings
root_dir = os.path.dirname(os.path.dirname(__file__))
projects_file_path = os.path.join(root_dir, "projects.xlsx")
timesheets_file_path = os.path.join(root_dir, "timesheets.xlsx")
name = "Denervaud Aloïs"

# Get list of projects
projects_df = pd.read_excel(projects_file_path, sheet_name="projects")

# Input fields
# Date selection
c1, c2 = st.columns([1,1])
date_start = c1.date_input("Start date", date.today())
date_end = c2.date_input("End date", date.today())
if date_start == date_end:
    st.warning("Start and end date are identical")

## 1 Generate an empty dataframe / excel file for the period
#if st.button("Create timesheet for the selected period"):
#    #hour_file_path = os.path.join(root_dir, str(date_start.year), "{}_{}_{}_timesheets.xlsx".format(datetime.strftime(date_start, "%Y%m%d"), datetime.strftime(date_end, "%Y%m%d"), name.replace(" ", "_")))
#    hour_file_path = os.path.join(root_dir, "spreadsheets", str(date_start.year)+".xlsx")
#    if not os.path.exists(os.path.dirname(hour_file_path)):
#        os.makedirs(os.path.dirname(hour_file_path))
#    
#    if not os.path.exists(hour_file_path):
#        hours_df = pd.DataFrame()
#        hours_df.to_excel(hour_file_path, index=False)
#        st.success("Timesheet created successfully!")
#    else:
#        st.error("Timesheet already exists for that period. Please remove the file and start again.")

## 1 Fetch timesheets
try:
    timesheets = pd.read_excel(timesheets_file_path, sheet_name=str(date_start.year))
except FileNotFoundError as fnfe:
    st.error(fnfe)
except Exception as e:
    st.warning(e)
    
## 2 Add project hours to the dataframe
project = st.selectbox("Select Project", projects_df["NameShort"])
hours = st.number_input("Number of Hours", min_value=0.0, max_value=200.0, step=0.5)
# Description - skip
comment = st.text_area("Comment (optional)")

# Button to submit the time entry
if st.button("Submit"):
    # Append new data to existing dataframe
    new_data = {"Project": project, "Year": date_start.year, "Month":date_start.month, "Hours": hours}# , "Description": description}
    df = pd.DataFrame([new_data])
    timesheets = pd.concat([timesheets, df])
    
    # Write DataFrame to a specific sheet in an Excel file
    with pd.ExcelWriter(timesheets_file_path, engine='openpyxl', mode='a', if_sheet_exists="replace") as writer:  
        timesheets.to_excel(writer, sheet_name=str(date_start.year), index=False)

    st.success("Entry submitted successfully!")


## 3 Generate PDF




# Generate PDF report
if st.button("Generate PDF Report"):
    # Read the data from the Excel file
    try:
        data = pd.read_excel("hours_tracker.xlsx")
    except FileNotFoundError:
        st.error("No data available to generate a report.")
        st.stop()

    # Filter data for the current user
    user_data = data[data["Name"] == name]
    
    if user_data.empty:
        st.error("No data available for the current user.")
        st.stop()
    
    # Group by project and sum the hours
    project_hours = user_data.groupby("Project")["Hours"].sum().reset_index()

    # Create a PDF
    pdf = FPDF()
    pdf.add_page()

    # Add title
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Project Hours Report", ln=True, align="C")

    # Add time period
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True, align="L")
    #pdf.cell(200, 10, txt=f"Time Period: {min(user_data['Date']).strftime('%Y-%m-%d')} to {max(user_data['Date']).strftime('%Y-%m-%d')}", ln=True, align="L")
    pdf.cell(200, 10, txt="Time period: {} - {}".format(datetime.strftime(date_start, "%d/%m/%Y"), datetime.strftime(date_end, "%d/%m/%Y")))

    # Add table header
    pdf.ln(10)
    pdf.cell(90, 10, txt="Project", border=1, align="C")
    pdf.cell(90, 10, txt="Total Hours", border=1, align="C")
    pdf.ln()

    # Add table rows
    for index, row in project_hours.iterrows():
        pdf.cell(90, 10, txt=row["Project"], border=1, align="C")
        pdf.cell(90, 10, txt=str(row["Hours"]), border=1, align="C")
        pdf.ln()

    # Signature line
    pdf.ln(20)
    pdf.cell(200, 10, txt="Signature: ____________________", ln=True, align="L")

    # Save the PDF
    pdf.output("hours_report.pdf")
    
    # Display success message
    st.success("PDF report generated successfully! Download it [here](hours_report.pdf).")
