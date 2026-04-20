def generate_recommendations(row, category_hhi_lookup):
    recommendations = []

    category_hhi = category_hhi_lookup.get(row["Category"], 0)

    if row["Risk Score"] >= 70 and category_hhi > 2500:
        recommendations.append("Prioritize category diversification")

    if row["Sustainability Score"] < 50 and row["Annual Spend"] > 50000:
        recommendations.append("Prioritize sustainability review for this supplier")

    if row["Lead Time (days)"] > 30 and str(row["Backup Supplier Available?"]).strip().lower() == "no":
        recommendations.append("Develop contingency sourcing plan")

    if row["Defect Rate %"] >= 3 and row["Annual Spend"] > 50000:
        recommendations.append("Initiate supplier performance review")

    if row["Supplier Share %"] > 35 and category_hhi > 2500:
        recommendations.append("Qualify secondary supplier within 90 days")

    if 1500 <= category_hhi <= 2500 and str(row["Backup Supplier Available?"]).strip().lower() == "no":
        recommendations.append("Develop contingency sourcing plan")

    if not recommendations:
        recommendations.append("No immediate action required")

    return " | ".join(recommendations)