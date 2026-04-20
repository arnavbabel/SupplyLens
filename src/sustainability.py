def score_certification(certified):
    return 100 if str(certified).strip().lower() == "yes" else 0

def score_ethical_material(indicator):
    return 100 if str(indicator).strip().lower() == "yes" else 0

def score_region_proxy(region):
    region_scores = {
        "Domestic": 100,
        "Local": 100,
        "Nearshore": 70,
        "Offshore Stable": 40,
        "Offshore Higher Risk": 20
    }
    return region_scores.get(region, 50)

def calculate_sustainability(row):
    certification = score_certification(row["Sustainability Certification?"])
    ethical = score_ethical_material(row["Recycled / Ethical Material Indicator?"])
    region_proxy = score_region_proxy(row["Region"])

    sustainability_score = (
        0.35 * certification +
        0.35 * ethical +
        0.20 * region_proxy +
        0.10 * 50
    )

    return round(sustainability_score, 1)