import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io

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

    # Use safe font
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

        # Calculate center position for the name
        text_width, text_height = draw.textsize(name, font=font)
        image_width, image_height = cert.size
        name_position = ((image_width - text_width) / 2, image_height * 0.5)

        # Draw text
        draw.text(name_position, name, fill="black", font=font)

        # Preview on Streamlit
        st.image(cert, caption=f"Preview: {name}", use_column_width=True)
