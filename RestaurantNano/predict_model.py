import numpy as np
import pandas as pd
import pickle
from surprise import SVD
import json
from datetime import datetime

def get_holiday_offer(date):
    with open('holidays_offers.json','r') as f:
        holiday_offers = json.load(f)
    if date in holiday_offers:
        print(f"Today is {holiday_offers[date]['holiday']}, take {holiday_offers[date]['offer']}")
    else:
        return
def get_product_id(id):
    with open('product_to_dish.json','r') as f:
        product_mapping = json.load(f)
    for p_id, dish in product_mapping.items():
        if id == p_id:
            return dish

# Load and preprocess the dataset
def preprocess_data(csv_path):
    df = pd.read_csv(csv_path)
    df = df.drop(['Id', 'ProfileName','Time','HelpfulnessNumerator','HelpfulnessDenominator','Text','Summary'], axis=1)
    df = df.groupby(['UserId', 'ProductId'], as_index=False)['Score'].mean()
    df.drop_duplicates(inplace=True)
    return df

def load_models():
    with open('svd_model.pkl', 'rb') as f:
        svd = pickle.load(f)
    
    with open('trainset.pkl', 'rb') as f:
        trainset = pickle.load(f)
    
    return svd, trainset

def ensemble_predict(svd, user_id, item_id):
    return svd.predict(user_id, item_id).est

def get_top_k_recommendations(svd, trainset, user_id, k=5, new_product_count=3):
    all_items = trainset.all_items()
    all_item_ids = [trainset.to_raw_iid(item) for item in all_items]

    inner_user_id = trainset.to_inner_uid(user_id)
    user_ratings = trainset.ur[inner_user_id]
    rated_items = [item for item, rating in user_ratings]

    predictions = []
    for item_id in all_item_ids:
        if item_id not in rated_items:
            predictions.append((item_id, ensemble_predict(svd, user_id, item_id)))
    
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    top_k = predictions[:k]
    new_products = [item for item in top_k if item[0] not in rated_items][:new_product_count]
    
    return top_k, new_products
def get_offers_on_points(id):
    with open('user_id_counts.json','r') as f:
        points = json.load(f)
    with open('restaurant_point_offers.json','r') as f:
        offer = json.load(f)
    for ids,ps in points:
        if(ids==id):
            points = ps*10
    for offer in offers_data:
        offer_range = offer['range']
        if offer_range[0] <= points <= offer_range[1]:
            print(f"You have {points} points, avail offer {offer['offer']}")


def get_popular_new_products(df, user_id, n=2):
    user_rated_items = df[df['UserId'] == user_id]['ProductId'].tolist()
    popular_items = df.groupby('ProductId').size().sort_values(ascending=False).index.tolist()
    popular_new_items = [item for item in popular_items if item not in user_rated_items][:n]
    return popular_new_items

def combined_recommendations(svd, trainset, df, user_id, k=5, new_product_count=3, n=2):
    top_k, new_products = get_top_k_recommendations(svd, trainset, user_id, k, new_product_count)
    popular_new_products = get_popular_new_products(df, user_id, n)
    combined = list(set([item[0] for item in top_k] + [item[0] for item in new_products] + popular_new_products))
    return combined

def recommend_for_user(svd, trainset, df, user_id, k=5, new_product_count=3, n=2):
    top_k, new_products = get_top_k_recommendations(svd, trainset, user_id, k, new_product_count)
    popular_new_products = get_popular_new_products(df, user_id, n)
    
    recommendations = {
        'user_history_based': top_k,
        'new_based_on_others': popular_new_products
    }
    
    return recommendations

def main_func(user_id):
    csv_path = r'Reviews.csv'  # Update with your dataset path
    df = preprocess_data(csv_path)
    svd, trainset = load_models()
    get_holiday_offer(datetime.today().strftime('%Y-%m-%d'))
    #get_offers_on_points(user_id)
    #user_id = 'A370Z6I5GBWU44'  # Replace with the detected user ID
    recommendations = recommend_for_user(svd, trainset, df, user_id)
    str = ""
    str+= "Recommendations for user {user_id}:"
    str+="Based on user's history:"
    for i in recommendations['user_history_based']:
       str+=" "+get_product_id(i[0])
    str+="Based on other similar users' history and popular items:"
    for i in recommendations['new_based_on_others']:
       str+=" "+get_product_id(i)
    return str
