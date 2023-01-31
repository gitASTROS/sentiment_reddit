
import streamlit as st
import plotly.graph_objects as go
from nltk.sentiment import SentimentIntensityAnalyzer
import praw






# Create a function to get comments from a subreddit
#@st.cache
def get_subreddit_comments(subreddit_name, num_comments=1000):
    reddit = praw.Reddit(client_id=st.secrets('client_id'), 
                         client_secret=st.secrets('client_secret'),
                         username=st.secrets('username'), 
                         password=st.secrets('password'), 
                         user_agent=st.secrets('user_agent'))
    subreddit = reddit.subreddit(subreddit_name)
    comments = []
    for comment in subreddit.comments(limit=num_comments):
        comments.append(comment.body)
    return comments

# Create a function to classify the sentiment of the comments
#@st.cache
def classify_sentiment(comments):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    for comment in comments:
        sentiment = analyzer.polarity_scores(comment)['compound']
        sentiments.append(sentiment)
    return sentiments

def main():
    st.title('Reddit Sentiment Analysis')
    st.markdown('By Sebvaldez')
    subreddit_name = st.text_input('Enter the subreddit name:','XRP')
    num_comments = st.number_input('Enter the number of comments to analyze:', min_value=1, max_value=1000)
    comments = get_subreddit_comments(subreddit_name, num_comments)
    sentiments = classify_sentiment(comments)

    # Create a pie chart to visualize the sentiment
    positive = len([x for x in sentiments if x > 0])
    negative = len([x for x in sentiments if x < 0])
    neutral = len([x for x in sentiments if x == 0])
    fig = go.Figure(data=[go.Pie(labels=['Positive', 'Negative', 'Neutral'],
                                 values=[positive, negative, neutral])])
    fig.update_layout(title_text='Sentiment Analysis Results')
    st.plotly_chart(fig)

if __name__ == '__main__':
    main()
