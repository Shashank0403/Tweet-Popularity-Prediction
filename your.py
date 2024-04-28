import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from firebase_admin import firestore

# Initialize Firestore DB
db = firestore.client()

# Load the dataset
file_path = 'tweet_dataset.csv'
df = pd.read_csv(file_path, encoding='latin1')

# Convert tweet texts to lowercase
df['text'] = df['text'].str.lower()

# Initialize the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit the vectorizer on the dataset
tfidf_matrix = tfidf_vectorizer.fit_transform(df['text'])

def convert_likes_to_int(likes_str):
    if likes_str.isdigit():
        return int(likes_str)
    elif likes_str.endswith('K'):
        return int(float(likes_str[:-1]) * 1000)
    elif likes_str.endswith('M'):
        return int(float(likes_str[:-1]) * 1000000)
    else:
        return 0  # Return 0 for unrecognized formats

def format_likes(likes_int):
    if likes_int >= 1000000:
        return f"{likes_int / 1000000:.1f}M"
    elif likes_int >= 1000:
        return f"{likes_int / 1000:.1f}K"
    else:
        return str(likes_int)

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
    tweets_info = []
    total_likes = 0
    for idx in matching_indices:
        if tweet_text in df.loc[idx, 'text']:
            likes_str = df.loc[idx, 'likes']
            likes_int = convert_likes_to_int(likes_str)
            total_likes += likes_int
            tweet_info = {
                'text': df.loc[idx, 'text'],
                'likes': likes_str,
                'image': df.loc[idx, 'image'],
                'info': df.loc[idx, 'info']
            }
            tweets_info.append(tweet_info)

    formatted_total_likes = format_likes(total_likes)
    return tweets_info, formatted_total_likes

def delete_post(username, content, index):
    try:
        db.collection('Posts').document(username).update({"Content": firestore.ArrayRemove([content[index]])})
        st.warning('Post deleted')
    except:
        st.write('Something went wrong..')

def app():
    if 'username' not in st.session_state or st.session_state.username == '':
        st.markdown("<h3 style='font-size:70px;'><b>Please Login first</b></h3>", unsafe_allow_html=True)
        return

    try:
        st.title('User: '+st.session_state['username'])
    except:
        st.text('An error occurred while fetching posts.')

    st.title("Tweet Likes Predictor")
    tweet_text = st.text_input("Enter your tweet:")
    if st.button("Predict Likes"):
        if not tweet_text:  # Check if the input is empty
            st.info("Please type something.")  # Display a message if the input is empty
        else:
            tweets_info, total_likes = predict_likes(tweet_text)
            st.success(f"Total likes for matched tweets: {total_likes}")
            if tweets_info:
                for tweet_info in tweets_info:
                    st.write(f"Likes: {tweet_info['likes']}")
                    st.write(f"Info: {tweet_info['info']}")
                    try:
                        st.image(tweet_info['image'], caption=tweet_info['text'], use_column_width=True)
                    except Exception as e:
                        st.error(f"An error occurred when displaying the image: {e}")
            else:
                st.info("No matching tweets found.")

if __name__ == "__main__":
    app()
