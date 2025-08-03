import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

st.title("🎓 Automated Certificate Generator")

# Upload certificate template
template_file = st.file_uploader("Upload Certificate Template (PNG)", type=["png"])

# Upload CSV file with columns: Name, Course, Date
csv_file = st.file_uploader("Upload CSV with Student Details", type=["csv"])

if template_file and csv_file:
    # Load template and data
    template = Image.open(template_file)
    data = pd.read_csv(csv_file)
    st.write("Preview of uploaded data:", data.head())

    # Use safe font for Streamlit Cloud
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
    except:
        font = ImageFont.load_default()

    st.write("Generating certificates...")

    for index, row in data.iterrows():
        name, course, date = row["Name"], row["Course"], row["Date"]

        # Copy template
        cert = template.copy()
        draw = ImageDraw.Draw(cert)

        image_width, image_height = cert.size

        # --- Name ---
        bbox_name = draw.textbbox((0,0), name, font=font)
        name_width = bbox_name[2] - bbox_name[0]
        name_position = ((image_width - name_width) / 2, image_height * 0.45)

        # --- Course ---
        bbox_course = draw.textbbox((0,0), course, font=font)
        course_width = bbox_course[2] - bbox_course[0]
        course_position = ((image_width - course_width) / 2, image_height * 0.55)

        # --- Date ---
        bbox_date = draw.textbbox((0,0), date, font=font)
        date_width = bbox_date[2] - bbox_date[0]
        date_position = ((image_width - date_width) / 2, image_height * 0.65)

        # Draw text
        draw.text(name_position, name, fill="black", font=font)
        draw.text(course_position, course, fill="black", font=font)
        draw.text(date_position, date, fill="black", font=font)

        # Show certificate preview in Streamlit
        st.image(cert, caption=f"Preview: {name}", use_column_width=True)
