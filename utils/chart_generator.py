import streamlit as st


def generate_chart(df):

    if df.empty:
        return

    # Only one value
    if len(df.columns) == 1:
        st.metric(df.columns[0], df.iloc[0, 0])
        return

    # Two columns
    if len(df.columns) == 2:

        x = df.columns[0]
        y = df.columns[1]

        # Line chart for dates
        if "date" in x.lower() or "month" in x.lower():
            st.line_chart(df.set_index(x))

        # Bar chart otherwise
        else:
            st.bar_chart(df.set_index(x))

        return

    # Three or more columns
    st.dataframe(df, use_container_width=True)