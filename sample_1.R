#Libraries
library("ISLR")
library(e1071)
library(caret)

#Data
attach(OJ)
fix(OJ)
set.seed(1) 
train = sample(nrow(OJ), 800, replace = FALSE) 
test = -train 
data.train = data.frame(OJ[train,])
data.test = data.frame(OJ[test,])
data.test.x = data.test[,-1]
data.test.y = Purchase


#Linear Kernel
svm.linear = svm(Purchase~., data = data.train, kernel = "linear", cost = 0.01, scale = TRUE)
summary(svm.linear)
#Training Error
ypred = predict(svm.linear, data.train)
table = table(predict = ypred, truth = data.train$Purchase)
confusionMatrix(table)
#Test Error
ypred=predict(svm.linear,data.test)
table = table(predict = ypred, truth = data.test$Purchase)
confusionMatrix(table)

#Find optimal value for cost using tune
set.seed(1)
tune.out =tune(svm, Purchase~., data = data.train, kernel = "linear",ranges=list(cost=c(0.01, 0.03, .05, .07, .09, .1, .3, .5, .7, .9, 1, 5, 10)))
bestmod = tune.out$best.model
summary(bestmod)
#Training Error
ypred = predict(bestmod, data.train)
table = table(predict = ypred, truth = data.train$Purchase)
confusionMatrix(table)
#Test Error
ypred=predict(bestmod,data.test)
table = table(predict = ypred, truth = data.test$Purchase)
confusionMatrix(table)

#Radial Kernel
svm.radial = svm(Purchase~., data = data.train, kernel = "radial", cost = 0.01, scale = TRUE)
summary(svm.radial)
#Training Error
ypred = predict(svm.radial, data.train)
table = table(predict = ypred, truth = data.train$Purchase)
confusionMatrix(table)
#Test Error
ypred=predict(svm.radial,data.test)
table = table(predict = ypred, truth = data.test$Purchase)
confusionMatrix(table)
#Find optimal value for cost using tune
set.seed(1)
tune.out =tune(svm, Purchase~., data = data.train, kernel = "radial",ranges=list(cost=c(0.01, 0.03, .05, .07, .09, .1, .3, .5, .7, .9, 1, 5, 10)))
bestmod = tune.out$best.model
summary(bestmod)
#Training Error
ypred = predict(bestmod, data.train)
table = table(predict = ypred, truth = data.train$Purchase)
confusionMatrix(table)
#Test Error
ypred=predict(bestmod,data.test)
table = table(predict = ypred, truth = data.test$Purchase)
confusionMatrix(table)

#Polynomial Kernel
svm.poly = svm(Purchase~., data = data.train, kernel = "polynomial", cost = 0.01, degree = 2, scale = TRUE)
summary(svm.poly)
#Training Error
ypred = predict(svm.poly, data.train)
table = table(predict = ypred, truth = data.train$Purchase)
confusionMatrix(table)
#Test Error
ypred=predict(svm.poly,data.test)
table = table(predict = ypred, truth = data.test$Purchase)
confusionMatrix(table)
#Find optimal value for cost using tune
set.seed(1)
tune.out =tune(svm, Purchase~., data = data.train, kernel = "poly", degree = 2 ,ranges=list(cost=c(0.01, 0.03, .05, .07, .09, .1, .3, .5, .7, .9, 1, 5, 10)))
bestmod = tune.out$best.model
summary(bestmod)
#Training Error
ypred = predict(bestmod, data.train)
table = table(predict = ypred, truth = data.train$Purchase)
confusionMatrix(table)
#Test Error
ypred=predict(bestmod,data.test)
table = table(predict = ypred, truth = data.test$Purchase)
confusionMatrix(table)

