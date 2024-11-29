import streamlit as st
from dotenv import load_dotenv

from chatgpt import llm_chat
from history import History
from replace import replace_text_in_docx

load_dotenv()


# Streamlit UI
st.title("CV Text Editor")

# Upload the DOCX file
# Step 3: Run the script to replace text and export to PDF
uploaded_file = st.file_uploader("Choose a DOCX file", type="docx")

if uploaded_file is not None:
    old_text = '<Biography Text to Replace>'  # Replace with the text you want to find
    application_text = '<Text of the Application>'  # Replace with the text you want to replace it with

    # Input fields for old and new text
    old_text = st.text_area("Text to Replace", old_text)
    application_text = st.text_area("Application Text", application_text)

    # Button to replace text and export the file
    if st.button("Replace Text and Download PDF"):
        if old_text and application_text:
            # Define output path
            output_path = "modified_cv.docx"

            history = History()
            history.system("Application: " + application_text)
            history.system("CV Text: " + old_text)
            history.user("Can you rewrite the CV text to be more appropriate to fit the application. Only return the new CV biography text:")
            new_text = llm_chat(history)
            # Replace the text in the document
            modified_file = replace_text_in_docx(uploaded_file, old_text, new_text, output_path)

            # Provide download link for the modified file
            with open(output_path, "rb") as f:
                st.download_button("Download Modified CV", f, file_name=output_path)
        else:
            st.warning("Please provide both old and new text for replacement.")
