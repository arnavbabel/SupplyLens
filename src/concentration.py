def calculate_hhi(df):
    shares = df["Spend"] / df["Spend"].sum()

    hhi = (shares ** 2).sum()

    return round(hhi,4)