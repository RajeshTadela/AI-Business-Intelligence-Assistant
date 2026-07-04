import streamlit as st


def initialize_dashboard():

    if "dashboard" not in st.session_state:
        st.session_state.dashboard = []


def save_report(question, sql, data, insights):

    # Prevent duplicate reports
    for report in st.session_state.dashboard:
        if report["question"] == question:
            return

    report = {
        "title": question,
        "question": question,
        "sql": sql,
        "data": data,
        "insights": insights
    }

    st.session_state.dashboard.append(report)
    
def get_reports():

    return st.session_state.dashboard


def delete_report(index):

    st.session_state.dashboard.pop(index)


def report_count():

    return len(st.session_state.dashboard)