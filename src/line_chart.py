


def linechart(dailychart, ax):
    # Extracting date and close values from the dailychart objects
    dates = [data.date for data in dailychart]
    close_values = [data.close for data in dailychart]

    # Creating the line chart
    ax.plot(dates, close_values, linestyle='-', color='blue')
    
    # Adding labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Close')
    ax.set_title('Daily Close Prices')
    
    # Rotating the x-axis labels for better readability
    ax.tick_params(axis='x', rotation=45)