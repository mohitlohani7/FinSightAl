import pandas as pd

def load_csv(file):
    """
    Load CSV from either a file path or a Streamlit UploadedFile object.
    """
    if hasattr(file, "read"):  # Streamlit UploadedFile
        return pd.read_csv(file)
    else:  # Normal file path
        return pd.read_csv(file)

def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # normalize column names
    df.columns = [c.strip() for c in df.columns]

    # Rename common variants to standard column names
    rename_map = {}
    for c in df.columns:
        if c.lower() == "amount" and c != "Amount":
            rename_map[c] = "Amount"
        elif c.lower() == "merchant" and c != "Merchant":
            rename_map[c] = "Merchant"
        elif c.lower() == "date" and c != "Date":
            rename_map[c] = "Date"
    df.rename(columns=rename_map, inplace=True)

    # parse dates if 'Date' column exists
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # ensure Amount numeric
    if "Amount" in df.columns:
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # fill missing columns with default empty string
    for c in ["Description", "Merchant", "Type"]:
        if c not in df.columns:
            df[c] = ""

    return df
