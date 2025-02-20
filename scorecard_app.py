import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fpdf import FPDF

# Define categories and weights
categories = {
    "Founder Traits": 0.30,
    "Execution Ability": 0.30,
    "Industry & Network Strength": 0.25,
    "Investor Fit": 0.15
}

# Define the scorecard criteria and explanations
criteria = {
    "Founder Traits": [
        ("Vision Clarity", "How well the founders articulate their vision, problem, and solution."),
        ("Leadership Presence", "Can the founder inspire confidence and drive execution?"),
        ("Passion & Industry Knowledge", "Does the founder have deep knowledge of the market?"),
        ("Soft Skills & Coachability", "Can the founder take feedback and adapt quickly?")
    ],
    "Execution Ability": [
        ("Hustle & Problem-Solving", "Has the team executed anything tangible? Can they overcome challenges?"),
        ("Team Completeness", "Does the team cover critical business & tech roles?"),
        ("Market Sentiment", "What do customers, industry peers, and experts say about the startup?"),
        ("Team Balance & Dynamics", "Do the co-founders work well together?")
    ],
    "Industry & Network Strength": [
        ("Industry Experience", "Does the team have relevant experience in this sector?"),
        ("Network & Ability to Attract Talent", "Can the founders bring in top advisors, employees, or investors?")
    ],
    "Investor Fit": [
        ("Investor Confidence", "Does the investor feel strongly about this team?")
    ]
}

# Predefined explanations for different score ranges
explanations = {
    "low": "Needs significant improvement. This area is a major concern.",
    "medium": "Average performance. Some strengths, but also some weaknesses.",
    "high": "Strong performance. This is a key strength of the team."
}

# Collect startup information
startup_name = input("Enter the Startup Name: ")

# Collect scores
scores = {}
detailed_assessment = {}
for category, items in criteria.items():
    scores[category] = []
    detailed_assessment[category] = []
    print(f"\n{category} (Weight: {categories[category]*100}%)")
    for criterion, description in items:
        while True:
            try:
                print(f"\n{criterion}: {description}")
                score = float(input("Enter a score (1-10): "))
                if 1 <= score <= 10:
                    scores[category].append(score)

                    # Generate explanation based on score range
                    if score <= 3:
                        explanation = explanations["low"]
                    elif score <= 6:
                        explanation = explanations["medium"]
                    else:
                        explanation = explanations["high"]

                    detailed_assessment[category].append((criterion, score, explanation))
                    break
                else:
                    print("Invalid score. Please enter a number between 1 and 10.")
            except ValueError:
                print("Invalid input. Please enter a number.")

# Calculate average scores per category
average_scores = {category: sum(scores[category]) / len(scores[category]) for category in scores}
weighted_scores = {category: average_scores[category] * categories[category] for category in categories}

# Calculate final weighted score (out of 100)
final_score = sum(weighted_scores.values())

# Generate recommendation based on final score
if final_score >= 90:
    recommendation = "Outstanding Team: Highly investable!"
elif final_score >= 75:
    recommendation = "Strong Team: Worth considering with minor improvements."
elif final_score >= 50:
    recommendation = "Needs Improvement: Promising but requires significant work."
else:
    recommendation = "High Risk: Major concerns. Needs substantial changes."

# Generate radar chart
def generate_radar_chart(scores, startup_name):
    labels = list(scores.keys())
    values = list(scores.values())

    max_score = 10
    normalized_values = [v / max_score * 10 for v in values]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    normalized_values += normalized_values[:1]  # Close the chart
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    ax.set_ylim(0, 10)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.fill(angles, normalized_values, color='blue', alpha=0.25)
    ax.plot(angles, normalized_values, color='blue', linewidth=2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, ha='center', rotation=20, va="top")

    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(["2", "4", "6", "8", "10"])

    plt.title(f"{startup_name} Scorecard", fontsize=14, pad=20)
    plt.savefig("radar_chart.png", bbox_inches="tight", dpi=300)
    plt.close()

generate_radar_chart(average_scores, startup_name)

# Generate Score Bars (Red → Green with an arrow)
def generate_score_bar(score, filename):
    fig, ax = plt.subplots(figsize=(4, 0.4))

    cmap = plt.get_cmap("RdYlGn")  # Red to Green Gradient
    color = cmap(score / 10)

    ax.barh(0, score, color=color, height=0.6)
    ax.set_xlim(0, 10)
    ax.set_xticks(range(1, 11))
    ax.set_yticks([])

    # Add Arrow
    ax.text(score, 0, "▲", fontsize=14, ha='center', va='center', color="black")

    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.close()

# Generate PDF Report
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

pdf.set_font("Arial", "B", 14)
pdf.cell(200, 10, f"Startup: {startup_name}", ln=True, align="C")

pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, "Score Breakdown & Explanations:", ln=True)

for category, assessments in detailed_assessment.items():
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, f"{category} (Weight: {categories[category]*100}%)", ln=True)

    pdf.set_font("Arial", "", 10)
    for criterion, score, explanation in assessments:
        pdf.cell(0, 7, f"{criterion}: {score}/10", ln=True)
        
        # Generate and insert the score bar
        bar_filename = f"{criterion}_bar.png"
        generate_score_bar(score, bar_filename)
        pdf.image(bar_filename, x=pdf.get_x(), w=60)

        pdf.multi_cell(0, 7, explanation)

pdf.image("radar_chart.png", x=40, w=120)

pdf.set_font("Arial", "B", 12)
pdf.cell(0, 10, f"Final Score: {final_score:.2f}/100", ln=True)

pdf.multi_cell(0, 10, recommendation)

pdf.output(f"{startup_name}_Scorecard.pdf")
print(f"PDF report generated: {startup_name}_Scorecard.pdf")
