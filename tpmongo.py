from pymongo import MongoClient

# Connexion à MongoDB
client = MongoClient("mongodb+srv://gueye:Abdou2025@abdou.6xgcm.mongodb.net/")
db = client['montpmongo']
reviews_collection = db['avis_clients']

# 1. Insérer les avis dans MongoDB
avis_clients = [
    {"client_id": "C001", "product_id": "P001", "rating": 5, "comment": "Excellent!", "date": "2024-01-01"},
    {"client_id": "C002", "product_id": "P002", "rating": 3, "comment": "Average product.", "date": "2024-01-02"},
    {"client_id": "C001", "product_id": "P003", "rating": 4, "comment": "Very good", "date": "2024-01-03"},
]
reviews_collection.insert_many(avis_clients)

# 2. Récupérer et afficher les avis sous forme de tuples
cursor = reviews_collection.find()
reviews_tuples = [(review['client_id'], review['product_id'], review['rating'], review['comment'], review['date']) for review in cursor]
print("Données converties en liste de tuples :")
for review in reviews_tuples:
    print(review)

# 3. Agrégation pour trouver le produit avec la meilleure note moyenne
pipeline_best_product = [
    {"$group": {"_id": "$product_id", "average_rating": {"$avg": "$rating"}}},
    {"$sort": {"average_rating": -1}},
    {"$limit": 1}
]
result_best_product = reviews_collection.aggregate(pipeline_best_product)
for doc in result_best_product:
    print(f"Le produit avec la meilleure note moyenne est {doc['_id']} avec une note de {doc['average_rating']:.2f}")

# 4. Agrégation pour trouver le client ayant laissé le plus d'avis
pipeline_most_reviews = [
    {"$group": {"_id": "$client_id", "total_reviews": {"$sum": 1}}},
    {"$sort": {"total_reviews": -1}},
    {"$limit": 1}
]
result_most_reviews = reviews_collection.aggregate(pipeline_most_reviews)
for doc in result_most_reviews:
    print(f"Le client ayant laissé le plus d'avis est {doc['_id']} avec {doc['total_reviews']} avis.")

# 5. Agrégation pour compter le nombre total d'avis par produit
pipeline_count_reviews_by_product = [
    {"$group": {"_id": "$product_id", "total_reviews": {"$sum": 1}}},
    {"$sort": {"total_reviews": -1}}
]
result_count_reviews_by_product = reviews_collection.aggregate(pipeline_count_reviews_by_product)
for doc in result_count_reviews_by_product:
    print(f"Le produit {doc['_id']} a {doc['total_reviews']} avis.")
