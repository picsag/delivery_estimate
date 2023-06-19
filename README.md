# delivery_estimate

The raw data is a csv file with columns:
order_id	
account_id	
added	
estimated_preptime	
actual_preptime	order_total_items	
order_total_price	
account_cluster_id	
xhist_avg_actual_preptime	
xhist_avg_estimated_preptime

The file contains orders for food delivery. 
The column added is the date and time when order added. 
The estimated_preptime is the estimated cooking time and the actual_preptime is the actual cooking time. 
The account cluster_id is an integer number representing the city. 
The columns xhist_avg_actual_preptime is the average actual cooking time for the last 7 days including the day of the order. 
The xhist_avg_estimated_preptime is the average estimated cooking time for last 7 days including the day of the order.
Some of the values for 2 columns: xhist_avg_estimated_preptime and xhist_avg_actual_preptime are missing.

Actions performed:<br>
[Data preprocessing](data_preprocessing.py) - fill the last 2 columns with average values for last 7 days before the order date <br>
[Feature engineering](feature_engineering.py) - extract the date-time features <br>
[Train regressors](train_algos.py) - train scikit-learn based Random Forest regressor for each cluster <br>
[Dashboard](./dashboard/dashboard.py) - Dashboard with 2 tabs for business analysis and ML predictions <br>
[Dashboard Dockerfile](./dashboard/Dockerfile) - Dockerfile for the dashboard with Gunicorn for WSGI capability <br>
[GAN Feature generation](./generate_data.py) - Generative Adversarial Networks employed to generate artificial records <br>
... TO BE CONTINUED ...