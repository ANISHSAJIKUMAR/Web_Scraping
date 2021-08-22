from csv import DictReader

with open('good_reads_books_dataset.csv', 'r', encoding='utf-8') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        print(row['bookID'], row['title'])