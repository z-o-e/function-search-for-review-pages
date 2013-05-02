# loade data
data<-read.table("/Users/zoe/Desktop/alldata.csv",sep=",",header=T)
summary(data)


# calculate total sample size
# set 1/3 of samples to be test set
# set the rest for training
sample_size=nrow(data)
train_size=sample_size-floor(sample_size/3)


# set up training set and test set
set.seed(45)
shuffled_index=sample.int(sample_size,size=sample_size,replace=FALSE)
train=data[shuffled_index[1:train_size],]
test=data[-shuffled_index[1:train_size],]


# boxplot to see distribution of the predictors
par(mfrow=c(3,2))
for(i in c(3:8))
{
  boxplot(data[,i], at = 1, xaxt = "n", xlim = c(0, 4), main = colnames(data)[i])
  boxplot(test[,i], at = 2, xaxt = "n", add = TRUE)
  boxplot(train[,i], at = 3, xaxt = "n", add = TRUE)
  axis(1, at = 1:3, labels = c("Original", "Test", "Train"), tick = TRUE)
}
par(mfrow = c(1,1))


# function score.table()
# inputs:
#       p---prediction
#       r---actual
# output:
#       table---classification results
#
score.table <- function(p, r, threshold = 0.5)
{
  TH <- p > threshold
  Pred <- rep(0, length(TH))
  Pred[TH] <- 1
  Actual <- r
  cat("Predicted vs. Actual", fill = T)
  table(Pred, Actual)
}


# perform logistic regression on training set
train_model<-glm(label~domain+url.keywords+first.person+punctuation+html.keywords+voting.link.tag,
                 data=train, family=binomial)
summary(train_model)
fit_model<-predict(train_model, type="response")

# see training result
score.table(fit_model, train$label)
plot(fit_model, train$label,pch=21, main="logistic regression on trainig set",
     xlab="Posterior", ylab="Actual")

# fit the test set
fit_test<-predict(train_model, newdata=test, type="response")

# see model performance on test set
score.table(fit_test,test$label)
plot(fit_test, test$label, pch=21, main="logistic regression on test set",
     xlab="Posterior", ylab="Actual")


# gradient boost with gbm
library(gbm)

# 10 iterations
train_model_gbm10<-gbm(label~domain+url.keywords+first.person+punctuation+html.keywords+voting.link.tag,
                     data=train,n.trees=10, shrinkage=0.1)
summary(train_model_gbm10)
fit_test_gbm10<-predict(train_model_gbm10, newdata=test, n.trees=10,type="response")
summary(fit_test_gbm10)


# 20 iterations
train_model_gbm20<-gbm(label~domain+url.keywords+first.person+punctuation+html.keywords+voting.link.tag,
                       data=train,n.trees=20, shrinkage=0.1)
summary(train_model_gbm20)
fit_test_gbm20<-predict(train_model_gbm20, newdata=test, n.trees=20,type="response")
summary(fit_test_gbm20)


# 30 iterations
train_model_gbm30<-gbm(label~domain+url.keywords+first.person+punctuation+html.keywords+voting.link.tag,
                       data=train,n.trees=30, shrinkage=0.1)
summary(train_model_gbm30)
fit_test_gbm30<-predict(train_model_gbm30, newdata=test, n.trees=30,type="response")
summary(fit_test_gbm30)


# 50 iterations
train_model_gbm50<-gbm(label~domain+url.keywords+first.person+punctuation+html.keywords+voting.link.tag,
                       data=train,n.trees=50, shrinkage=0.1)
summary(train_model_gbm50)
fit_test_gbm50<-predict(train_model_gbm50, newdata=test, n.trees=50,type="response")
summary(fit_test_gbm50)


# 80 itersations
train_model_gbm80<-gbm(label~domain+url.keywords+first.person+punctuation+html.keywords+voting.link.tag,
                       data=train,n.trees=80, shrinkage=0.1)
summary(train_model_gbm80)
fit_test_gbm80<-predict(train_model_gbm80, newdata=test, n.trees=80,type="response")
summary(fit_test_gbm80)


# function plot.roc(), lines.roc()
# inputs:
#       p---prediction
#       r---actual
# output:
#       plot---classification results
#
plot.roc  <- function(p, r, main = "ROC Curve", col = 4)
{
  tp <- truepos(p, r)
  tn <- trueneg(p, r)
  plot(1-tn, tp,  type = "n", main = main,
       xlab = "False Positive", ylab = "True Positive")
  lines(1-tn, tp, col = col, lwd =2)
  abline(0, 1)
}

lines.roc  <- function(p, r, main = "ROC Curve", col)
{
  tp <- truepos(p, r)
  tn <- trueneg(p, r)
  lines(1-tn, tp, col = col, lwd =2)
}

truepos  <- function(p, r)
{
  threshold <- seq(0, 1, .01)
  if (is.logical(r))
    apply((apply(sapply(p, '>=', threshold), 1, '&',
                 sapply(r, '==', T))), 2, sum)/sum(r == T)
  else 
    apply((apply(sapply(p, '>=', threshold), 1, '&',
                 sapply(as.factor(r), '==', levels(as.factor(r))[2]))), 2, sum)/sum(as.factor(r)   	== levels(as.factor(r))[2])
}

trueneg  <- function(p, r)
{
  threshold <- seq(0, 1, .01)
  if (is.logical(r))
    apply((apply(sapply(p, '<=', threshold), 1, '&',
                 sapply(r, '==', F))), 2, sum)/sum(r == F)
  else 
    apply((apply(sapply(p, '<=', threshold), 1, '&',
                 sapply(as.factor(r), '==', levels(as.factor(r))[1]))), 2, sum)/sum(as.factor(r) 		== levels(as.factor(r))[1])
}        


# score table
score.table(fit_test_gbm10,test$label)
score.table(fit_test_gbm30,test$label)
score.table(fit_test_gbm80,test$label)

# plot ROC curves
plot.roc(fit_test_gbm10,test$label,main="Gradient Boost")
lines.roc(fit_test_gbm20,test$label,col="red2")
lines.roc(fit_test_gbm30,test$label,col="green")
lines.roc(fit_test_gbm50,test$label,col="orange")
lines.roc(fit_test_gbm80,test$label,col="yellow")
legend(.6,.8, legend=c("10 iter","20 iter","30 iter","50 iter","100 iter"),
       col=c("blue","red2","green","orange","yellow"))

score.table(fit_test_gbm80,test$label)
