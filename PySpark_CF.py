from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
import hashlib
from pyspark import SparkConf, SparkContext

conf = SparkConf().setAppName("App")
conf = (conf.setMaster('local[*]')
        .set("spark.driver.memory", "32g")
		.set("spark.executor.memory", "8g")
		.set("spark.driver.allowMultipleContexts", "true"))
sc = SparkContext(conf=conf)

def hashStrToInt(s):
	return abs(hash(s)) % (10 ** 8)

# Load and parse the data
train_data = sc.textFile("spark/train_triplets.txt").map(lambda l: l.split('\t'))\
	.map(lambda (user, product, rate): Rating(hashStrToInt(user), hashStrToInt(product), float(rate)))
test_data = sc.textFile("spark/visible_evaluation_triplets.txt").map(lambda l: l.split('\t'))\
	.map(lambda (user, product, rate): Rating(hashStrToInt(user), hashStrToInt(product), float(rate)))
data = sc.union([train_data, test_data])

# Build the recommendation model using Alternating Least Squares
model = ALS.train(test_data, 5, 3)

Evaluate the model on training data
userProducts = test_data.map(lambda (user, product, rate): ((user, product)))
predictions = model.predictAll(userProducts)\
	.map(lambda (user, product, rate): ((user, product), rate)).cache()
ratesAndPreds = test_data.map(lambda (user, product, rate): ((user, product), rate)).join(predictions)
MSE = ratesAndPreds.map(lambda ((user, product), (r1, r2)): (r1 - r2)**2).mean()
print("Mean Squared Error = " + str(MSE))

model.save(sc, "spark/myPyCF_test")

recomm = model.recommendProductsForUsers(20)
recomm.saveAsTextFile('file:/Users/jacob/Downloads/results')

sc.stop()
