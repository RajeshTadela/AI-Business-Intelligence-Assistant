import streamlit as st
from ai.pipeline import ask_database
from utils.chart_generator import generate_chart
from managers.dashboard_manager import *
# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Session State ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

initialize_dashboard()

if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

if "current_result" not in st.session_state:
    st.session_state.current_result = None
# ---------------- Sidebar ---------------- #

with st.sidebar:

    st.title("🤖 SQL Analytics Assistant")

    st.markdown("---")

    st.subheader("Example Questions")

    st.markdown("""
- Show total revenue
- Show top 10 products
- Revenue by category
- Monthly revenue
- Top sales persons
""")

    st.markdown("---")

    if st.session_state.show_dashboard:

        if st.button("⬅ Back to Assistant"):
            st.session_state.show_dashboard = False
            st.rerun()

    else:

        count = report_count()

        if st.button(f"Dashboard ({count})"):

            st.session_state.show_dashboard = True

            st.rerun()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        st.session_state.dashboard = []

        st.rerun()

# ---------------- Dashboard ---------------- #

if st.session_state.show_dashboard:

    st.title("Saved Dashboard Reports")

    reports = get_reports()

    if len(reports) == 0:

        st.info("No reports saved yet. Ask a question and click '📌 Save Report'.")

    else:

        for i, item in enumerate(reports, start=1):

            st.subheader(f" {item['question']}")
            st.subheader("📄 Report")
            st.write(f"**Question:** {item['question']}")

            if item["data"] is not None:

                st.subheader("Result")

                st.dataframe(
                    item["data"],
                    use_container_width=True
                )

                # Show chart only when useful
                if len(item["data"].columns) == 2:

                    first_col = item["data"].columns[0].lower()

                    if (
                        "month" in first_col
                        or "date" in first_col
                        or "category" in first_col
                        or "region" in first_col
                    ):

                        st.subheader("Visualization")
                        generate_chart(item["data"])


                csv = item["data"].to_csv(index=False).encode("utf-8")

                col1, col2 = st.columns(2)

                with col1:

                    st.download_button(
                        "📥 Download CSV",
                        csv,
                        file_name=f"report_{i}.csv",
                        mime="text/csv",
                        key=f"download_{i}"
                    )

                with col2:

                    if st.button(
                        "🗑 Delete Report",
                        key=f"delete_{i}"
                    ):

                        delete_report(i - 1)

                        st.toast("✅ Report deleted")

                        st.rerun()

            
    st.stop()

# ---------------- Main Page ---------------- #

st.title("🤖 AI SQL Analytics Assistant")

st.caption(
    "Ask questions about your connected MySQL database using natural language."
)

# ---------------- Previous Chat ---------------- #

for i, msg in enumerate(st.session_state.messages):

    with st.chat_message(msg["role"]):

        if msg["role"] == "user":

            st.write(msg["content"])

        else:

            # SQL
            st.subheader("SQL Query")
            st.code(msg["sql"], language="sql")

            # Result
            if msg["data"] is not None:

                st.subheader("Result Data")

                st.dataframe(
                    msg["data"],
                    use_container_width=True
                )

                # Download CSV
                csv = msg["data"].to_csv(index=False).encode("utf-8")

                st.download_button(
                    "📥 Download CSV",
                    csv,
                    file_name=f"query_result_{i}.csv",
                    mime="text/csv",
                    key=f"download_{i}"
                )

                # Visualization
                if len(msg["data"].columns) == 2:

                    first = msg["data"].columns[0].lower()

                    if (
                        "month" in first
                        or "date" in first
                        or "category" in first
                        or "region" in first
                    ):

                        st.subheader("Visualization")

                        generate_chart(msg["data"])

            # Insights
            st.subheader("💡 Business Insights")
            st.markdown(msg["insights"])

            # Save Report
            if st.button(
                "📌 Save Report",
                key=f"save_{i}"
            ):

                save_report(
                    msg.get("question", ""),
                    msg["sql"],
                    msg["data"],
                    msg["insights"]
                )

                st.toast("✅ Report Saved")

# ---------------- Chat Input ---------------- #

question = st.chat_input("Ask anything...")

# ---------------- Ask New Question ---------------- #

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    with st.spinner("🤖 Thinking..."):

        result = ask_database(question)

    st.session_state.current_result = {
        "question": question,
        "sql": result["sql"],
        "data": result["data"],
        "insights": result["insights"]
    }

    st.session_state.messages.append(
        {
            "role": "assistant",
            "question": question,
            "sql": result["sql"],
            "data": result["data"],
            "insights": result["insights"]
        }
    )
    st.rerun()

