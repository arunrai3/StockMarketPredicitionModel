


def piechart(count_green_year, count_red_year, ax):
    # Prepare data
    labels = ['Green Years', 'Red Years']
    sizes = [count_green_year, count_red_year]
    colors = ['green', 'red']
    
    # Create pie chart
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)

    ax.axis('equal')  # Equal aspect ratio ensures a circular pie
    ax.set_title('% of Green/Red Years for last 10 Years', fontsize=12)  # Set chart title