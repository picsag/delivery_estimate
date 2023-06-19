FROM python:3.9

WORKDIR /app

# Copy the datasets
COPY data_final.csv .
COPY mse_scores_randomforest.csv .
COPY mse_scores_fused_randomforest.csv .

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --index-url=https://pypi.org/simple/ -r requirements.txt

# Copy the Dash app code
COPY dashboard.py .

# Expose port 80
EXPOSE 80

# Run the Dash app with Gunicorn
CMD ["gunicorn", "dashboard:server", "-b", "0.0.0.0:80", "--workers=4"]
