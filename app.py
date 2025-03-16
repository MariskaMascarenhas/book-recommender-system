from flask import Flask, render_template, request
import pickle
import numpy as np

# Load data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input').strip().lower()  # Normalize input

    # Ensure case-insensitive match
    index_array = np.where(pt.index.str.lower() == user_input)[0]

    # If book is not found, show an error message
    if len(index_array) == 0:
        return render_template('recommend.html', data=[], error="⚠️ Book not found! Please check the title.")

    index = index_array[0]  # Safe access

    # Get similar books
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'].str.lower() == pt.index[i[0]].lower()]
        if not temp_df.empty:
            data.append([
                temp_df['Book-Title'].values[0],
                temp_df['Book-Author'].values[0],
                temp_df['Image-URL-M'].values[0]
            ])

    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
