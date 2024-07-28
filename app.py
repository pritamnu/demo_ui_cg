import streamlit as st
import random
from PIL import Image
import os
import matplotlib.pyplot as plt

# module imports
import moderate


# Function to submit the review
def submit_review(product, review, rating, moderated):
    if 'reviews' not in st.session_state:
        st.session_state.reviews = []
    if moderated:
        results = moderate.moderate(review)
    else:
        results = {}
    st.session_state.reviews.append({'product': product, 'review': review, 'rating': rating, 'scores': results})


# Load product images
image_folder = 'images'  # Path to the folder containing product images
image_files = [f for f in os.listdir(image_folder) if f.endswith(('png', 'jpg', 'jpeg'))]

if 'current_image' not in st.session_state:
    st.session_state.current_image = random.choice(image_files)

# Streamlit app
st.title('Product Review Posting App')

st.header('Submit a Review')

# Display random product image
current_image_path = os.path.join(image_folder, st.session_state.current_image)
image = Image.open(current_image_path)
st.image(image, caption=st.session_state.current_image)

review_text = st.text_area('Review')
rating = st.slider('Rating', 1, 5, 3)
enable_moderation = st.checkbox('Enable Moderation')

if st.button('Submit'):
    if review_text:
        moderated = enable_moderation
        submit_review(st.session_state.current_image, review_text, rating, moderated)
        st.success('Review submitted successfully!')
        # Load a new random image
        st.session_state.current_image = random.choice(image_files)
    else:
        st.error('Please enter the review text.')

st.header('Reviews')
if 'reviews' in st.session_state and st.session_state.reviews:
    for review in st.session_state.reviews:
        print(review)
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write('Rating:', '⭐' * review['rating'])
            st.write(review['review'])
        if review.get('scores') and review['scores']:
            with col2:
                # Bar chart for scores
                scores = review['scores']['scores']
                categories = list(scores.keys())
                values = list(scores.values())
                plt.style.use('dark_background')

                fig, ax = plt.subplots(figsize=(1, 1))
                ax.barh(categories, values, color=['red', 'orange', 'green', 'purple'])
                ax.set_xlabel('Score')
                ax.set_title('Review Scores')
                for index, value in enumerate(values):
                    ax.text(value, index, f'{value:.2f}')
                st.pyplot(fig)
        else:
            with col2:
                st.write('No Moderation Applied')
        st.write('---')

else:
    st.write('No reviews yet.')
