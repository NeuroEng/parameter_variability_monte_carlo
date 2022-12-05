install.packages("xtable")

library(xtable)

## Load data, remove non-converging rows, scale all variables
dat.full <- read.csv("sim_results.csv")[,-1]
dat <- subset(dat.full, tri_error!=999.0 | bi_error!=999.0 | kin_error != 999.0)
dat.scale <- as.data.frame(scale(dat))

##########################################
## Regression models with main effects for bi error
g1 <- lm(bi_error~., data=dat.scale[,-c(29,31)])
summary(g1)
# print out sorted coefficient table
xtable(round(summary(g1)$coefficients[order(summary(g1)$coefficients[,4]),],4))

## Regression models with main effects for tri error
g1 <- lm(tri_error~., data=dat.scale[,-c(30,31)]) #data=subset(dat.scale,bi_error<0.88)[,-30])
summary(g1)
# print out sorted coefficient table
xtable(round(summary(g1)$coefficients[order(summary(g1)$coefficients[,4]),],4))

###########################################
## Interaction effect models
## bi error
g2 <- lm(bi_error~.^2, data=dat.scale[,-c(29,31)])
summary(g2)
# print out sorted coefficient table
xtable(round(summary(g2)$coefficients[order(summary(g2)$coefficients[,4]),],4))

## tri error
g2 <- lm(tri_error~.^2, data=dat.scale[,-c(30,31)])
summary(g2)
# print out sorted coefficient table
xtable(round(summary(g2)$coefficients[order(summary(g2)$coefficients[,4]),],4))











