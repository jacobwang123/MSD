from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
import hashlib
from sys import argv
from pyspark import SparkConf, SparkContext

conf = (SparkConf().set("spark.executor.memory", "6g"))
sc = SparkContext(conf = conf)

script, user, num = argv

def hashStrToInt(s):
	return abs(hash(s)) % (10 ** 8)

model = MatrixFactorizationModel.load(sc, "spark/myPyCF")
user = hashStrToInt(user)
r = model.recommendProducts(user, int(num))
for i in r:
	print(i.product)