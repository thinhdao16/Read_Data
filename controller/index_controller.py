import os
import csv
from itertools import islice

def get_csv_path():
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, '..', 'data', 'Reviews.csv')

def load_reviews(page: int, page_size: int = 15):
    reviews_path = get_csv_path()
    start = (page - 1) * page_size
    end = start + page_size

    with open(reviews_path, 'r', encoding='utf-8') as csvfile:
        valid_lines = (line for line in csvfile if not line.strip().startswith('//'))
        reader = csv.DictReader(valid_lines)
        return list(islice(reader, start, end))

_total_reviews = None

def count_reviews():
    global _total_reviews
    if _total_reviews is not None:
        return _total_reviews

    with open(get_csv_path(), 'r', encoding='utf-8') as csvfile:
        valid_lines = (line for line in csvfile if not line.strip().startswith('//'))
        next(valid_lines, None)
        _total_reviews = sum(1 for _ in valid_lines)
        return _total_reviews
    
def update_review(review_id, updated_data):
    reviews_path = get_csv_path()

    with open(reviews_path, 'r', encoding='utf-8') as f:
        valid_lines = [line for line in f if not line.strip().startswith('//')]
        reader = list(csv.DictReader(valid_lines))
        fieldnames = reader[0].keys()
        

    found = False
    for idx, row in enumerate(reader):
        if str(row.get("Id")) == str(updated_data["Id"]):
            # Giữ nguyên các field không được gửi từ form
            updated_row = {field: updated_data.get(field, row[field]) for field in fieldnames}
            reader[idx] = updated_row
            found = True
            break

    if not found:
        raise ValueError(f"Review with Id {review_id} not found.")

    with open(reviews_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reader)



def delete_review_controller(review_id, delete_data):
    reviews_path = get_csv_path()
    with open(reviews_path, 'r', encoding='utf-8') as f:
        valid_lines = (line for line in f if not line.strip().startswith('//'))
        reader = list(csv.DictReader(valid_lines))
        if review_id < 1 or review_id > len(reader):
            raise ValueError("Invalid review ID")
        # Delete the review from the listk
        del reader[review_id - 1]
        # Get the fieldnames (if there are any reviews left)
        fieldnames = reader[0].keys() if reader else []
    with open(reviews_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reader)
        
def remove_duplicate_reviews():
    reviews_path = get_csv_path()

    with open(reviews_path, 'r', encoding='utf-8') as f:
        valid_lines = (line for line in f if not line.strip().startswith('//'))
        reader = list(csv.DictReader(valid_lines))
        if not reader:
            return  # file trống thì thôi

        fieldnames = reader[0].keys()

    seen_ids = set()
    unique_reviews = []

    for row in reader:
        row_id = row.get('Id')
        if row_id not in seen_ids:
            seen_ids.add(row_id)
            unique_reviews.append(row)

    with open(reviews_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(unique_reviews)
