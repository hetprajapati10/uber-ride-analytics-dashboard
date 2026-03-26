import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

st.set_page_config("Uber Analytics", layout="wide")

df = pd.read_csv("Uber data set ncr.xlsx - ncr_ride_bookings.csv")

#_______________________________________________________________________________________________________________________
#                                           CSS
#_______________________________________________________________________________________________________________________
def apply_css():
    st.markdown("""
    <style>

    /* ===============================
       PROFESSIONAL ANALYTICS THEME
       =============================== */

    :root {
      --bg: #0f1117;
      --card: #161a23;
      --border: #2a2f3a;
      --text: #e6e9ef;
      --muted: #9aa4b2;
      --primary: #4f8cff;
      --accent: #22c55e;
    }

    /* ---------- GLOBAL ---------- */
    html, body, [class*="css"] {
      background-color: var(--bg) !important;
      color: var(--text) !important;
      font-family: 'Inter', sans-serif !important;
    }

    .stApp {
      background-color: var(--bg) !important;
    }

    /* ---------- HEADINGS ---------- */
    h1, h2, h3 {
      color: var(--text) !important;
      font-weight: 600 !important;
    }

    h2 {
      color: var(--primary) !important;
    }

    /* ---------- SIDEBAR ---------- */
    [data-testid="stSidebar"] {
      background: #11141c !important;
      border-right: 1px solid var(--border);
    }

    /* ---------- METRIC CARDS ---------- */
    [data-testid="stMetric"] {
      background: var(--card) !important;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 14px;
      transition: 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
      border-color: var(--primary);
      box-shadow: 0 0 10px rgba(79,140,255,0.2);
      transform: translateY(-3px);
    }

    /* ---------- DATAFRAME ---------- */
    [data-testid="stDataFrame"] {
      border-radius: 10px;
      border: 1px solid var(--border);
      overflow: hidden;
    }

    /* TEXT FIX */
    [data-testid="stDataFrame"] * {
      color: var(--text) !important;
    }

    /* HEADER */
    [data-testid="stDataFrame"] thead th {
      background: #1c2130 !important;
      color: var(--primary) !important;
      font-weight: 600;
    }

    /* ROW */
    [data-testid="stDataFrame"] tbody tr {
      background: var(--card) !important;
      transition: 0.2s;
    }

    /* HOVER */
    [data-testid="stDataFrame"] tbody tr:hover {
      background: rgba(79,140,255,0.08) !important;
    }

    /* ---------- INPUTS ---------- */
    .stTextInput input,
    .stSelectbox div,
    .stMultiSelect div {
      background: var(--card) !important;
      border: 1px solid var(--border) !important;
      color: var(--text) !important;
      border-radius: 6px;
    }

    .stTextInput input:focus,
    .stSelectbox div:focus-within {
      border-color: var(--primary) !important;
      box-shadow: 0 0 0 2px rgba(79,140,255,0.2);
    }

    /* ---------- BUTTON ---------- */
    .stButton button,
    [data-testid="stDownloadButton"] button {
      background: var(--primary) !important;
      color: white !important;
      border: none;
      border-radius: 6px;
      transition: 0.2s;
    }

    .stButton button:hover {
      background: #3b6fd8 !important;
    }

    /* ---------- SLIDER ---------- */
    [data-testid="stSlider"] > div > div > div > div {
      background: var(--primary) !important;
    }

    /* ---------- PLOTLY ---------- */
    .js-plotly-plot {
      background: var(--card) !important;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px;
    }

    /* ---------- EXPANDER ---------- */
    [data-testid="stExpander"] {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 10px;
    }

    /* ---------- SCROLLBAR ---------- */
    ::-webkit-scrollbar {
      width: 6px;
    }

    ::-webkit-scrollbar-thumb {
      background: var(--border);
      border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
      background: var(--primary);
    }

    </style>
    """, unsafe_allow_html=True)

apply_css()


with st.sidebar:
    selected = option_menu("Main Menu",
                           ["Dataset","Overview","Ride Analytics"],
                           icons=["table","bar-chart","graph-up"],
                           menu_icon="car-front",
                           default_index=0)

if selected == "Dataset":
    st.title("Data Explorer")
    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows",df.shape[0])
    col2.metric("Total Columns",df.shape[1])
    col3.metric("Mising Value", df.isna().sum().sum())

    st.divider()

    #column selection
    st.subheader("Select Column")
    selected_column = st.multiselect("Select Column to Display",
                                     df.columns, default=df.columns)
    filtered_df = df[selected_column]

    #search
    st.subheader("Search in Dataset")
    search_value = st.text_input("Enter Value to Search")
    if search_value:
        filtered_df = filtered_df[filtered_df.astype(str).apply(
            lambda row:row.str.contains(search_value,case=False).any(), axis=1
        )]
    # st.dataframe(filtered_df)
    st.subheader("Select Row Range")

    row_range = st.slider(
        "Choose row range",
        0,
        len(filtered_df),
        (0, min(100, len(filtered_df)))
    )
    filtered_df = filtered_df.iloc[row_range[0]:row_range[1]]
    # st.dataframe(filtered_df)

    col1, col2 = st.columns(2)

    with col1:
        selected_col = st.selectbox(
            "Select Column",
            filtered_df.columns
        )

    with col2:
        unique_values = ["All"] + list(filtered_df[selected_col].dropna().unique())

        selected_value = st.selectbox(
            "Select Value",
            unique_values
        )

    if selected_value != "All":
        filtered_df = filtered_df[filtered_df[selected_col] == selected_value]


    # if len(filtered_df) > 0:
    #     row_range = st.slider(
    #         "Choose row range",
    #         0,
    #         len(filtered_df),
    #         (0, min(100, len(filtered_df)))
    #     )
    #
    #     filtered_df = filtered_df.iloc[row_range[0]:row_range[1]]

    st.dataframe(filtered_df, use_container_width=True)

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

#OVERVIEW
if selected == "Overview":
    st.header("Ride Overview")
    completion_rate = (df["Booking Status"].value_counts().get('Completed', 0) / len(df)) * 100
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rides", len(df))
    col2.metric("Revenue", df["Booking Value"].sum())
    total_revenue = df["Booking Value"].sum()
    col3.metric("Completion Rate", f"{completion_rate:.1f}%")
    col4.metric("Avg Ride Value", f"₹{df['Booking Value'].mean():.0f}")

    st.divider()

        # business unit perfomance
    st.header("Business Unit Performance Metrix")
    bu_matrix = df.groupby("Vehicle Type").agg(
        Total_Booking=("Booking ID", "count"),
        Revenue_Generated=("Booking Value", "sum"),
        Avg_Distance=("Ride Distance", "mean"),
        Avg_Rating=("Driver Ratings", "mean")
        )

    bu_matrix["Revenue Share%"] = (
        bu_matrix["Revenue_Generated"] / total_revenue * 100 if (total_revenue) > 0 else 0)

    st.dataframe(bu_matrix.style.format({
        "Revenue_Generated": "${:,.2f}",
        "Avg_Distance": "{:,.2f}km",
        "Avg_Rating": "{:,.1f}",
        "Revenue Share%": "${:,.1f}"
    }).background_gradient(subset=["Revenue_Generated"], cmap="YlOrRd"))

    # OPERATION EFEICIENCY

    col_eff, col_can = st.columns(2)
    with col_eff:
        st.header("Operational Efficiency")
        eff_df = df.groupby("Vehicle Type")[["Avg VTAT", "Avg CTAT"]].mean()
        st.write("Average Turn Around Time {%in Minutes%}")
        st.dataframe(eff_df.style.highlight_max(axis=0, color="#2bfb6b").highlight_min(axis=0, color="#fb352b"),
                     use_container_width=True)

    total_rides = len(df)
    with col_can:
        st.header("Cancellation Audit")
        status_count = df["Booking Status"].value_counts().to_frame(name="Count")
        status_count["Share %"] = (status_count["Count"] / total_rides * 100)
        st.write("Breakdown of Ride Cancellation and Completion Statu")
        st.dataframe(status_count, use_container_width=True)
        st.divider()

    completed_rides = df.groupby("Payment Method")["Booking ID"]
    st.dataframe(completed_rides)

    #Top Insights
    st.subheader("Top Insights")

    top_vehicle = df.groupby("Vehicle Type")["Booking Value"].sum().idxmax()
    top_payment = df["Payment Method"].mode()[0]

    col1, col2 = st.columns(2)

    col1.success(f"Highest Revenue Vehicle: {top_vehicle}")
    col2.info(f"Most Used Payment Method: {top_payment}")

    # FINANCIAL ANALYSIS
    st.header("Financial Deep Dive")
    pay_col, reason_col = st.columns([4, 6])
    with pay_col:
        st.markdown(" ** Payment Method Distribution")
    pay_summary = (df["Payment Method"].value_counts(normalize=True) * 100)
    st.dataframe(pay_summary)

    st.header("Completed Rides by Payment Method")
    completed_rides = df.groupby("Payment Method")["Booking ID"].count()
    completed_rides.columns = ["Payment Method", "Total Rides"]
    st.dataframe(completed_rides, use_container_width=True)

    #Data Quality
    with st.expander("Data Quality & Audit Logs"):
        audit1, audit2 = st.columns(2)
        audit1.write(f"**Duplicate Records:{df.duplicated().sum()}")
        audit2.write(f"Missing Value:{df["Booking Status"].isna().sum()}")
        st.info("Missing Booking Value are expected for cancellation and no driver acceptance")
        st.success("Executive Overview are generated from operational dataset")


    st.title("Uber Operations")
    st.markdown("---")

    #strategic kpi
    completed_rides=df[df["Booking Status"]=="Completed"]
    total_revenue=completed_rides["Booking Value"].sum()
    avg_distance=completed_rides["Ride Distance"].mean()
    success_rate=(len(completed_rides)/total_revenue*100 if (total_revenue) > 0 else 0)
    avg_rating=completed_rides["Customer Rating"].dropna().mean()

    kpi1,kpi2,kpi3,kpi4 = st.columns(4)
    kpi1.metric(f"Gross Total Revenue",f"{total_revenue:,.0f}","target: %1.2M")
    kpi2.metric("Average Distance",f"{avg_distance:,.1f}KM")
    kpi3.metric("Fullfillment Rate",f"{success_rate:,.2f}%","-2.4% v/s Last Month","red")
    kpi4.metric("Average Customer Rating",f"{avg_rating:,.1f}")

    st.subheader("Select Columns to Display")
    selected_columns = st.multiselect("Choose columns",df.columns,default=df.columns[:2])
    if selected_columns:
        st.dataframe(df[selected_columns], use_container_width=True)
    else:
        st.warning("Please select at least one column")

    option = st.selectbox("Int Value", ["Int", "Float"])
    if option == "int":
        int_data = df.select_dtypes(int)
        st.write(int_data)
    elif option == "Float":
        int_data = df.select_dtypes(float)
        st.write(int_data)

if selected == "Ride Analytics":
    st.title("Advance Ride Intelligence Dashboard")

    completed = df[df["Booking Status"]=="Completed"]
    #sunburst chart
    st.subheader("Revenue Hierarchy")
    fig1 = px.sunburst(completed,path=["Vehicle Type","Payment Method"],
                       values="Booking Value",
                       color="Booking Value",
                       color_continuous_scale="Turbo")
    fig1.update_layout(height=500)
    st.plotly_chart(fig1, use_container_width=True)

    #treemap
    st.subheader("Revenue Distribution")
    fig2 = px.treemap(completed,path=["Vehicle Type","Payment Method"],
                      values="Booking Value",
                      color="Booking Value",
                      color_continuous_scale=["#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"])
    fig2.update_layout(margin = dict(t=20, b=0, l=0, r=0),height=420)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Customer Rating spread")
    fig3 = px.box(completed,x="Vehicle Type",y="Customer Rating", color="Vehicle Type")
    fig3.update_layout(height=500)
    st.plotly_chart(fig3, use_container_width=True)

    #sankey chart
    st.subheader("Ride Flow Analysis")
    flow = df.groupby(["Vehicle Type", "Booking Status"]).size().reset_index(name="Count")
    st.dataframe(flow, use_container_width=True)
    source_label = flow["Vehicle Type"].unique().tolist()
    target_label = flow["Booking Status"].unique().tolist()

    labels = source_label + target_label

    source = flow["Vehicle Type"].apply(
        lambda x: labels.index(x)
    )
    target = flow["Booking Status"].apply(
        lambda x: labels.index(x)
    )
    value = flow["Count"]

    fig4 = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="blue",width=0.5),label=labels
        ),
        link=dict(source=source, target=target, value=value)
    )])
    st.plotly_chart(fig4, use_container_width=True)

    #bar
    st.subheader("Ride Demand by Vehicle Type")
    demand = df.groupby("Vehicle Type").size().reset_index(name="Total Bookings")
    demand.columns = ["Vehicle Type","Total Bookings"]

    fig5 = px.bar(demand,x="Vehicle Type",y="Total Bookings",color="Vehicle Type")
    st.plotly_chart(fig5, use_container_width=True)

    #Horizontal Bar
    st.subheader("Revenue by Vehicle Type")

    rev = df.groupby("Vehicle Type").agg(total_revenue = ("Booking Value", "sum")).reset_index()

    fig6 = px.bar(rev, x="total_revenue",y="Vehicle Type",color="Vehicle Type")
    st.plotly_chart(fig6, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
    #pie
        st.subheader("Booking Status Distribution")

        status = df.groupby("Booking Status").size().reset_index(name="Count")
        fig7 = px.pie(status,names="Booking Status",values="Count",hole=0.45)
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
    #pie2
        st.subheader("Payment Method Usage")

        payment = df.groupby("Payment Method").size().reset_index(name="Count")
        fig8 = px.pie(payment,names="Payment Method",values="Count")
        st.plotly_chart(fig8, use_container_width=True)

    #scatter
    st.subheader("Ride Distance vs Booking Value")

    fig9 = px.scatter(df,
                      x="Ride Distance",
                      y="Booking Value",
                      color="Vehicle Type")
    st.plotly_chart(fig9, use_container_width=True)

    #histogram
    st.subheader("Customer Rating Distribution")

    fig10 = px.histogram(df,x="Customer Rating",nbins=15,color="Customer Rating")
    st.plotly_chart(fig10, use_container_width=True)

    #bar2
    st.subheader("Cancellation Reasons Analysis")

    cancel = df[df["Booking Status"] != "Completed"]
    cancel["Cancellation Reason"] = cancel["Reason for cancelling by Customer"].fillna(
        cancel["Driver Cancellation Reason"]
    )
    cancel_ride = cancel.groupby("Cancellation Reason").size().reset_index(name="Count")
    fig11 = px.bar(cancel_ride,x="Count",y="Cancellation Reason",orientation="h",color="Cancellation Reason")
    st.plotly_chart(fig11, use_container_width=True)
    #bar3
    st.subheader(" Average Distance by Vehicle Type")
    avg_distance = df.groupby("Vehicle Type")["Ride Distance"].mean().reset_index()

    fig12 = px.bar(avg_distance,
                 x="Vehicle Type",
                 y="Ride Distance",
                 color="Vehicle Type",
                 title="Average Distance by Vehicle Type")

    st.plotly_chart(fig12, use_container_width=True)

    #histo
    st.subheader("Booking Value Distribution")
    fig13 = px.histogram(df,
                       x="Booking Value",
                       nbins=35,
                       title="Booking Value Distribution")

    st.plotly_chart(fig13, use_container_width=True)

    #scatter2
    st.subheader("Operational Efficiency (CTAT vs VTAT)")
    fig14 = px.scatter(df,
                     x="Avg CTAT",
                     y="Avg VTAT",
                     title="CTAT vs VTAT",
                     opacity=0.6)

    st.plotly_chart(fig14, use_container_width=True)