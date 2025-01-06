def extract_product_engagement(row):
    is_active, n_products = row['IsActiveMember'], row['NumOfProducts']
    
    if is_active == 0:
        return 'very_low_engagment'
    elif is_active == 1 and n_products == 1:
        return 'small_engagment'
    elif is_active == 1 and n_products == 2:
        return 'avg_engagment'
    elif is_active == 1 and n_products == 3:
        return 'above_avg_engagment'
    elif is_active == 1 and n_products == 4:
        return 'high_engagment'
