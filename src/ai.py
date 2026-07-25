import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("AI_API_KEY"), base_url="https://api.groq.com/openai/v1")


def generate_brief(summary):
    prompt = f"""
You are a procurement analytics assistant.

Based on the data below, generate:

1. Key Risks (max 4 bullets)
2. Key Drivers (max 4 bullets)
3. Recommended Actions (max 4 bullets)

Be specific. Use supplier names and categories.

DATA:
Avg Risk: {summary['avg_risk']}
% High Risk: {summary['high_risk_pct']}%
Avg HHI: {summary['avg_hhi']}

High Risk Suppliers:
{summary['high_risk']}

High Concentration:
{summary['high_conc']}

Low Sustainability:
{summary['low_sust']}
"""

    resp = client.chat.completions.create(
        model=os.getenv("AI_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return resp.choices[0].message.content


def explain_supplier(row):
    prompt = f"""
Explain why this supplier is risky.

Supplier: {row['Supplier Name']}
Category: {row['Category']}
Risk Score: {row['Risk Score']}
On-Time Delivery: {row['On-Time Delivery %']}
Defect Rate: {row['Defect Rate %']}
Lead Time: {row['Lead Time (days)']}
Region: {row['Region']}
Backup Supplier: {row['Backup Supplier Available?']}

Give 3–4 bullet points.
"""

    resp = client.chat.completions.create(
        model=os.getenv("AI_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return resp.choices[0].message.content


def simulate_scenario(row, new_risk):
    prompt = f"""
A supplier scenario has changed.

Supplier: {row['Supplier Name']}
New Risk Score: {new_risk}
On-Time Delivery: {row['On-Time Delivery %']}
Backup Supplier: {row['Backup Supplier Available?']}

Explain:
1. Why the risk changed
2. What procurement should do

Keep it short.
"""

    resp = client.chat.completions.create(
        model=os.getenv("AI_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return resp.choices[0].message.content