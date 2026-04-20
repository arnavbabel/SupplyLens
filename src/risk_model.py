def score_delivery(on_time):
    if on_time >= 95:
        return 10
    elif on_time >= 90:
        return 35
    elif on_time >= 85:
        return 65
    else:
        return 90

def score_quality(defect_rate):
    if defect_rate < 1:
        return 10
    elif defect_rate < 3:
        return 35
    elif defect_rate < 5:
        return 65
    else:
        return 90

def score_lead_time(days):
    if days < 7:
        return 10
    elif days <= 14:
        return 35
    elif days <= 30:
        return 60
    else:
        return 85

def score_geography(region):
    region_map = {
        "Domestic": 15,
        "Local": 15,
        "Nearshore": 40,
        "Offshore Stable": 60,
        "Offshore Higher Risk": 80
    }
    return region_map.get(region, 50)

def score_backup(has_backup):
    return 20 if str(has_backup).strip().lower() == "yes" else 85

def calculate_risk(row):
    delivery_risk = score_delivery(row["On-Time Delivery %"])
    quality_risk = score_quality(row["Defect Rate %"])
    lead_time_risk = score_lead_time(row["Lead Time (days)"])
    geographic_risk = score_geography(row["Region"])
    backup_risk = score_backup(row["Backup Supplier Available?"])

    risk_score = (
        0.35 * delivery_risk +
        0.20 * quality_risk +
        0.15 * lead_time_risk +
        0.15 * geographic_risk +
        0.15 * backup_risk
    )

    return round(risk_score, 1)