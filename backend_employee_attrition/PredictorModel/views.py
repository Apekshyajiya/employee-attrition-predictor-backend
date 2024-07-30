import pandas as pd
import json
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.



@csrf_exempt
# class ModelPredictor(APIView):
def predictor(request):
        if request.method == 'POST':
       #import the libraries
        # Load the data
            uploaded = 'WA_Fn-UseC_-HR-Employee-Attrition.csv'
            df = pd.read_csv(uploaded)

        # Remove some useless columns
            for column in ['Over18', 'EmployeeNumber', 'StandardHours', 'EmployeeCount']:
                if column in df.columns:
                    df = df.drop(column, axis=1)

        # Label encode categorical columns
            label_encoders = {}
            for column in df.columns:
                if df[column].dtype == 'object':  # Check if the column is categorical
                    le = LabelEncoder()
                    df[column] = le.fit_transform(df[column])
                    label_encoders[column] = le
        # joblib.dump(label_encoders, 'label_encoders.sav')
        # Separate features and target variable
            x = df.drop('Attrition', axis=1).values  # Assuming 'Attrition' is the target column
            y = df['Attrition'].values

        # Split the data into training and test sets
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

        # Initialize and train the RandomForestClassifier
            forest = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
            forest.fit(x_train, y_train)

        # Get the accuracy on the training dataset
            print(f"Training Accuracy: {forest.score(x_train, y_train)*100}")

        # Define a function to predict new data
            def predict_attrition(new_data_list):
            # Convert new_data to DataFrame
                new_df = pd.DataFrame(new_data_list, columns=df.columns[:-1])
            
            # Handle missing values
                for column in new_df.columns:
                    if new_df[column].isnull().any():
                    # Example: Fill missing values with the most frequent value in the training data
                        most_frequent = df[column].mode()[0]
                        new_df[column] = new_df[column].fillna(most_frequent)
            
            # Apply the same preprocessing as training data
                for column in new_df.columns:
                    if column in label_encoders:
                        le = label_encoders[column]
                        # Ensure all values are known to the encoder
                        new_df[column] = new_df[column].apply(lambda x: le.transform([x])[0] if x in le.classes_ else le.transform([le.classes_[0]])[0])
            
                 # Make predictions
                new_data_processed = new_df.values
                predictions = forest.predict(new_data_processed)
                return predictions

        # if request.method == 'POST':
             
            data = json.loads(request.body)
                # Extracting the values from the JSON data
            val1 = data.get('dailyrate')
            val2 = data.get('Gender')
            val3 = data.get('HourlyRate')
            val4 = data.get('Job_Involvement')
            val5 = data.get('Joblevel')
            val6 = data.get('JobSatisfaction')
            val7 = data.get('MaritalStatus')
            val8 = data.get('MonthlyIncome')
            val9 = data.get('Monthlyrate')
            val10 = data.get('NumCompaniesWorked')
            val11 = data.get('OverTime')
            val12 = data.get('PercentSalaryHike')
            val13 = data.get('Performancerating')
            val14 = data.get('TotalWorkingYears')
            val15 = data.get('WorkLifeBalance')
            val16 = data.get('YearsAtCompany')
            val17 = data.get('YearsInCurrentRole')
            val18 = data.get('YearsSinceLastPromotion')
            val19 = data.get('YearswithCurrManager')

            new_data = {
                    'dailyRate': val1, 'Gender': val2, 'HourlyRate': val3, 'JobInvolvement': val4, 'JobLevel': val5, 'JobSatisfaction': val6,
                    'MaritialStatus': val7, 'MonthlyIncome': val8, 'MonthlyRate': val9, 'NumCompaniesWorked': val10, 'OverTime': val11,
                    'PercentSalaryHike': val12, 'PerformanceRating': val13, 'TotalWorkingYears': val14, 'WorkLifeBalance': val15,
                    'YearsAtCompany': val16, 'YearsInCurrentRole': val17, 'YearsSinceLastPromotion': val18, 'YearsWithCurrManager': val19
                }
            new_data_list = [new_data]


        # Predict and print the results
        predictions = predict_attrition(new_data_list)
        print(f"Predictions: {predictions}")
        predictions_list = [int(pred) for pred in predictions]  # Convert directly to list if possible
        # predictions_list  = predictions.tolist          #converting to list
        print("Prediction List:", predictions_list)
        return JsonResponse({'prediction': predictions_list})