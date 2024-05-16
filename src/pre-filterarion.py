from pymongo import MongoClient
import sys
sys.path.append('mongodb-vector-search')
from util import config
import numpy as np

# Connect to MongoDB Atlas
client = MongoClient(config.MONGO_URI)
db = config.DB_NAME
collection = config.COLLECTION_NAME



# define pipeline
pipeline = [
    {
        '$vectorSearch': {
            'index': 'vector_search',
            'path': 'plot_embedding',
            'filter': {
                '$and': [
                    {
                        'genres': {
                            '$in': [
                                'Drama', 'Western', 'Crime'
                            ],
                            '$nin': [
                                'Action', 'Adventure', 'Family'
                            ]
                        }
                    }, {
                        'year': {
                            '$gte': 1960,
                            '$lte': 2000
                        }
                    }
                ]
            },
            'queryVector': list(np.random.uniform(-1, 1, 1536)),
            'numCandidates': 200,
            'limit': 10
        }
    }, {
        '$project': {
            '_id': 0,
            'title': 1,
            'genres': 1,
            'plot': 1,
            'year': 1,
            'score': {
                '$meta': 'vectorSearchScore'
            }
        }
    }
]

# # Perform pre-filtration using aggregation
# filtered_data = list(collection.aggregate(pipeline))
#
# # Assess the filtered data
# for document in filtered_data:
#     print(document)


# run pipeline
result = client[db][collection].aggregate(pipeline)

# print results
for i in result:
    print(i)

# Close the connection
client.close()



