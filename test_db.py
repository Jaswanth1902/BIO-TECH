from app import app, db
from models import ThresholdPolicy

with app.app_context():
    print("Policies:")
    for p in ThresholdPolicy.query.all():
        print(p.product_type, p.min_temp, p.max_temp)
