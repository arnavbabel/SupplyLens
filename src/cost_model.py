def add_cost_score(df):

    df = df.copy()

    def score_category(group):
        min_spend = group["Annual Spend"].min()
        max_spend = group["Annual Spend"].max()

        if min_spend == max_spend:
            group["Cost Score"] = 100
        else:
            group["Cost Score"] = 100 - (
                (group["Annual Spend"] - min_spend) / (max_spend - min_spend)
            ) * 100

        return group

    df = df.groupby("Category", group_keys=False).apply(score_category)

    df["Cost Score"] = df["Cost Score"].round(1)

    return df