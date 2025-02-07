import matplotlib
matplotlib.use('Agg')  # Ensure non-GUI mode for Matplotlib

from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import folium
import os

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():

    schools = pd.read_csv("./data/sample.csv").fillna("").sort_values(by = "nat_score", ascending = False)
    unique_regions = list(schools["Region"].str.strip().unique())

    print(unique_regions)

    # Region Filter Logic
    selected_region = request.form.get("region", "All")
    print("selected_region: ", selected_region)
    if selected_region != "All":
        schools = schools[schools["Region"] == selected_region]


    # KPIs
    avg_teacher_ratio = round(schools["student_teacher_ratio"].mean(), 1)
    num_elec = schools["noelec"].sum()    
    avg_nat_score = round(schools["nat_score"].mean(), 1)
    avg_cct = round(schools["cct_percentage"].mean(), 1)


    # Bar Chart: Variance in Student-Teacher Ratio
    plt.figure(figsize=(6, 4))
    schools.plot(kind="bar", x="school_name", y="student_teacher_ratio", color="skyblue")
    plt.xlabel("School")
    plt.ylabel("Students per Teacher")
    plt.title("Student-Teacher Ratio per School")
    plt.tight_layout()
    plt.savefig("static/teacher_ratio.png")
    plt.close()


    # Pie Chart: Male vs Female Students
    total_male = schools["total_male"].sum()  # Sum all male students
    total_female = schools["total_female"].sum()  # Sum all female students
    plt.figure(figsize=(4, 4))
    plt.pie(
        [total_male, total_female], 
        labels=["Male Students", "Female Students"], 
        autopct='%1.1f%%', 
        colors=["blue", "pink"]
    )
    plt.savefig("static/gender_pie.png")
    plt.close()


    # Map of Schools
    school_map = folium.Map(location=[12.8797, 121.7740], zoom_start=6)
    for _, row in schools.iterrows():
        folium.CircleMarker(
            location=[row["Lat"], row["Lon"]],
            popup=f"{row['school_name']}<br>NAT Score: {row['nat_score']}%",
            # icon=folium.Icon(color="blue" if row["original_internet_boolean"] else "red")
            radius=4,  # Circle size
            color="green",  # Border color
            fill=True,
            fill_color="green",
            fill_opacity=0.7,
        ).add_to(school_map)
    school_map.save("static/school_map.html")


    # Scatter Plot: Student-Teacher Ratio vs. NAT Score
    plt.figure(figsize=(6, 4))
    plt.scatter(schools["student_teacher_ratio"], schools["student_teacher_ratio"], color="blue", alpha=0.6)
    plt.xlabel("Student-Teacher Ratio")
    plt.ylabel("NAT Score")
    plt.title("Student-Teacher Ratio vs. NAT Score")
    plt.grid(True)
    plt.savefig("static/scatter_plot.png")
    plt.close()


    return render_template("index.html",
                        avg_teacher_ratio=avg_teacher_ratio,
                        num_elec=num_elec,
                        avg_nat_score=avg_nat_score,
                        avg_cct=avg_cct,
                        schools=schools.to_dict(orient="records"),
                        regions=unique_regions,
                        selected_region=selected_region)  # Convert DataFrame to list of dictionaries



@app.route("/scatter-data")
def scatter_data():
    # Read data
    schools = pd.read_csv("./data/sample.csv").fillna("").sort_values(by="nat_score")

    # Get selected region from query parameters (passed from JavaScript)
    selected_region = request.args.get("region", "All")

    print("Selected Region:", selected_region)  # Debugging

    # Apply region filter if it's not "All"
    if selected_region != "All":
        schools = schools[schools["Region"].str.strip() == selected_region]

    # Convert data to JSON for JavaScript
    return jsonify(schools.to_dict(orient="records"))


if __name__ == '__main__':
    app.run(debug=True)
