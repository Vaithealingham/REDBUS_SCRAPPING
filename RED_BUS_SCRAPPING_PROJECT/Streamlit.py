import streamlit as st
import pandas as pd
import os

# Load data
column_names = ['bus_routes_link', 'bus_routes_name', 'bus_name', 'bus_type', 'departure_time', 'duration', 'arrival_time', 'rating', 'seats_available', 'price']
# Get the current directory
current_dir = os.path.dirname(__file__)

# Assuming the CSV file is named 'data.csv' in the same folder as your Streamlit script
csv_path = os.path.join(current_dir, 'bus_details.csv')
img_path = os.path.join(current_dir, 'rb.png')
df = pd.read_csv(csv_path, names=column_names)

# Main menu in the sidebar
st.sidebar.title("Main Menu")
page = st.sidebar.radio("Navigation", ["Home", "Select the Bus"])

# Function to create rating ranges
def create_rating_ranges():
    return ['All', '0-1', '1-2', '2-3', '3-4', '4-5']

# Function to categorize departure times
def categorize_departure_time(time):
    if '00:00' <= time <= '06:00':
        return '00:00-06:00'
    elif '06:01' <= time <= '12:00':
        return '06:01-12:00'
    elif '12:01' <= time <= '18:00':
        return '12:01-18:00'
    elif '18:01' <= time <= '23:59':
        return '18:01-23:59'
    else:
        return 'Unknown'

# Function to categorize price ranges
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

# Display content based on the selection
if page == "Home":
    st.markdown("""
    <div style='text-align: center; font-size: 120px; color:white'>
        Home page
        </div>
    """, unsafe_allow_html=True)
    st.image(img_path, width=600)

elif page == "Select the Bus":
    st.title("Select the Bus")

    col1, col2, col3 = st.columns(3)

    # First row: Selectboxes for ratings, bus name, and departure time
    with col1:
        selected_rating_range = st.selectbox('Select the ratings:', create_rating_ranges())

    with col2:
        unique_bus_names = ['All'] + df['bus_routes_name'].unique().tolist()
        selected_bus_name = st.selectbox('Select the Route:', unique_bus_names)

    with col3:
        departure_time_ranges = ['All', '00:00-06:00', '06:01-12:00', '12:01-18:00', '18:01-23:59']
        selected_departure_time = st.selectbox('Select the departure time:', departure_time_ranges)

    # Second row: Selectboxes for price range, seat type, and A/C type
    col4, col5, col6 = st.columns(3)

    with col4:
        price_ranges = ['All', '0-250', '251-500', '500-1000', '1000-2000', '2000-5000']
        selected_price_range = st.selectbox('Select the price range:', price_ranges)

    with col5:
        seat_types = ['All', 'Sleeper', 'Seater']
        selected_seat_type = st.selectbox('Select the seat type:', seat_types)

    with col6:
        ac_types = ['All', 'A/C', 'NON A/C']
        selected_ac_type = st.selectbox('Select the A/C type:', ac_types)

# Additional Streamlit components can follow
    # Filter data based on selected criteria
    if selected_bus_name != 'All':
        df = df[df['bus_routes_name'] == selected_bus_name]

    if selected_departure_time != 'All':
        df = df[df['departure_time'].apply(categorize_departure_time) == selected_departure_time]

    if selected_price_range != 'All':
        df = df[df['price'].apply(categorize_price) == selected_price_range]

    if selected_seat_type != 'All':
        bus_type_keyword = 'Sleeper' if selected_seat_type == 'Sleeper' else 'Seater'
        df = df[df['bus_type'].str.contains(bus_type_keyword)]

    if selected_ac_type != 'All':
        ac_keyword = 'A/C' if selected_ac_type == 'A/C' else 'NON AC'
        df = df[df['bus_type'].str.contains(ac_keyword)]

    # Apply rating range filter
    if selected_rating_range != 'All':
        lower_rating, upper_rating = map(float, selected_rating_range.split('-'))
        df = df[(df['rating'] >= lower_rating) & (df['rating'] < upper_rating)]

    # Display filtered data
    st.write("Filtered Data:")
    st.dataframe(df)

else:
    st.write("Required columns not found in the data.")
