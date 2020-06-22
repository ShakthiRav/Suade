import csv
import datetime

def getReport(input):

    promoted_prod_id = set()
    promotion_ids = set()
    customer_ids =set()
    order_vendor_pairs = {}
    commissions = {}

    item_cnt =0
    customer_cnt =0
    order_total =0
    discount_total =0
    no_discount_total =0
    total_commisions =0
    total_promoted_commissions =0

    try:
        entered_date = datetime.datetime.strptime(input, '%Y-%m-%d').date()
    except:
        return "Invalid input. Please input a valid date of the form YYYY-MM-DD"

    with open('data/orders.csv', newline='', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:

            date = datetime.datetime.strptime(str(row[1]), '%Y-%m-%d %H:%M:%S.%f').date()
            if date == entered_date:
                order_vendor_pairs[row[0]] = row[2]
                customer_ids.add(row[3])

    with open('data/product_promotions.csv', newline='', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:

            date = datetime.datetime.strptime(str(row[0]), '%Y-%m-%d').date()
            if date == entered_date:
                promotion_ids.add(row[2])
                promoted_prod_id.add(row[1])

    with open('data/commissions.csv', newline='', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:

            date = datetime.datetime.strptime(str(row[0]), '%Y-%m-%d').date()
            if date == entered_date:
                commissions[row[1]] = row[2]



    if len(order_vendor_pairs.keys()) == 0:
        return "No records of any orders were found for this day"

    with open('data/order_lines.csv', newline='', encoding = 'utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:

            if row[0] in order_vendor_pairs.keys():
                item_cnt += int(row[6])
                no_discount_total +=float(row[7])
                discount_total += float(row[8])
                order_total +=float(row[10])

                added_commission = float(row[10]) * float(commissions[  order_vendor_pairs[row[0]]  ])
                total_commisions += added_commission


                if row[1] in promoted_prod_id:
                    total_promoted_commissions +=added_commission

    # Discount rates are calculated prior to VAT additions

    # Commissions are applied to VAT as well

    # When calculating average commision per promotion
    # only commisions from products that were promoted are considered

    report = f""" 
    number of items: {item_cnt} 
    number of customers: {len(customer_ids)} 
    total discount (£): {round(no_discount_total -  discount_total,2)} 
    average discount rate before VAT (%): {round((no_discount_total -  discount_total)/no_discount_total *100,2)}
    average order_total (£): {round(order_total/len(order_vendor_pairs.keys()),2)}
    commissions total (£): {round(total_commisions,2)} 
    commissions per order (£): {round(total_commisions /len(order_vendor_pairs.keys()) ,2)} 
    commissions total from promoted products (£): {round (total_promoted_commissions,2 )} 
    average promoted product commisions per promotion scheme run (£): {
        round(total_promoted_commissions/max(len(promotion_ids),1),2)}
    """
    return report 



if __name__ == "__main__":
    print(getReport("2019-09-28"))