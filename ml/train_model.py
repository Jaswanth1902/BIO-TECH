import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import pickle
import os

def create_dummy_data():
    np.random.seed(42)
    n_samples = 200
    
    # avg_temp, max_temp, avg_humidity, elapsed_days, product_type (mock mapping)
    # Target: remaining_days
    
    avg_temp = np.random.normal(20, 5, n_samples)
    max_temp = avg_temp + np.random.uniform(0, 10, n_samples)
    avg_humidity = np.random.normal(60, 15, n_samples)
    elapsed_days = np.random.randint(1, 30, n_samples)
    product_type = np.random.randint(0, 2, n_samples) # 0 for sample, 1 for food
    
    # Calculate target (simple arbitrary logical rule for dummy)
    # Cooler temps and lower humidity mean more shelf life
    # Food spoils faster than samples
    
    base_shelf_life = np.where(product_type == 1, 30, 60)
    temp_penalty = (avg_temp - 10) * 0.5
    humidity_penalty = (avg_humidity - 50) * 0.2
    
    remaining_days = base_shelf_life - temp_penalty - humidity_penalty - elapsed_days
    remaining_days = np.maximum(0, remaining_days) # Can't go below 0
    
    df = pd.DataFrame({
        'avg_temp': avg_temp,
        'max_temp': max_temp,
        'avg_humidity': avg_humidity,
        'elapsed_days': elapsed_days,
        'product_type': product_type,
        'remaining_days': remaining_days
    })
    
    return df

def train_and_save():
    df = create_dummy_data()
    X = df[['avg_temp', 'max_temp', 'avg_humidity', 'elapsed_days', 'product_type']]
    y = df['remaining_days']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LinearRegression())
    ])
    
    pipeline.fit(X_train, y_train)
    
    score = pipeline.score(X_test, y_test)
    print(f"Model trained with R^2 score: {score:.2f}")
    
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)
    print(f"Model saved to {model_path}")

if __name__ == '__main__':
    train_and_save()
