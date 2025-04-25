# liver-cirrhosis-stage-prediction-project

## Overview
This project focuses on exploratory data analysis (EDA) for a dataset related to liver cirrhosis patients. The goal is to understand the data structure, identify patterns, and prepare the dataset for building predictive models to classify the stage of liver cirrhosis.

## Dataset
The dataset used is sourced from Kaggle, titled **"Cirrhosis Prediction Dataset"**. It includes various clinical and demographic features such as:
- **Numerical variables**: Age, Albumin, Bilirubin, etc.
- **Categorical variables**: Gender, Drug type, Cirrhosis Stage (target variable).

## Key Steps Performed
1. **Data Loading & Initial Exploration**: Examined dataset shape, data types, and missing values.
2. **Data Cleaning**: Handled missing values, renamed columns, and corrected inconsistencies.
3. **Univariate Analysis**: Explored distributions of numerical and categorical variables.
4. **Bivariate/Multivariate Analysis**: Investigated relationships between features and the target variable.
5. **Correlation Analysis**: Identified significant correlations using a heatmap.
6. **Outlier Detection**: Analyzed and treated outliers in key features.
7. **Missing Value Treatment**: Applied imputation or deletion strategies.
8. **Feature Engineering**: (If applicable) Created derived features like binned age or binary indicators.

## Findings
- Lab test variables (e.g., Albumin, Bilirubin) strongly correlate with cirrhosis stages.
- Stage 4 (Severe cirrhosis) exhibits distinct patterns compared to earlier stages.
- Some features had high missing values, requiring careful handling.

## Recommendations
- Use feature selection or dimensionality reduction techniques.
- Normalize/standardize numerical features before modeling.
- Address class imbalance in the target variable if present.

## Repository Structure
- `liver_cirrhosis.csv`: Raw dataset (not included; available on Kaggle).
- `EDA_Report.pdf`: Detailed exploratory analysis report.
- `scripts/`: (Optional) Code for data cleaning, visualization, and analysis.

## How to Use
1. Download the dataset from Kaggle and place it in the project directory.
2. Review the EDA report (`EDA_Report.pdf`) for insights.
3. (Optional) Run provided scripts to reproduce analyses or extend the work.

## Author
**Eman Abdallah Yosif Maharik**  
Dataset Source: [Kaggle - Cirrhosis Prediction Dataset](https://www.kaggle.com/datasets/...)

Link of deployment: [https://liver-cirrhosis-stage-prediction-project.streamlit.app/]
