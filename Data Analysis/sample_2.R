#Libraries
library("ISLR")
library(caret)


#STEP A
#Data
attach(OJ)
fix(OJ)
set.seed(1) 
train = sample(nrow(OJ), 800, replace = FALSE) 
test = -train 
data.train = data.frame(OJ[train,])
data.test = data.frame(OJ[test,])
data.test.x = data.test[,-1]
data.test.y = Purchase[test]

#STEP B - CREATE TREE
tree.oj.train = tree(Purchase~., data.train)
summary(tree.oj.train)
#There are 8 terminal nodes. The predictors used are LoyalCH, PriceDiff, SpecialCH, and ListPriceDiff.
#The misclassification error rate is .165

#STEP C - PICK ONE NODE TO INTERPRET
tree.oj.train
#Interpret node:  7) LoyalCH > 0.764572 278   86.14 CH ( 0.96403 0.03597 ) *
#This node represents: all instances where LoyalCH is greater than .764572
#There are 278 such instances, of which .96403 are CH, and only .03597 are MM.
#The classification for this node is CH.
#The deviance for this branch is 86.14


#STEP D - PLOT THE TREE
plot(tree.oj.train)
text(tree.oj.train, pretty=0)
#Interpretation of results: based on this plot, we see clearly that LoyalCH is the variable that provides
#the most information gain. We see this since the data is initially split on that variable,
#and then further splits are still based on that variable. 
#Furthermore, we note that this decision tree seems reasonably balanced.
#It results in 8 terminal nodes that classify instances as MM or CH.

#STEP E - PREDICTIONS AND TABLE
tree.pred=predict(tree.oj.train, data.test, type = "class")
summary(tree.pred)
oj.table = table(tree.pred, data.test.y)
print(oj.table)
(49+12)/(147+49+12+62)
#The test error rate is .223

#STEP F - CV.TREE TO DETERMINE OPTIMAL TREE SIZE
cv.oj=cv.tree(tree.oj.train, FUN=prune.misclass)

#STEP G - PLOT TREE SIZE VS ERROR
par(mfrow=c(1,2))
plot(cv.oj$size,cv.oj$dev, type="b")
print(cv.oj$dev)
print(cv.oj)

#STEP H
#Optimal size - no difference between 5 and 8, so let's do 5 since smaller
#The cv error rate for 5 and 8 nodes is 153

#STEP I - CREATE PRUNED TREE
prune.oj = prune.misclass(tree.oj.train, best = 5)


#STEP J - TRAINING ERROR BETWEEN PRUNED AND UNPRUNED TREES
summary(tree.oj.train)
#Misclassification error rate: 0.165 = 132 / 800 
summary(prune.oj)
#Misclassification error rate: 0.165 = 132 / 800 
#They have the same training error rate!


#STEP K - TESTING ERROR BETWEEN PRUNED AND UNPRUNED TREES
print(oj.table)
(49+12)/(147+49+12+62)
#Pruned tree
tree.pred2=predict(prune.oj, data.test, type = "class")
summary(tree.pred2)
oj.table2 = table(tree.pred2, data.test.y)
print(oj.table2)
(12+49)/(147+49+12+62)
#They have the same testing error rate of .226