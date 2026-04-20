def calculate_risk(row):
    delivery_risk = 100 - row["OnTime"]
    concentration_risk = min(row["Spend"]/1000,100)

    geo_risk = {
        "US":20,
        "Europe":30,
        "Asia":60
    }.get(row["Region"],40)

    backup_risk = 80 if row["BackupSupplier"]=="No" else 20

    risk_score = (
        0.4*delivery_risk +
        0.3*concentration_risk +
        0.2*geo_risk +
        0.1*backup_risk
    )

    return round(risk_score,2)