import org.apache.spark.mllib.recommendation.ALS
import org.apache.spark.mllib.recommendation.MatrixFactorizationModel
import org.apache.spark.mllib.recommendation.Rating
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

val conf = new SparkConf()
.setMaster('local[*]')
.set("spark.driver.memory", "32g")
.set("spark.executor.memory", "8g")
.set("spark.driver.allowMultipleContexts", "true"))
val sc = new SparkContext(conf)

// spark/train_triplets.txt
val raw = sc.textFile("spark/train_triplets.txt")
val train_data = raw.map(_.split('\t') match {
	case Array(user, product, rate) =>
	Rating(Math.abs(user.hashCode()), Math.abs(product.hashCode()), rate.toDouble)
})
// spark/visible_evaluation_triplets.txt
val test_raw = sc.textFile("spark/visible_evaluation_triplets.txt")
val test_data = test_raw.map(_.split('\t') match {
	case Array(user, product, rate) =>
	Rating(Math.abs(user.hashCode()), Math.abs(product.hashCode()), rate.toDouble)
})
val data = train_data.union(test_data)
// Build the recommendation model using ALS
val rank = 5
val numIterations = 3
val model = ALS.train(data, rank, numIterations, 0.01)

// Evaluate the model on rating test_data
val usersProducts = test_data.map {
	case Rating(user, product, rate) => (user, product)
}
val predictions =
	model.predict(usersProducts).map {
		case Rating(user, product, rate) => ((user, product), rate)
}

val ratesAndPreds = test_data.map {
	case Rating(user, product, rate) => ((user, product), rate)
}.join(predictions)

val MSE = ratesAndPreds.map { case ((user, product), (r1, r2)) =>
	val err = (r1 - r2)
	err * err
}.mean

println("Mean Squared Error = " + MPE)

val users = test_ratings.map(_.user).distinct().collect()
val recommendations = users.map{user => model.recommendProducts(user, 5)}