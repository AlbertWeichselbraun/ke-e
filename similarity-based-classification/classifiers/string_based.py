def string_classify_document(document, keyword_list):
    document_lower = document.lower()

    # Count the number of keywords within the document
    return sum([document_lower.count(keyword.lower()) for keyword in keyword_list])
