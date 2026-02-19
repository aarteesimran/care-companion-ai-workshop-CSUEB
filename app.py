import re
import streamlit as st

# ----------------------------
# Page setup
# ----------------------------
st.set_page_config(page_title="Care Companion Demo", layout="wide")
st.title("Care Companion Demo")
st.caption("AI-assisted coding workshop demo. Non-diagnostic educational tool.")

# ----------------------------
# Input
# ----------------------------
default_note = """Dad seemed more tired than usual this morning and skipped breakfast.
Blood pressure at 11 AM was 92/58.
He felt dizzy when standing up and needed help walking to the bathroom.
Took his blood pressure medication but missed his afternoon vitamin D.
Drank very little water today and did not go for his usual evening walk.
Mood seemed quiet and withdrawn."""

note = st.text_area("Paste today's caregiver note", value=default_note, height=170)

context = st.text_input(
    "Optional context (age, conditions, meds list)",
    value="Older adult; diabetes; usually walks daily; takes metformin + vitamin D; on blood pressure medication."
)

# ----------------------------
# Helper Functions
# ----------------------------
def find_bp(text: str):
    match = re.search(r"\b(\d{2,3})\s*/\s*(\d{2,3})\b", text)
    if match:
        systolic = int(match.group(1))
        diastolic = int(match.group(2))
        return systolic, diastolic, match.group(0)
    return None

def contains_any(text: str, keywords):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in keywords)

# ----------------------------
# Risk Radar
# ----------------------------
def risk_radar(note_text):
    risks = []
    urgency = "Low"

    bp = find_bp(note_text)
    if bp:
        sys, dia, raw = bp
        if sys <= 90 or dia <= 60:
            risks.append(f"Low blood pressure detected: {raw}")
            urgency = "Moderate"

    if contains_any(note_text, ["dizzy", "dizziness", "lightheaded"]):
        risks.append("Dizziness mentioned — monitor fall risk.")
        urgency = "Moderate"

    if contains_any(note_text, ["chest pain", "short of breath", "fainted"]):
        risks.append("Potential urgent symptom mentioned.")
        urgency = "High"

    if contains_any(note_text, ["very little water", "dehydr"]):
        risks.append("Low hydration mentioned.")

    if not risks:
        risks.append("No clear risk signals detected.")

    return f"Urgency Level: {urgency}\n\n" + "\n".join(risks)

# ----------------------------
# Action Planner
# ----------------------------
def action_planner(note_text):
    actions = []
    monitors = []
    confirm = []

    if contains_any(note_text, ["dizzy"]):
        actions.append("Help stand slowly and reduce fall risk.")
        monitors.append("Track when dizziness occurs.")

    if find_bp(note_text):
        actions.append("Recheck blood pressure later if possible.")
        monitors.append("Log BP with timestamps.")

    if contains_any(note_text, ["missed"]):
        confirm.append("Confirm which medication was missed and when.")

    if contains_any(note_text, ["very little water", "skipped breakfast"]):
        actions.append("Encourage hydration and light food if appropriate.")
        monitors.append("Track food and fluid intake.")

    if not actions:
        actions.append("Continue monitoring and document symptoms clearly.")

    output = "Do Now:\n" + "\n".join(f"- {a}" for a in actions)
    output += "\n\nMonitor:\n" + "\n".join(f"- {m}" for m in monitors)
    output += "\n\nConfirm:\n" + "\n".join(f"- {c}" for c in confirm)

    return output

# ----------------------------
# Doctor Brief
# ----------------------------
def doctor_brief(note_text):
    bp = find_bp(note_text)
    summary = "Caregiver reports changes in condition based on note provided."

    if bp:
        summary += f" Reported BP: {bp[2]}."

    if contains_any(note_text, ["dizzy"]):
        summary += " Dizziness noted."

    if contains_any(note_text, ["missed"]):
        summary += " Missed medication dose reported."

    output = (
        "Summary:\n"
        + summary
        + "\n\nPertinent Positives:\n"
    )

    if bp:
        output += f"- BP reading: {bp[2]}\n"
    if contains_any(note_text, ["dizzy"]):
        output += "- Dizziness\n"

    output += "\nSuggested Questions for Clinician:\n"
    output += "- Could symptoms relate to hydration or medication timing?\n"
    output += "- What monitoring should continue at home?\n"

    return output

# ----------------------------
# Care Circle
# ----------------------------
def care_circle(note_text):
    message = ["Quick update:"]

    if contains_any(note_text, ["dizzy"]):
        message.append("- Dizziness when standing was observed.")

    bp = find_bp(note_text)
    if bp:
        message.append(f"- BP reading reported: {bp[2]}.")

    message.append("- Monitoring symptoms and encouraging hydration.")
    message.append("- Will update if anything changes.")

    return "\n".join(message)

# ----------------------------
# Wellbeing
# ----------------------------
def wellbeing_support(note_text):
    return (
        "Caregiver Support Suggestions:\n"
        "- Take a brief rest if possible.\n"
        "- Share a quick status update with someone.\n"
        "- Focus on one next task at a time.\n"
        "- Aim for safety and consistency over perfection.\n"
    )

# ----------------------------
# Tabs
# ----------------------------
tabs = st.tabs([
    "Risk Radar",
    "Action Planner",
    "Doctor Brief",
    "Care Circle",
    "Wellbeing",
])

with tabs[0]:
    if st.button("Analyze Risk"):
        st.text(risk_radar(note))

with tabs[1]:
    if st.button("Generate Action Plan"):
        st.text(action_planner(note))

with tabs[2]:
    if st.button("Generate Doctor Brief"):
        st.text(doctor_brief(note))

with tabs[3]:
    if st.button("Generate Care Circle Message"):
        st.text(care_circle(note))

with tabs[4]:
    if st.button("Generate Wellbeing Support"):
        st.text(wellbeing_support(note))

st.markdown("---")
st.caption("Educational demo. Non-diagnostic. Designed for AI-assisted coding workshop.")
