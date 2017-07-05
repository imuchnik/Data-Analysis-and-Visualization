############################################################################
###                    Analysis of Lending Club Data                    ####
###          Generates Various CSV files for Data Visualization          ###
############################################################################

#Setup
setwd("C:/Users/mirik/Desktop")

#Read the data
loans = read.csv("C:/Users/mirik/Desktop/loandata.csv")
attach(loans)

#View variables  
names(loans)

#Generate dataset: frequency table for loan purpose
purpose.freq = table(purpose)
rel.purpose.freq = purpose.freq / nrow(loans)
write.csv(rel.purpose.freq, file = "Frequency_Purpose.csv")


#Generate dataset: interest rates and grade
df.rates.grades = data.frame(int_rate, grade)
write.csv(df.rates.grades, file = "Rates_Grades.csv")