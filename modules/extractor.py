import pandas as pd
import pdfplumber

def extract_from_pdf(uploaded_file):
    text_content = []
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)

                tables = page.extract_tables()
                for table in tables:
                    if table and len(table) > 1:  # ensure it's not empty
                        df = pd.DataFrame(table[1:], columns=table[0])
                        text_content.append(df.to_string(index=False))

        return "\n".join(text_content) if text_content else "No readable content found in the PDF."
    except Exception as e:
        return f"Error extracting PDF: {e}"


def extract_from_excel(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        return df
    except Exception as e:
        return f"Error reading Excel: {str(e)}"
