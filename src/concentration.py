import pandas as pd

def add_supplier_share(df):
    df = df.copy()
    category_totals = df.groupby("Category")["Annual Spend"].transform("sum")
    df["Supplier Share %"] = (df["Annual Spend"] / category_totals) * 100
    return df

def label_supplier_share(share):
    if share < 20:
        return "Low"
    elif share <= 35:
        return "Medium"
    else:
        return "High"

def calculate_category_hhi(df):
    hhi_rows = []

    for category, group in df.groupby("Category"):
        shares = (group["Annual Spend"] / group["Annual Spend"].sum()) * 100
        hhi = (shares ** 2).sum()

        if hhi < 1500:
            level = "Low"
        elif hhi <= 2500:
            level = "Moderate"
        else:
            level = "High"

        hhi_rows.append({
            "Category": category,
            "HHI": round(hhi, 1),
            "HHI Level": level
        })

    return pd.DataFrame(hhi_rows)