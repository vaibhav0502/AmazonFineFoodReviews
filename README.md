# Amazon Fine Food Review Sentiment Analysis

## 1.Business Problem:

### 1.1 Description
1. [Dataset is taken from Kaggle](https://www.kaggle.com/snap/amazon-fine-food-reviews)
2. This dataset consists of reviews of fine foods from amazon. The data span a period of more than 10 years, including all ~500,000 reviews up to October 2012. Reviews include product and user information, ratings, and a plain text review. It also includes reviews from all other Amazon categories.

### 1.2 Problem Statemtent:
To determine whether a review is positive or negative and build a machine learning model around it.

## 2.Dataset:

### 2.1 Data includes:
- Reviews from Oct 1999 - Oct 2012
- 568,454 reviews
- 256,059 users
- 74,258 products
- 260 users with > 50 reviews

### 2.2 Columns:
1. Id
2. ProductId - Unique identifier for the product
3. UserId - Unqiue identifier for the user
4. ProfileName - Profile name of user
5. HelpfulnessNumerator - Number of users who found the review helpful
6. HelpfulnessDenominator - Number of users who indicated whether they found the review helpful or not
7. Score - Rating between 1 and 5
8. Time - Timestamp for the review
9. Summary - Brief summary of the review
10. Text - Text of the review

## 3.Text Preprocessing:
- Convert everything to lowercase
- Remove HTML tags
- Remove URL from sentence
- Contraction mapping
- Eliminate punctuations and special characters
- Remove stopwords
- Remove short words

## 4.Evaluation:

![Capture](https://user-images.githubusercontent.com/42543380/224705315-5f9dde68-e295-4943-8a17-6312ee3ff638.PNG)


## FrontEnd
![Capture](https://user-images.githubusercontent.com/42543380/224711680-2918236a-6217-48d1-8e78-b9d8fe72507a.PNG)


