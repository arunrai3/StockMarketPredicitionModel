


def predicitionModel(training_data, date,open,close, type):
    global good_score
    global total_score
    # Extract the training features and labels from the training_data
    training_features = [[bar.close, bar.high, bar.open, bar.low, bar.volume] for bar in training_data]
    training_labels = ['green' if bar.close > bar.open else 'red' for bar in training_data]

    
    clf = DecisionTreeClassifier()
    clf.fit(training_features, training_labels)

    # Extract the features of the last bar in the training_data (current day's features)
    recent_features = training_features[-100:]

    # Predict the label for the next trading day (2020-01-02)
    next_day_prediction = clf.predict(recent_features)
    
    diff = close - open
    if diff > 0:
        answer = 'green'
    else:
        answer = 'red'
    
    if type == "regular":
        if answer == next_day_prediction[0]:
            good_score = good_score + 1
        total_score = total_score + 1
        
    if type == "marketopen":
        print("Prediction for {:<18} {:<20} Answer: {:<20}".format(str(date) + ":", next_day_prediction[0], "Unknown, because market is still open."))
    elif type == "regular":
        print("Prediction for {:<18} {:<20} Answer: {:<20}".format(str(date) + ":", next_day_prediction[0], answer))
    elif type == "marketclosed":
        print("Prediction for {:<18} {:<20} Answer: {:<20}".format("Next Trading Day:", next_day_prediction[0], "Unknown"))