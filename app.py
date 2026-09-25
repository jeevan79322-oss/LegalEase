"""LegalEase Streamlit frontend."""
import os
from pathlib import Path
import requests
import streamlit as st

API_URL = os.getenv("LEGALEASE_API_URL", "http://127.0.0.1:8000").rstrip("/")
LOGO_PATH = Path(__file__).resolve().parent / "assets" / "legalease_logo.png"
st.set_page_config(page_title="LegalEase | Document Studio", page_icon="⚖️", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Libre+Baskerville:wght@400;700&display=swap');
.stApp { background: #f5f7f8; color: #20313c; }
h1,h2,h3 { font-family: 'Libre Baskerville', Georgia, serif; color: #19364b; }
.hero { padding: 1.5rem 0 .5rem; }
.eyebrow { text-transform: uppercase; letter-spacing: .16em; color: #9b6f37; font-size: .76rem; font-weight: 700; }
.subtle { color: #61717d; }
div[data-testid="stForm"] { background: white; padding: 1.25rem 1.4rem; border: 1px solid #e1e7ea; border-radius: 14px; }
.draft-card { background: white; border: 1px solid #e1e7ea; border-radius: 14px; padding: 1.25rem 1.5rem; }
div.stButton > button[kind="primary"] { background: #19364b; border-color: #19364b; }
</style>
""", unsafe_allow_html=True)

st.image(str(LOGO_PATH), width=180)
st.markdown('<div class="hero"><div class="eyebrow">Document studio</div></div>', unsafe_allow_html=True)
st.title("A clearer first draft starts here.")
st.markdown('<p class="subtle">Create an editable starting point for your agreement. Review every detail before anyone signs.</p>', unsafe_allow_html=True)

left, right = st.columns([0.9, 1.1], gap="large")
with left:
    st.subheader("Tell us about the agreement")
    with st.form("document_details"):
        document_type = st.selectbox("Document type", ["Non-disclosure agreement", "Employment agreement", "Residential lease agreement", "Freelance services agreement", "Consulting agreement", "Custom document"])
        if document_type == "Custom document":
            document_type = st.text_input("Name your document", placeholder="e.g. Equipment loan agreement")
        parties = st.text_area("Parties and roles", placeholder="Example: Jordan Lee (Consultant) and Northstar Studio Ltd. (Client)", height=86)
        terms_text = st.text_area("Key terms", placeholder="One term per line or separated by semicolons\nExample: Fee is due within 30 days; Either party may end the agreement with 14 days' written notice", height=145)
        effective_date = st.text_input("Effective date", placeholder="e.g. 1 October 2026")
        jurisdiction = st.text_input("Jurisdiction", placeholder="e.g. Ontario, Canada", help="Local legal requirements vary. Add the relevant country and region if known.")
        language = st.selectbox("Draft language", ["English", "Spanish", "French", "Hindi", "Portuguese"])
        submitted = st.form_submit_button("Generate draft", type="primary", use_container_width=True)

    if submitted:
        terms = [item.strip() for item in terms_text.replace(";", "\n").splitlines() if item.strip()]
        if not document_type or len(parties.strip()) < 2 or not terms or not effective_date.strip():
            st.error("Add the document type, parties, at least one key term, and an effective date.")
        else:
            payload = {"document_type": document_type, "parties": parties.strip(), "terms": terms,
                       "effective_date": effective_date.strip(), "jurisdiction": jurisdiction.strip() or "Not specified", "language": language}
            try:
                with st.spinner("Preparing your draft…"):
                    response = requests.post(f"{API_URL}/generate", json=payload, timeout=90)
                if response.ok:
                    result = response.json()
                    st.session_state["draft"] = result["content"]
                    st.session_state["editable_draft"] = result["content"]
                    st.session_state["draft_type"] = document_type
                    st.session_state["ai_generated"] = result["ai_generated"]
                    st.session_state["draft_model"] = result["model"]
                else:
                    try:
                        detail = response.json().get("detail", "The server could not generate the draft.")
                    except ValueError:
                        detail = "The server could not generate the draft."
                    st.error(detail)
            except requests.RequestException:
                st.error("Could not reach the backend. Start the FastAPI server and try again.")

with right:
    st.subheader("Review and edit")
    draft = st.session_state.get("draft", "")
    if draft:
        if st.session_state.get("ai_generated"):
            st.success(f"AI draft · {st.session_state.get('draft_model', 'Gemini')}")
        else:
            st.info("Local template mode · Add a Gemini API key to enable AI drafting.")
        edited = st.text_area("Document text", value=draft, height=480, label_visibility="collapsed", key="editable_draft")
        st.session_state["draft"] = edited
        st.caption("Editing happens in this preview. Your draft stays in this browser session and is not saved by the app.")
        st.markdown("**Download your draft**")
        cols = st.columns(3)
        for col, fmt in zip(cols, ["txt", "docx", "pdf"]):
            with col:
                try:
                    response = requests.post(f"{API_URL}/export/{fmt}", json={"document_type": st.session_state.get("draft_type", "Agreement"), "content": edited}, timeout=30)
                    if response.ok:
                        st.download_button(f"Download .{fmt}", response.content, file_name=f"legalease-draft.{fmt}", mime=response.headers.get("content-type", "application/octet-stream"), key=f"download_{fmt}", use_container_width=True)
                    else:
                        st.caption(f".{fmt} export unavailable")
                except requests.RequestException:
                    st.caption(f".{fmt} export unavailable")
    else:
        st.markdown('<div class="draft-card"><p class="eyebrow">Your workspace</p><h3>Your draft will appear here</h3><p class="subtle">Complete the agreement details and select <b>Generate draft</b>. You can edit the text and download it as TXT, DOCX, or PDF.</p></div>', unsafe_allow_html=True)

st.divider()
st.caption("LegalEase creates draft text for convenience. It is not legal advice, does not verify legal compliance, and does not replace review by a qualified lawyer. Avoid entering highly sensitive personal information.")
