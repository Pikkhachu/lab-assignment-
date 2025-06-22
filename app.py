import pandas as pd
import sys
import matplotlib.pyplot as plt
from jinja2 import Template


df = pd.read_csv("data.csv")
df.columns = df.columns.str.strip() 

# Check if the correct number of arguments is provided
if len(sys.argv) != 3:
    html = "<!DOCTYPE html><html><body><h2>WRONG INPUT</h2></body></html>"
    with open("output.html", "w") as f:
        f.write(html)
    sys.exit()

mode = sys.argv[1]
id_value = sys.argv[2]

# STUDENT MODE
if mode == '-s':
    student_data = df[df['Student id'] == int(id_value)]
    if student_data.empty:
        html = "<!DOCTYPE html><html><body><h2>WRONG INPUT</h2></body></html>"
    else:
        total_marks = student_data['Marks'].sum()
        table_rows = ""
        for _, row in student_data.iterrows():
            table_rows += f"<tr><td>{row['Student id']}</td><td>{row['Course id']}</td><td>{row['Marks']}</td></tr>"
        table_rows += f"<tr><td colspan='2'><strong>Total</strong></td><td><strong>{total_marks}</strong></td></tr>"
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Student Details</title></head>
        <body>
        <h2>Student Details</h2>
        <table border="1">
        <tr><th>Student ID</th><th>Course ID</th><th>Marks</th></tr>
        {table_rows}
        </table>
        </body>
        </html>
        """

# COURSE MODE
elif mode == '-c':
    course_data = df[df['Course id'] == int(id_value)]
    if course_data.empty:
        html = "<!DOCTYPE html><html><body><h2>WRONG INPUT</h2></body></html>"
    else:
        avg_marks = round(course_data['Marks'].mean(), 2)
        max_marks = course_data['Marks'].max()
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Course Details</title></head>
        <body>
        <h2>Course Details</h2>
        <table border="1">
        <tr><th>Average Marks</th><th>Maximum Marks</th></tr>
        <tr><td>{avg_marks}</td><td>{max_marks}</td></tr>
        <br><img src="histogram.png" alt="Marks Histogram">
        </body>
        </html>
        """
        # Histogram
        plt.figure(figsize=(6, 4))
        plt.hist(course_data['Marks'], bins=10, color='skyblue', edgecolor='black')
        plt.title(f"Marks Distribution for Course {id_value}")
        plt.xlabel("Marks")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig("histogram.png")

# INVALID MODE
else:
    html = "<!DOCTYPE html><html><body><h2>WRONG INPUT</h2></body></html>"

# Save output.html
with open("output.html", "w") as f:
    f.write(html)

