import streamlit as st
import requests
import re
from clickup_helper import ClickUpManager

# Page setup
st.set_page_config(
    page_title="High-Ticket AI OS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Theme Customization (Skyblue & White - Clean Enterprise)
st.markdown("""
<style>
    /* Global Light Theme Override */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
    }

    [data-testid="stHeader"] {
        background-color: #F8FAFC !important;
    }

    h1 {
        color: #0284C7 !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    h2, h3, h4 {
        color: #0369A1 !important;
        font-weight: 600 !important;
    }

    /* Invisible Text & Label Fixes */
    label, p, div {
        color: #1E293B !important;
    }

    .stTextInput label, .stTextArea label, .stSelectbox label, .stNumberInput label {
        color: #0284C7 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Input Controls Custom Styling */
    input, textarea, div[role="combobox"] {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    input:focus, textarea:focus {
        border-color: #0284C7 !important;
        box-shadow: 0 0 0 2px rgba(2, 132, 199, 0.2) !important;
    }

    /* Sidebar Clean Skyblue Styling */
    [data-testid="stSidebar"] {
        background-color: #E0F2FE !important;
        border-right: 1px solid #BAE6FD !important;
    }

    .portfolio-box {
        background-color: #FFFFFF;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #BAE6FD;
        box-shadow: 0 2px 8px rgba(2, 132, 199, 0.08);
    }

    /* Buttons Styling */
    .stButton>button {
        background: #0284C7 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }

    .stButton>button:hover {
        background: #0369A1 !important;
        cursor: pointer;
    }

    /* Download Button Specific Design */
    .stDownloadButton>button {
        background-color: #FFFFFF !important;
        color: #0284C7 !important;
        border: 1px solid #0284C7 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }
    .stDownloadButton>button:hover {
        background-color: #E0F2FE !important;
        color: #0369A1 !important;
    }

    /* Metrics Styling */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        padding: 16px !important;
        border-radius: 10px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02) !important;
    }

    div[data-testid="stMetricValue"] {
        color: #0284C7 !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# Credentials
CLICKUP_KEY = st.secrets["CLICKUP_API_KEY"]
CLICKUP_LIST = st.secrets["CLICKUP_LIST_ID"]
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]


# Clean Markdown Text Function
def clean_markdown(text):
    clean = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Convert bold tags
    clean = re.sub(r'#+\s*', '', clean)  # Remove header symbols
    clean = clean.replace('* ', '• ')
    return clean


# Premium HTML Document Generator (No Emojis, Clean Corporate Design)
def generate_html_proposal(client, tier, timeline, raw_proposal, roi):
    paragraphs = raw_proposal.strip().split('\n')
    formatted_body = ""

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        p_clean = clean_markdown(p)
        if p.startswith('1.') or p.startswith('2.') or p.startswith(
                '3.') or "Executive Summary" in p or "System Architecture" in p or "Milestone" in p:
            formatted_body += f"<h3 style='color: #0284C7; border-bottom: 2px solid #E0F2FE; padding-bottom: 6px; margin-top: 25px;'>{p_clean}</h3>"
        elif p.startswith('•'):
            formatted_body += f"<li style='margin-bottom: 8px;'>{p_clean[1:].strip()}</li>"
        else:
            formatted_body += f"<p style='line-height: 1.7; margin-bottom: 12px;'>{p_clean}</p>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Strategic Proposal - {client}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #F8FAFC;
                color: #1E293B;
                margin: 0;
                padding: 40px;
            }}
            .container {{
                max-width: 850px;
                margin: 0 auto;
                background: #FFFFFF;
                padding: 50px;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(2, 132, 199, 0.08);
                border-top: 8px solid #0284C7;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #E0F2FE;
                padding-bottom: 20px;
                margin-bottom: 25px;
            }}
            .brand {{
                font-size: 22px;
                font-weight: bold;
                letter-spacing: 0.5px;
                color: #0284C7;
            }}
            .meta-grid {{
                background-color: #E0F2FE;
                padding: 20px;
                border-radius: 10px;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 12px;
                margin-bottom: 30px;
                font-size: 14px;
            }}
            .meta-item strong {{
                color: #0369A1;
            }}
            .roi-banner {{
                display: flex;
                justify-content: space-around;
                background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
                color: white;
                padding: 18px;
                border-radius: 10px;
                margin-bottom: 30px;
                text-align: center;
            }}
            .roi-card h4 {{
                margin: 0;
                font-size: 20px;
                color: #FFFFFF !important;
            }}
            .roi-card p {{
                margin: 4px 0 0 0;
                font-size: 12px;
                color: #E0F2FE !important;
            }}
            .proposal-content {{
                font-size: 15px;
                color: #334155;
            }}
            .footer {{
                margin-top: 50px;
                text-align: center;
                font-size: 12px;
                color: #94A3B8;
                border-top: 1px solid #E2E8F0;
                padding-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="brand">SYSTEM PROPOSAL</div>
                <div style="color: #64748B; font-size: 14px;">Prepared for: <strong>{client}</strong></div>
            </div>

            <div class="meta-grid">
                <div class="meta-item"><strong>Positioning Tier:</strong> {tier}</div>
                <div class="meta-item"><strong>Target Timeline:</strong> {timeline}</div>
                <div class="meta-item"><strong>Est. Monthly Hours Saved:</strong> {roi['hours']:.1f} hrs</div>
                <div class="meta-item"><strong>Projected Annual Value:</strong> ${roi['annual']:,.0f}</div>
            </div>

            <div class="roi-banner">
                <div class="roi-card">
                    <h4>{roi['hours']:.1f} Hours/Mo</h4>
                    <p>Time Reclaimed</p>
                </div>
                <div class="roi-card">
                    <h4>${roi['savings']:,.0f}/Mo</h4>
                    <p>Cost Saved</p>
                </div>
                <div class="roi-card">
                    <h4>${roi['annual']:,.0f}</h4>
                    <p>1-Year System Value</p>
                </div>
            </div>

            <div class="proposal-content">
                {formatted_body}
            </div>

            <div class="footer">
                Confidential & Proprietary Statement • Strategic Scope Document
            </div>
        </div>
    </body>
    </html>
    """


# Dashboard Top Header
st.title("High-Ticket AI OS")
st.markdown(
    "<p style='color: #0369A1; margin-top: -15px;'>Enterprise Strategic Scoping & Client Management Console</p>",
    unsafe_allow_html=True)

# Sidebar UI
st.sidebar.header("Client Portfolio")
st.sidebar.markdown("""
<div class="portfolio-box">
<b style="color: #0284C7;">Active Retainers</b><br><br>
• <span style="color: #334155;"><b>E-Commerce Agent:</b> $12,000</span><br>
• <span style="color: #334155;"><b>Lead Automation:</b> $4,500/mo</span><br>
• <span style="color: #334155;"><b>Knowledge RAG:</b> $8,000</span>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Proposal & Scope Builder", "Active Client Portal"])

with tab1:
    st.markdown("### 1. Client & Scope Input")
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Client / Company Name", placeholder="Acme Corp")
        business_problem = st.text_area("Client Bottleneck / Operational Goal",
                                        placeholder="Manual lead processing takes 20 hrs/week...")

    with col2:
        target_budget = st.selectbox("Positioning Tier", ["$3,000 - Growth Package", "$7,500 - Scale Integration",
                                                          "$15,000 - Enterprise AI System"])
        timeline = st.text_input("Expected Delivery Timeline", "3-4 Weeks")

    st.markdown("### 2. ROI & Pricing Dynamics")
    r_col1, r_col2, r_col3 = st.columns(3)
    with r_col1:
        hours_wasted = st.number_input("Hours wasted per week", min_value=1, value=15)
    with r_col2:
        hourly_rate = st.number_input("Client avg hourly cost ($)", min_value=10, value=50)
    with r_col3:
        automation_efficiency = st.slider("Target Automation Efficiency (%)", 50, 95, 80)

    # Calculations
    monthly_hours_saved = (hours_wasted * 4) * (automation_efficiency / 100)
    monthly_money_saved = monthly_hours_saved * hourly_rate
    annual_roi = monthly_money_saved * 12

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate Executive Proposal", use_container_width=True):
        if client_name and business_problem:
            with st.spinner("Generating executive client proposal..."):
                # STRICT CLIENT-FACING PROMPT
                prompt = f"""
                You are an elite, high-ticket AI automation agency owner. 
                Write a STRICTLY client-facing, highly professional proposal for '{client_name}'.

                Context:
                - Client Bottleneck: {business_problem}
                - Investment Tier: {target_budget}
                - Timeline: {timeline}
                - Projected Monthly Savings: ${monthly_money_saved:,.2f}
                - Projected Time Saved: {monthly_hours_saved:.1f} hours/month

                MANDATORY FORMAT (Use exactly these headings, nothing else):
                1. Executive Summary & Value Proposition
                2. System Architecture & Technical Deliverables
                3. Milestone Breakdown (List exactly 4 steps: Milestone 1, Milestone 2, Milestone 3, Milestone 4)

                CRITICAL INSTRUCTIONS:
                - DO NOT include any internal reasoning, brainstorming, emojis, "Tone checks", or "Math checks".
                - DO NOT output your planning process or meta comments.
                - Write directly to the client using authoritative language (e.g., "We will implement...").
                - Output ONLY the final, polished proposal text ready for the client.
                """

                list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_KEY}"
                try:
                    list_res = requests.get(list_url)
                    models_data = list_res.json()

                    if "models" in models_data:
                        candidate_models = [
                            m["name"] for m in models_data["models"]
                            if "generateContent" in m.get("supportedGenerationMethods", [])
                               and "2.5" not in m["name"]
                        ]

                        priority_order = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-2.0-flash"]
                        sorted_models = [m for m in priority_order if m in candidate_models] + [m for m in
                                                                                                candidate_models if
                                                                                                m not in priority_order]

                        proposal_text = None
                        last_err = None

                        for model_name in sorted_models:
                            gen_url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={GEMINI_KEY}"
                            payload = {"contents": [{"parts": [{"text": prompt}]}]}
                            headers = {'Content-Type': 'application/json'}

                            gen_res = requests.post(gen_url, json=payload, headers=headers)
                            gen_data = gen_res.json()

                            if gen_res.status_code == 200 and 'candidates' in gen_data:
                                proposal_text = gen_data['candidates'][0]['content']['parts'][0]['text']
                                break
                            else:
                                last_err = gen_data.get('error', {}).get('message', gen_res.text)

                        if proposal_text:
                            st.session_state["latest_proposal"] = proposal_text
                            st.session_state["roi_data"] = {
                                "hours": monthly_hours_saved,
                                "savings": monthly_money_saved,
                                "annual": annual_roi
                            }

                            subtasks = []
                            for line in proposal_text.split('\n'):
                                if "Milestone" in line:
                                    subtasks.append(line.replace('#', '').replace('*', '').strip())
                            if not subtasks:
                                subtasks = [
                                    "Milestone 1: Workflow Audit & Architecture Setup",
                                    "Milestone 2: Core Automation Engine Development",
                                    "Milestone 3: System Integration & Testing",
                                    "Milestone 4: Handover, Training & Go-Live"
                                ]
                            st.session_state["subtasks"] = subtasks

                            st.success("Executive Proposal Successfully Generated!")
                        else:
                            st.error(f"Generation Error: {last_err}")
                except Exception as err:
                    st.error(f"Connection Error: {err}")
        else:
            st.warning("Please fill out the client name and problem description.")

    # Proposal Render Section
    if "latest_proposal" in st.session_state:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### Value Realization Highlights")
        m1, m2, m3 = st.columns(3)
        m1.metric("Est. Monthly Hours Saved", f"{st.session_state['roi_data']['hours']:.1f} hrs")
        m2.metric("Est. Monthly Savings", f"${st.session_state['roi_data']['savings']:,.0f}")
        m3.metric("Projected 1-Yr Value", f"${st.session_state['roi_data']['annual']:,.0f}")

        st.markdown("<br>", unsafe_allow_html=True)
        cleaned_display_text = clean_markdown(st.session_state["latest_proposal"])

        st.markdown(f"""
        <div style="background-color: #FFFFFF; padding: 25px; border-radius: 10px; border-left: 6px solid #0284C7; border: 1px solid #E2E8F0; line-height: 1.7;">
            {cleaned_display_text.replace('\n', '<br>')}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        action_col1, action_col2 = st.columns(2)

        with action_col1:
            html_doc = generate_html_proposal(
                client_name,
                target_budget,
                timeline,
                st.session_state["latest_proposal"],
                st.session_state["roi_data"]
            )
            st.download_button(
                label="Download Executive Proposal (.html)",
                data=html_doc,
                file_name=f"Proposal_{client_name.replace(' ', '_')}.html",
                mime="text/html",
                use_container_width=True
            )

        with action_col2:
            if st.button("Push Scope & Milestones to ClickUp", use_container_width=True):
                try:
                    cu = ClickUpManager(CLICKUP_KEY, CLICKUP_LIST)
                    res = cu.create_lead_task(
                        client_name,
                        st.session_state["latest_proposal"],
                        target_budget,
                        subtasks=st.session_state.get("subtasks", [])
                    )
                    st.success(f"ClickUp Task Created! ID: {res.get('id')}")
                except Exception as ex:
                    st.error(f"ClickUp Integration Error: {ex}")

with tab2:
    st.markdown("### Live Client Onboarding Tracker")
    st.info("Syncs directly with ClickUp backend.")
    st.metric("Active High-Ticket Retainers", "3", "+1 this month")
    st.metric("Total System Value Generated", "$29,500", "+$7,500")