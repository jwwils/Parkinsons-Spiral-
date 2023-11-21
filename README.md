
# Improving Parkinson's Disease Prediction Models with the Novel "Lift" Variable

## Abstract

This project explores the integration of a novel variable, "lift," into machine learning models for predicting Parkinson's disease using spiral drawing tests. The lift variable quantifies the frequency of pen lifts during the test. The aim is to assess how this new variable can enhance model accuracy and compare its effectiveness against other variables.

## Introduction

Early detection of Parkinson's disease is crucial for effective disease management. This project leverages handwriting and drawing tasks, specifically spiral sketching, to diagnose Parkinson's disease, focusing on variables like speed, pen-pressure, and the newly introduced "lift" metric.

## Methods

### Data Sets
- **UCI Machine Learning Dataset**: Spiral drawings classified into control and Parkinson's groups.
- **Zham et al. (2017) Dataset**: Focuses on time and pressure during the spiral test, including 15 control and 25 Parkinson's images.

### Exploratory Data Analysis
- Examination of Parkinson's and control group features.
- Statistical tests to understand data correlations and variable significance.
- Mann-Whitney U test to assess the significance of the "lift" variable.

### Feature Engineering and Selection
- Engineering new variables: lift, symmetry, area, length, and smoothness.
- Correlation analysis and decision tree models to identify crucial variables.
- Random forest and ANOVA tests for feature significance.

## Machine Learning Models and Results
- Implementation of logistic regression, random forest, SVM, KNN, neural network, and GBM.
- Model evaluation using accuracy, precision, F1 score, and AUC.
- Highlighting the impact of the "lift" variable on model performance.

## Further Work
- Development of an application for real-time Parkinson's prediction.
- Addressing challenges in data capture and processing.
- Potential for integration into digital health platforms.

## Conclusion
- The project underscores the significance of the lift variable in Parkinson's disease prediction.
- Future research directions include expanding data sets and combining lift with other motor activity data.

