import streamlit as st
import aspose.slides as slides
import tempfile
import os
import base64

def pptx_to_pdf(pptx_path):
    # Load presentation using Aspose.Slides
    with slides.Presentation(pptx_path) as presentation:
        # Save the presentation as PDF
        pdf_path = pptx_path.replace(".pptx", ".pdf")
        presentation.save(pdf_path, slides.export.SaveFormat.PDF)
    return pdf_path

def display_pdf(file_path):
    # Display PDF in the Streamlit app using an iframe
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.title("PPTX to PDF Converter and Previewer")

    pptx_file = st.file_uploader("Upload a PPTX file", type=["pptx"])

    if pptx_file is not None:
        st.write("Processing the uploaded file...")

        # Save the uploaded PPTX file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as tmp_file:
            tmp_file.write(pptx_file.read())
            pptx_path = tmp_file.name

        # Convert the PPTX to PDF
        pdf_path = pptx_to_pdf(pptx_path)

        # Display the PDF in Streamlit
        st.header("PDF Preview")
        display_pdf(pdf_path)

        # Provide a download button for the PDF
        with open(pdf_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
            st.download_button("Download PDF", data=pdf_data, file_name="converted.pdf")

if __name__ == "__main__":
    main()
