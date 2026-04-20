def sustainability_score(row):
    score = 100

    if row["Certified"] == "No":
        score -= 30

    if row["Region"] == "Asia":
        score -= 20

    if row["BackupSupplier"] == "No":
        score -= 10

    return max(score,0)