from flask import Blueprint, render_template, request, jsonify
import math
from controller.index_controller import load_reviews, count_reviews, update_review, delete_review_controller

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    page = int(request.args.get('page', 1))
    per_page = 15

    # Load reviews cho trang hiện tại
    reviews = load_reviews(page=page, page_size=per_page)

    # Đếm tổng số reviews
    total_reviews = count_reviews()
    total_pages = math.ceil(total_reviews / per_page)

    # Xác định khoảng phân trang hiển thị
    start = max(1, page - 2)
    end = min(total_pages, page + 2)

    return render_template('index.html',
                           reviews=reviews,
                           page=page,
                           per_page=per_page,
                           start=start,
                           end=end,
                           total_pages=total_pages)


@index_bp.route('/detail/<int:review_id>')
def detail(review_id):
    # Load all reviews (or optimize to load only the required one)
    reviews = load_reviews(page=1, page_size=count_reviews())
    if review_id < 1 or review_id > len(reviews):
        return "Review not found", 404

    review = reviews[review_id - 1]  # Adjust for 0-based index
    return render_template('detail.html', review=review)

@index_bp.route('/api/reviews/<int:review_id>', methods=['POST'])
def edit_review(review_id):
    updated_data = request.form.to_dict()
    try:
        update_review(review_id, updated_data)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@index_bp.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    delete_data = request.form.to_dict()
    try:
        delete_review_controller(review_id,delete_data)
        return jsonify({'success': True})
    except ValueError as ve:
        return jsonify({'success': False, 'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
