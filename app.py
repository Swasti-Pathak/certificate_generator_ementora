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

    from PIL import ImageFont

try:
    # Try default DejaVuSans (works on Streamlit Cloud)
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
except:
    # Fallback to a default PIL font if the file is missing
    font = ImageFont.load_default()


    pdf_buffer = io.BytesIO()  # For combined PDF
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch

    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.pagesizes import A4

    st.write("Generating certificates...")

    for index, row in data.iterrows():
        name, course, date = row["Name"], row["Course"], row["Date"]

        # Copy template
        cert = template.copy()
        draw = ImageDraw.Draw(cert)

        # Add text (adjust coordinates)
        draw.text((500, 300), name, fill="black", font=font)
        draw.text((500, 400), course, fill="black", font=font)
        draw.text((500, 500), date, fill="black", font=font)

        # Save each as PDF in memory
        img_buffer = io.BytesIO()
        cert.save(img_buffer, format='PDF')

        st.image(cert, caption=f"Preview: {name}", use_column_width=True)

    st.success("✅ Certificates generated! You can now download them individually.")
