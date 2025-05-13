import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Load data
column_names = ['bus_routes_link', 'bus_routes_name', 'bus_name', 'bus_type', 'departure_time', 'duration', 'arrival_time', 
                'rating', 'seats_available', 'price', 'state']

# Get the current directory
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, 'Busses.csv')
img_path = os.path.join(current_dir, 'rb.png')

# Reading the CSV file
df = pd.read_csv(csv_path, names=column_names)

# Ensure correct datatypes
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['seats_available'] = pd.to_numeric(df['seats_available'], errors='coerce')

# Main menu
st.sidebar.title("Main Menu")
page = st.sidebar.radio("Navigation", ["Home", "Select the Bus"])

# Departure time categorization
def categorize_departure_time(time):
    try:
        time_obj = datetime.strptime(time.strip(), "%H:%M").time()
        if time_obj <= datetime.strptime("06:00", "%H:%M").time():
            return "00:00-06:00"
        elif time_obj <= datetime.strptime("12:00", "%H:%M").time():
            return "06:01-12:00"
        elif time_obj <= datetime.strptime("18:00", "%H:%M").time():
            return "12:01-18:00"
        else:
            return "18:01-23:59"
    except:
        return "Unknown"

# Price range categorization
def categorize_price(price):
    if 0 <= price <= 250:
        return '0-250'
    elif 251 <= price <= 500:
        return '251-500'
    elif 501 <= price <= 1000:
        return '500-1000'
    elif 1001 <= price <= 2000:
        return '1000-2000'
    elif 2001 <= price <= 5000:
        return '2000-5000'
    else:
        return 'Unknown'

# Home page
if page == "Home":
    st.markdown("""
    <div style='text-align: center; font-size: 120px; color:white'>
        Home page
    </div>
    """, unsafe_allow_html=True)
    st.image(img_path, width=600)

# Bus selection page
elif page == "Select the Bus":
    st.title("Select the Bus")

    col1, col2, col3 = st.columns(3)

    # First row of filters: Rating, State, Route
    with col1:
        min_rating = float(df['rating'].min())
        max_rating = float(df['rating'].max())
        selected_rating = st.slider("Select rating range", min_value=0.0, max_value=5.0,
                                    value=(min_rating, max_rating), step=0.1)

    with col2:
        states = ['All'] + sorted(df['state'].dropna().unique().tolist())
        selected_state = st.selectbox("Select State", states)

    with col3:
        if selected_state != 'All':
            filtered_routes = df[df['state'] == selected_state]['bus_routes_name'].unique()
        else:
            filtered_routes = df['bus_routes_name'].unique()

        routes = ['All'] + sorted(filtered_routes.tolist())
        selected_bus_name = st.selectbox("Select Route", routes)

    # Second row: Departure, Price, Seat Type
    col4, col5, col6 = st.columns(3)

    with col4:
        departure_time_ranges = ['All', '00:00-06:00', '06:01-12:00', '12:01-18:00', '18:01-23:59']
        selected_departure_time = st.selectbox('Select Departure Time:', departure_time_ranges)

    with col5:
        price_ranges = ['All', '0-250', '251-500', '500-1000', '1000-2000', '2000-5000']
        selected_price_range = st.selectbox('Select Price Range:', price_ranges)

    with col6:
        seat_types = ['All', 'Sleeper', 'Seater']
        selected_seat_type = st.selectbox('Select Seat Type:', seat_types)

    # Third row: A/C and Seat Availability
    col7, col8 = st.columns(2)

    with col7:
        ac_types = ['All', 'A/C', 'NON A/C']
        selected_ac_type = st.selectbox('Select A/C Type:', ac_types)

    with col8:
        seat_avail_options = ['All', 'Seats > 0', 'Seats > 10', 'Seats > 20']
        selected_seat_avail = st.selectbox("Select Seat Availability:", seat_avail_options)

    # Start filtering
    if selected_state != 'All':
        df = df[df['state'] == selected_state]

    if selected_bus_name != 'All':
        df = df[df['bus_routes_name'] == selected_bus_name]

    if selected_departure_time != 'All':
        df = df[df['departure_time'].apply(categorize_departure_time) == selected_departure_time]

    if selected_price_range != 'All':
        df = df[df['price'].apply(categorize_price) == selected_price_range]

    if selected_seat_type != 'All':
        keyword = 'Sleeper' if selected_seat_type == 'Sleeper' else 'Seater'
        df = df[df['bus_type'].str.lower().str.contains(keyword.lower())]

    if selected_ac_type != 'All':
        keyword = 'a/c' if selected_ac_type == 'A/C' else 'non a/c'
        df = df[df['bus_type'].str.lower().str.contains(keyword)]

    if selected_seat_avail != 'All':
        if selected_seat_avail == 'Seats > 0':
            df = df[df['seats_available'] > 0]
        elif selected_seat_avail == 'Seats > 10':
            df = df[df['seats_available'] > 10]
        elif selected_seat_avail == 'Seats > 20':
            df = df[df['seats_available'] > 20]

    # Rating slider filter
    df = df[(df['rating'] >= selected_rating[0]) & (df['rating'] <= selected_rating[1])]

    # Display filtered result
    st.write("Filtered Bus Details:")
    st.dataframe(df.reset_index(drop=True))

