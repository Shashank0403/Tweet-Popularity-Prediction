import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
file_path = 'tweet_dataset.csv'
df = pd.read_csv(file_path, encoding='latin1')

# Convert tweet texts to lowercase
df['text'] = df['text'].str.lower()

# Initialize the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit the vectorizer on the dataset
tfidf_matrix = tfidf_vectorizer.fit_transform(df['text'])

def predict_likes(tweet_text):
    # Convert the input tweet text to lowercase
    tweet_text = tweet_text.lower()

    # Remove the '#' symbol if present
    tweet_text = tweet_text.replace('#', '')

    # Transform the input tweet text into a TF-IDF vector
    input_tweet_vector = tfidf_vectorizer.transform([tweet_text])

    # Calculate cosine similarity between the input tweet and all tweets in the dataset
    similarities = cosine_similarity(input_tweet_vector, tfidf_matrix)

    # Find the indices of matching tweets in the dataset
    matching_indices = similarities.argsort()[0][::-1]

    # Calculate the average likes for matching tweets
    total_likes = 0
    count = 0
    for idx in matching_indices:
        if tweet_text in df.loc[idx, 'text']:  # Check if the input tweet text exactly matches
            total_likes += df.loc[idx, 'likes']
            count += 1
            if count >= 5:
                break

    # Calculate the average likes for matching tweets
    predicted_likes = total_likes / count if count > 0 else 0

    return predicted_likes

def main():
    st.title("Tweet Likes Predictor")

    tweet_text = st.text_input("Enter your tweet:")

    if st.button("Predict Likes"):
        predicted_likes = predict_likes(tweet_text)
        st.success(f"Predicted likes for your tweet: {predicted_likes:.2f}")

if __name__ == "__main__":
    main()
