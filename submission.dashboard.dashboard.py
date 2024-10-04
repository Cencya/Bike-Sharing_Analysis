import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
day_df = pd.read_csv('day_df.csv')
hour_df = pd.read_csv('hour_df.csv')

def plot_seasonal_rentals():
    plt.figure(figsize=(8, 5))
    color_mapping = {
        'Spring': 'pink',
        'Summer': 'yellow',
        'Fall': 'orange',
        'Winter': 'skyblue'
    }
    season_counts = day_df.groupby(by="Season").Count.sum().sort_values(ascending=False)
    colors = [color_mapping[season] for season in season_counts.index]
    ax = season_counts.plot(kind='bar', color=colors)

    for i, count in enumerate(season_counts):
        ax.text(i, count, str(count), ha='center', va='bottom')

    plt.title('Total Bike Rentals by Season')
    plt.xlabel('Season')
    plt.ylabel('Total Rentals')
    plt.xticks(ticks=range(len(season_counts.index)), labels=season_counts.index, rotation=0)
    plt.tight_layout()

# Function for Working Day vs Weekend/Holiday
def plot_working_vs_holiday_by_days():
    holiday_counts = day_df['Holiday'].value_counts()
    workingday_counts = day_df['Workingday'].value_counts()

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    # Bar chart for Holiday
    bars_holiday = ax[0].bar(holiday_counts.index.astype(str), holiday_counts.values, color=['lightcoral', 'lightgreen'])
    ax[0].set_title('Count of Rentals by Holiday Status')
    ax[0].set_xlabel('Holiday (0: No, 1: Yes)')
    ax[0].set_ylabel('Count of Rentals')

    for bar in bars_holiday:
        yval = bar.get_height()
        ax[0].text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')

    # Bar chart for Working Day
    bars_workingday = ax[1].bar(workingday_counts.index.astype(str), workingday_counts.values, color=['lightgreen', 'lightcoral'])
    ax[1].set_title('Count of Rentals by Working Day Status')
    ax[1].set_ylabel('Count of Rentals')

    for bar in bars_workingday:
        yval = bar.get_height()
        ax[1].text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom')

    plt.tight_layout()

# Function for Casual and Registered Users by Days
def plot_casual_vs_registered_by_days():
    # Grouping data for Casual and Registered Users
    grouped_data = day_df.groupby('Workingday')[['Casual', 'Registered']].sum()

    labels = ['Weekend/Holiday', 'Working Day']

    casual_users = grouped_data['Casual']
    registered_users = grouped_data['Registered']

    x = range(len(labels))

    fig, ax = plt.subplots(figsize=(8, 5))
    bar_width = 0.35

    ax.bar(x, casual_users, width=bar_width, color='skyblue', label=f'Casual Users: {casual_users.sum()}')
    ax.bar([i + bar_width for i in x], registered_users, width=bar_width, color='lightgreen', label=f'Registered Users: {registered_users.sum()}')

    ax.set_xlabel('Day Type')
    ax.set_ylabel('Total Users')
    ax.set_title('Total Casual and Registered Users on Working Days and Weekends/Holidays')
    ax.set_xticks([i + bar_width/2 for i in x])
    ax.set_xticklabels(labels)
    ax.legend()

    for i, v in enumerate(casual_users):
        ax.text(i, v + 100, str(v), ha='center')

    for i, v in enumerate(registered_users):
        ax.text(i + bar_width, v + 100, str(v), ha='center')

    plt.tight_layout()

# Function for Hourly Trends during Working Day and Weekend/Holiday
def plot_hourly_trends():
    hourly_trend = hour_df.groupby(['Workingday', 'Hour'])[['Casual', 'Registered']].sum().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))

    # Workingday rentals
    ax.plot(hourly_trend[hourly_trend['Workingday'] == 1]['Hour'],
            hourly_trend[hourly_trend['Workingday'] == 1]['Casual'],
            label='Working Day Casual', color='skyblue', marker='o')

    ax.plot(hourly_trend[hourly_trend['Workingday'] == 1]['Hour'],
            hourly_trend[hourly_trend['Workingday'] == 1]['Registered'],
            label='Working Day Registered', color='lightgreen', marker='o')

    # Weekend/holiday rentals
    ax.plot(hourly_trend[hourly_trend['Workingday'] == 0]['Hour'],
            hourly_trend[hourly_trend['Workingday'] == 0]['Casual'],
            label='Weekend/Holiday Casual', color='blue', marker='o')

    ax.plot(hourly_trend[hourly_trend['Workingday'] == 0]['Hour'],
            hourly_trend[hourly_trend['Workingday'] == 0]['Registered'],
            label='Weekend/Holiday Registered', color='green', marker='o')

    # Set x-ticks to show all hours from 0 to 23
    ax.set_xticks(range(24))

    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Hourly Rental Trends: Working Day vs Weekend/Holiday')

    ax.legend()
    plt.grid()
    plt.tight_layout()

# Function for Impacts of Weather
def plot_weather():
    weather_trend = day_df.groupby('Weather')[['Casual', 'Registered']].sum().reset_index()

    # Total rentals
    total_casual = weather_trend['Casual'].sum()
    total_registered = weather_trend['Registered'].sum()

    fig, ax = plt.subplots(figsize=(10, 6))

    # Bars for Casual and Registered rentals
    bar_width = 0.35
    x = range(len(weather_trend['Weather']))

    bar1 = ax.bar(x, weather_trend['Casual'], width=bar_width, label=f'Casual ({total_casual})', color='skyblue')
    bar2 = ax.bar([p + bar_width for p in x], weather_trend['Registered'], width=bar_width, label=f'Registered ({total_registered})', color='lightgreen')

    # Total rentals for each bar
    for i in range(len(weather_trend)):
        ax.text(i, weather_trend['Casual'][i] + 5, weather_trend['Casual'][i], ha='center', va='bottom')
        ax.text(i + bar_width, weather_trend['Registered'][i] + 5, weather_trend['Registered'][i], ha='center', va='bottom')

    ax.set_xticks([p + bar_width / 2 for p in x])
    ax.set_xticklabels(weather_trend['Weather'])
    ax.set_xlabel('Weather Condition')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Impact of Weather on Bike-Sharing')
    ax.legend()
    
    plt.tight_layout()

# Function for User Trends
def plot_user_trends():
    # Group data by Year and Month
    trend_data = day_df.groupby(['Year', 'Month'])[['Casual', 'Registered']].sum().reset_index()

    # Total rentals for each casual and registered
    total_casual_2011 = trend_data[trend_data['Year'] == 2011]['Casual'].sum()
    total_registered_2011 = trend_data[trend_data['Year'] == 2011]['Registered'].sum()
    total_casual_2012 = trend_data[trend_data['Year'] == 2012]['Casual'].sum()
    total_registered_2012 = trend_data[trend_data['Year'] == 2012]['Registered'].sum()

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # 2011 Casual and Registered rentals
    axs[0].plot(trend_data[trend_data['Year'] == 2011]['Month'],
                trend_data[trend_data['Year'] == 2011]['Casual'],
                marker='o', color='skyblue', label=f'Casual Users (Total: {total_casual_2011})')
    axs[0].plot(trend_data[trend_data['Year'] == 2011]['Month'],
                trend_data[trend_data['Year'] == 2011]['Registered'],
                marker='o', color='lightgreen', label=f'Registered Users (Total: {total_registered_2011})')
    axs[0].set_title('2011 Rentals')
    axs[0].set_xlabel('Month')
    axs[0].set_ylabel('Number of Rentals')
    axs[0].set_xticks(trend_data['Month'].unique())
    axs[0].legend()

    # Actual rentals for each month in 2011
    for i in range(len(trend_data[trend_data['Year'] == 2011])):
        axs[0].text(trend_data[trend_data['Year'] == 2011]['Month'].iloc[i],
                    trend_data[trend_data['Year'] == 2011]['Casual'].iloc[i],
                    str(trend_data[trend_data['Year'] == 2011]['Casual'].iloc[i]),
                    fontsize=8, ha='center', va='bottom')
        axs[0].text(trend_data[trend_data['Year'] == 2011]['Month'].iloc[i],
                    trend_data[trend_data['Year'] == 2011]['Registered'].iloc[i],
                    str(trend_data[trend_data['Year'] == 2011]['Registered'].iloc[i]),
                    fontsize=8, ha='center', va='bottom')

    # 2012 Casual and Registered rentals
    axs[1].plot(trend_data[trend_data['Year'] == 2012]['Month'],
                trend_data[trend_data['Year'] == 2012]['Casual'],
                marker='o', color='skyblue', label=f'Casual Users (Total: {total_casual_2012})')
    axs[1].plot(trend_data[trend_data['Year'] == 2012]['Month'],
                trend_data[trend_data['Year'] == 2012]['Registered'],
                marker='o', color='lightgreen', label=f'Registered Users (Total: {total_registered_2012})')
    axs[1].set_title('2012 Rentals')
    axs[1].set_xlabel('Month')
    axs[1].set_ylabel('Number of Rentals')
    axs[1].set_xticks(trend_data['Month'].unique())
    axs[1].legend()

    # Actual rentals for each month in 2012
    for i in range(len(trend_data[trend_data['Year'] == 2012])):
        axs[1].text(trend_data[trend_data['Year'] == 2012]['Month'].iloc[i],
                    trend_data[trend_data['Year'] == 2012]['Casual'].iloc[i],
                    str(trend_data[trend_data['Year'] == 2012]['Casual'].iloc[i]),
                    fontsize=8, ha='center', va='bottom')
        axs[1].text(trend_data[trend_data['Year'] == 2012]['Month'].iloc[i],
                    trend_data[trend_data['Year'] == 2012]['Registered'].iloc[i],
                    str(trend_data[trend_data['Year'] == 2012]['Registered'].iloc[i]),
                    fontsize=8, ha='center', va='bottom')

    plt.tight_layout()

# Function for Bike-Sharing Growth
def plot_bike_sharing_growth():
    # Extract month and year from the 'Datetime' column
    day_df['Datetime'] = pd.to_datetime(day_df['Datetime'])
    hour_df['Datetime'] = pd.to_datetime(hour_df['Datetime'])
    day_df['Month'] = day_df['Datetime'].dt.month
    day_df['Year'] = day_df['Datetime'].dt.year
    
    # Group data by Year and Month
    monthly_trend = day_df.groupby(['Year', 'Month'])[['Casual', 'Registered']].sum().reset_index()

    monthly_trend['MonthLabel'] = monthly_trend['Month'].astype(str)  

    month_ticks = monthly_trend['MonthLabel'].tolist() 

    fig, ax = plt.subplots(figsize=(12, 6))

    # Plotting Casual rentals
    ax.plot(monthly_trend.index, 
            monthly_trend['Casual'],
            label='Casual Users', color='skyblue', marker='o')

    # Plotting Registered rentals
    ax.plot(monthly_trend.index,
            monthly_trend['Registered'],
            label='Registered Users', color='lightgreen', marker='o')

    ax.set_xlabel('2011 - 2012')
    ax.set_ylabel('Number of Rentals')
    ax.set_title('Growth from 2011 to 2012')

    ax.set_xticks(monthly_trend.index)
    ax.set_xticklabels(month_ticks, rotation=0) 

    # Displaying total rentals on each point
    for i, (casual, registered) in enumerate(zip(monthly_trend['Casual'], monthly_trend['Registered'])):
        ax.text(i, casual, str(casual), ha='center', va='bottom')
        ax.text(i, registered, str(registered), ha='center', va='bottom')

    plt.legend()
    plt.grid()
    plt.tight_layout()

# Sidebar for title, date range, and options
st.sidebar.title('Bike-Sharing')
st.sidebar.write('Dataset Date Range: 2011 - 2012')

# Sidebar options
options = ['Home', 'Seasonal Rentals', 'Working Day vs Weekend/Holiday', 'Impacts of Weather', 'Casual Users vs Registered Users']  
selected_option = st.sidebar.selectbox("Select Analysis:", options)

# Home section
if selected_option == 'Home':
    st.title("Bike-Sharing Analysis")
    img_file = 'bike-sharing.jpg'
    st.image(img_file, caption='Bike-Sharing', width=300)
    st.write("This app provides insights into bike-sharing rentals from 2011 to 2012.")
    st.write("Explore the data by selecting an option from the sidebar.")
    st.subheader("Dataset")
    st.markdown("[Source](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)")
    st.subheader("Created by")
    st.write("Vincent Pangdipta")
    st.subheader("Email")
    st.markdown("[vincent17ede@gmail.com](mailto:vincent17ede@gmail.com)")
    st.markdown("[m195b4ky4430@bangkit.academy](m195b4ky4430@bangkit.academy)")

# Seasonal Rentals
elif selected_option == 'Seasonal Rentals':
    st.header('Seasonal Rentals')
    with st.container():
        plot_seasonal_rentals()  
        st.pyplot(plt)  
        with st.expander("Insight"):
            st.write(""" 
            We clustered the rents by Season:
        
            - **Spring** includes March, April, and May: 1,061,129 Users
            - **Summer** includes June, July, and August: 471,348 Users
            - **Fall** includes September, October, and November: 918,589 Users
            - **Winter** includes December, January, and February: 841,613 Users
        
            Fall was the Season that has the highest rentals throughout 2011-2012, while Spring was the Season with the lowest rentals during the same period.
            """)

# Working Day vs Weekend/Holiday
elif selected_option == 'Working Day vs Weekend/Holiday':
    st.header('Working Day vs Weekend/Holiday')
    with st.container():
        st.subheader('Distribution of Bike Rentals in 2011-2012 by Days')
        plot_working_vs_holiday_by_days()  
        st.pyplot(plt) 
        with st.expander("Insight"):
            st.write(""" 
            - **Working Days:** 500 bike-sharing rentals recorded.
            - **Weekend/Holidays:** 231 bike-sharing rentals recorded, where 21 were on holidays.
            """)

        # Casual vs Registered Users
        st.subheader('Total Casual and Registered Users on Working Days and Weekends/Holidays')
        plot_casual_vs_registered_by_days()
        st.pyplot(plt)
        with st.expander("Insight"):
            st.write(""" 
            - Casual Users slightly prefer to rent during Weekend/Holiday.
            - Registered Users prefer to rent during Working Day.
            - Overall, bike-sharing usage is higher on Working Day compared to Weekend/Holiday.
            """)

    #Hourly Trends
    with st.container():
        st.subheader('Hourly Rental Trends')
        plot_hourly_trends()
        st.pyplot(plt)
        with st.expander("Insight"):
            st.write(""" 
            - Peak hour for Workingday Registered rentals are at 17:00, followed by 18:00 and 08:00 respectively. We could also interpreted that many people using bike-sharing services to commute during workingdays.
            - Workingday Casual, Weekend/Holiday Casual and Registered rentals, all have similar patterns from 08:00-20:00. We can interpreted that bike-sharing services are popular during those hours as leisure activity.
            """)

# Impacts of Weather
elif selected_option == 'Impacts of Weather':
    st.header('Impacts of Weather on Bike-Sharing')
    with st.container():
        plot_weather()
        st.pyplot(plt)
        with st.expander('Insight'):
            st.write(""" 
            - Weather have a significant impacts on Bike-Sharing
            - More people tend to rent during good weather compared to moderate and poor weather
            - No rentals occurred during severe weather
            """)

# Casual vs Registered Trends
elif selected_option == 'Casual Users vs Registered Users':
    st.header('Casual Users and Registered Users')

    # Trends
    with st.container():
        st.subheader('Trends of Casual Users and Registered Users')
        plot_user_trends()
        st.pyplot(plt)
        with st.expander("2011 Trends"):
            st.write("""
            - Registered Users; Bike-Sharing rentals started increasing significantly in April, with June being the peak, and gradually began to decline from August.
            - Casual Users; Bike-Sharing rentals started increasing significantly in April, with July being the peak, and gradually began to decline from August.
            """)         
        with st.expander("2012 Trends"):
            st.write("""
            - Registered Users; Bike-Sharing rentals started increasing significantly in March, with September being the peak, and began to decline significantly in November.
            - Casual
            Users; Bike-Sharing rentals started increasing significantly in March, with May being the peak, and gradually began to decline from October. But throughout May to September, the number of rentals remained fairly consistent.
            """)

    #Growth
    with st.container():        
        st.subheader('Bike-Sharing Growth')
        plot_bike_sharing_growth()
        st.pyplot(plt)
        st.write(""" 
        There is a significant increase for Registered Users from 2011 to 2012, while the growth in Casual Users is relatively small in comparison.
        """)
        with st.expander("Insight"):
            st.write("""
            - The Peak for Registered Users was in September 2012
            - The Peak for Casula Users was in May 2012
            - During both 2011 and 2012, the early months of the year consistently recorded the lowest bike-sharing rentals. This trend highlights a seasonal pattern where usage is minimal in the initial months, likely due to colder weather and reduced outdoor activities
            """)
