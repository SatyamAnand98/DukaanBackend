def modify_input_for_product_model(productName, description, MRP, image, sp, category):
    dict = {}
    dict['productName'] = productName
    dict['description'] = description
    dict['MRP'] = MRP
    dict['image'] = image
    dict['SP'] = sp
    dict['category'] = category
    return dict

def modify_input_for_category_model(category, product_id=None):
    dict = {}
    dict["category"] = category
    dict["product_id"] = product_id