import mysql.connector
from tabulate import tabulate
import os
import datetime
import time

today1 = datetime.date.today().strftime("%m-%d-%Y")

current_datetime = datetime.datetime.now()

# Format the date and time in the desired pattern
today = current_datetime.strftime("%d %b %Y, %I:%M%p")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mobile"
)

cursor = conn.cursor()
def fetchall_myproduct(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    myresult = cursor.fetchall()
    return myresult
    return True
def my_product():
    cursor.execute("SELECT * FROM my_products")
    myresult = cursor.fetchall()
    data=[]
    for x in myresult:
        x=list(x)
        data.append(x)
        table = tabulate(data, headers=["#","Name","Model","Model ID","Manufacturer","Price","Qty",'date'], tablefmt="fancy_grid")
        os.system('clear')
    print(table)

while True:
    print("+===========================+")
    print("1:MY PRODUCTS\n2:PRODUCT ENTRY\n3:SELL PRODUCT\n4:PURCHASE PRODUCT\n5:DAY BOOK\n6:MONTHLY REPORT\n7:Over All Information\n8:Cash Book\n9:Credit Book\n10:Edit\n11:Delete\n12:Quit")
    print("+===========================+")

    choice = int(input("Enter your choice: "))

    if choice == 12:
        print("BY BY!!")
        break

    elif choice == 2:
        date = today
        product_name = input("Enter the Product Name: ")
        model = input("Enter the Product Model: ")
        model_id= int(input('Enter the model id: '))
        id_unique = False
        result = fetchall_myproduct('my_products')
        for i in result:
            if model_id == i[3]:
                print("Alerady model_id Avalible\nTry a Unique Model ID")
                exit()
        price = int(input("Enter the Product Price: "))
        stock = int(input("Enter the stock Quantity: "))

        if price >0 and stock >=0:
            manufacture = input("Enter the Product Manufacture: ")
            query = "INSERT INTO my_products  ( name, model,model_id, manufacturer, stock_price, stock_qty,date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query, (product_name,model,model_id,manufacture,price,stock,date))
            conn.commit()
            query = "INSERT INTO stock_buy  ( name, model,model_id, manufacturer, stock_price, qty,date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(query, (product_name,model,model_id,manufacture,price,stock,date))
            conn.commit()
            os.system('clear')

            print("+============================+")
            print("|  Product added successfully  |")
            print("+============================+\n")
        else:
            os.system('clear')
            print("Invalid price or stock Quantity\nStock Entery Fail!!")
    elif choice == 1:
        my_product()

    elif choice ==4:
        found = False
        my_product()
        model_id = int(input("Enter the model ID of mobile that you want to purchase:"))
        data =fetchall_myproduct("my_products")
        for x in data:
            if x[3] == model_id:
                date = today
                name = x[1]
                model = x[2]
                model_id = x[3]
                manufacturer = x[4]
                stock_price = x[5]
                qty = x[6]
                imei1 = int(input("Enter the IMEI#1:"))
                imei2 = int(input("Enter the IMEI#2:"))
                product_conditon = input('Enter the mobile conditon new or used:')
                purchasing_price = int(input("Enter the purchasing price:"))
                conditon_m = False
                if product_conditon == 'new':
                    query = "INSERT INTO purchase_new  ( name, model,model_id, manufacturer, stock_price, purchase_p,imei_1,imei_2,condition_p,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(query, (name,model,model_id,manufacturer,stock_price,purchasing_price,imei1,imei2,'new',date))
                    conn.commit()
                    os.system('clear')
                    qty = x[6]+1
                    query="UPDATE `my_products` SET `stock_qty`=%s WHERE model_id=%s"
                    cursor.execute(query, (qty,model_id))
                    conn.commit()
                    print("+===============================+")
                    print("|  Product purchased successfully  |")
                    print("+===============================+\n")

                elif product_conditon == 'used':
                    query = "INSERT INTO purchase_used  ( name, model,model_id, manufacturer, stock_price, purchase_p,imei_1,imei_2,condition_p,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(query, (name,model,model_id,manufacturer,stock_price,purchasing_price,imei1,imei2,'used',date))
                    conn.commit()
                    os.system('clear')
                    qty = x[6]+1
                    query="UPDATE `my_products` SET `stock_qty`=%s WHERE model_id=%s"
                    cursor.execute(query, (qty,model_id))
                    conn.commit()
                    print("+===============================+")
                    print("|  Product purchased successfully  |")
                    print("+===============================+\n")
                else:
                    print('Invalid PRODUCT conditon!! ')



                found = True
        if not found:
            print(f'{model_id} not match with any model_id')

    elif choice ==3:
        data1=[]
        data = fetchall_myproduct('my_products')
        os.system("clear")
        for x in data:
            # data1.append(x)
            total = x[6]
            purchase_data = fetchall_myproduct('purchase_new')
            sum_new = 0
            for i in purchase_data:
                if i[3] == x[3] and i[11]>0:
                    sum_new += i[11]
                    # data1.append(str(sum_new))
            total_new = sum_new
            purchase_data =fetchall_myproduct('purchase_used')
            sum_used = 0
            for i in purchase_data:
                if i[3] ==x[3] and i[11]>0:
                    sum_used += i[11]
                    # data1.append(str(sum_used))
            total_used = sum_used

            total_new = sum_new
            purchase_data =fetchall_myproduct('stock_buy')
            sum_stock = 0
            for i in purchase_data:
                if i[3] ==x[3] and i[-2]>0:
                    sum_stock += i[-2]
                    data1.append([x[0],x[1],x[2],x[3],x[4],x[5],x[6],sum_stock,sum_new,sum_used ])
                    table = tabulate(data1, headers=["#","Name","Model","Model ID","Manufacturer","Price","Total Qty","Stock","New","Used"], tablefmt="fancy_grid")
        os.system('clear')
        print(table)
        chose = int(input("Enter  the Model_ID of mobile that you want to Sell:"))
        data1=[]
        data = fetchall_myproduct('my_products')
        os.system("clear")
        found = False
        for x in data:

            if chose == x[3]:
                if x[6] >0:
                    cho = input("Enter the Mbile conditon(stock,used,new):")
                    if cho == 'stock':
                        purchase_data =fetchall_myproduct('stock_buy')
                        stock = False
                        data2 = []
                        for i in purchase_data:

                            if chose == i[3] and i[6]>0:
                                data2.append(i)
                                stock = True
                        table = tabulate(data2, headers=["#","Name","Model","Model ID","Manufacturer","Price","Stock",'date'], tablefmt="fancy_grid")
                        os.system('clear')
                        print(table)
                        data3 =data2[0]
                        name = data3[1]
                        model = data3[2]
                        model_id =data3[3]
                        manufacturer = data3[4]
                        original_price = data3[5]
                        selling_price = int(input("Enter the Mobile Selling Price:"))
                        imei1 = int(input('Enter the Mobile IMEI#1:'))
                        imei2 = int(input('Enter the Mobile IMEI#2:'))
                        stock_qty =int(data3[6])-1
                        purchasing_date = data3[7]
                        total_qty = int(x[6])-1
                        selling_date = today
                        query = "INSERT INTO stock_sell ( name, model,model_id, manufacturer, original_price, selling_price,imei_1,imei_2,condition_sell,purchasing_date,selling_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(query, (name,model,model_id,manufacturer,original_price,selling_price,imei1,imei2,'stock',purchasing_date,selling_date))
                        conn.commit()

                        query=" UPDATE `my_products` SET `stock_qty`=%s WHERE model_id = %s"
                        cursor.execute(query, (total_qty,model_id))
                        conn.commit()
                        query=" UPDATE `stock_buy` SET `qty`=%s WHERE model_id = %s"
                        cursor.execute(query, (stock_qty,model_id))
                        conn.commit()
                        os.system('clear')
                        print("+===============================+")
                        print("|  Product sold successfully  |")
                        print("+===============================+\n")
                        # stock = True
                        if not stock:
                            print('No Stock Avalible')



                    elif cho == 'new':
                        purchase_data =fetchall_myproduct('purchase_new')
                        stock = False
                        data2 = []
                        for i in purchase_data:

                            if chose == i[3] and i[6]>0:
                                data2.append(i[0:10])
                                print(i[0:10])
                                stock = True
                                table = tabulate(data2, headers=["#","Name","Model","Model ID","Manufacturer","Original Price",'PURCHASE Price',"IMEI#1","IMEI#2","Condition","date","qty"], tablefmt="fancy_grid")
                        os.system('clear')

                        print(table)
                        purchase_data =fetchall_myproduct('purchase_new')
                        stock = False
                        data =[]
                        number = int(input("Enter the mobile number that you want to  sell:"))
                        for i in purchase_data:
                            if  number == i[0] and i[6]>0:
                                data3 = i[0]
                                name = i[1]
                                model = i[2]
                                model_id =x[3]
                                manufacturer = i[4]
                                original_price = i[5]
                                purchase_price =i[6]
                                selling_price = int(input("Enter the Mobile Selling Price:"))
                                imei1 = i[7]
                                imei2 = i[8]
                                stock_qty =int(i[11])-1
                                purchasing_date = i[10]
                                total_qty = int(x[6])-1
                                selling_date = today
                                print(data3, name,model,model_id,imei1,imei2,stock_qty,total_qty,purchasing_date)
                                query = "INSERT INTO sell_new ( name, model,model_id, manufacturer, original_price,purchase_price, selling_price,imei_1,imei_2,condition_sell,purchasing_date,selling_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                cursor.execute(query, (name,model,model_id,manufacturer,original_price,purchase_price,selling_price,imei1,imei2,'new',purchasing_date,selling_date))
                                conn.commit()

                                query=" UPDATE `my_products` SET `stock_qty`=%s WHERE model_id = %s"
                                cursor.execute(query, (total_qty,model_id))
                                conn.commit()
                                query=" UPDATE `purchase_new` SET `qty`=%s WHERE imei_1 = %s"
                                cursor.execute(query, (stock_qty,imei1))
                                conn.commit()
                                os.system('clear')
                                print("+===============================+")
                                print("|  Product sold successfully  |")
                                print("+===============================+\n")



                                stock = True
                        if not stock:
                            print('No Stock Avalible')

                    elif cho == 'used':
                        purchase_data =fetchall_myproduct('purchase_used')
                        stock = False
                        data2 = []
                        for i in purchase_data:

                            if chose == i[3] and i[6]>0:
                                data2.append(i[0:10])
                                print(i[0:10])
                                stock = True
                                table = tabulate(data2, headers=["#","Name","Model","Model ID","Manufacturer","Original Price",'PURCHASE Price',"IMEI#1","IMEI#2","Condition","date","qty"], tablefmt="fancy_grid")
                        os.system('clear')

                        print(table)
                        purchase_data =fetchall_myproduct('purchase_used')
                        stock = False
                        data =[]
                        number = int(input("Enter the mobile number that you want to  sell:"))
                        for i in purchase_data:
                            if  number == i[0] and i[6]>0:
                                data3 = i[0]
                                name = i[1]
                                model = i[2]
                                model_id =x[3]
                                manufacturer = i[4]
                                original_price = i[5]
                                purchase_price =i[6]
                                selling_price = int(input("Enter the Mobile Selling Price:"))
                                imei1 = i[7]
                                imei2 = i[8]
                                stock_qty =int(i[11])-1
                                purchasing_date = i[10]
                                total_qty = int(x[6])-1
                                selling_date = today
                                print(data3, name,model,model_id,imei1,imei2,stock_qty,total_qty,purchasing_date)
                                query = "INSERT INTO sell_used ( name, model,model_id, manufacturer, original_price,purchase_price, selling_price,imei_1,imei_2,condition_sell,purchasing_date,selling_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                cursor.execute(query, (name,model,model_id,manufacturer,original_price,purchase_price,selling_price,imei1,imei2,'used',purchasing_date,selling_date))
                                conn.commit()

                                query=" UPDATE `my_products` SET `stock_qty`=%s WHERE model_id = %s"
                                cursor.execute(query, (total_qty,model_id))
                                conn.commit()
                                query=" UPDATE `purchase_used` SET `qty`=%s WHERE imei_1 = %s"
                                cursor.execute(query, (stock_qty,imei1))
                                conn.commit()
                                os.system('clear')
                                print("+===============================+")
                                print("|  Product sold successfully  |")
                                print("+===============================+\n")



                                stock = True
                        if not stock:
                            print('No Stock Avalible')


                    found = True
        if not found:
            print('No mobile Avalible of this model_id')
    elif choice == 5:
        today_date = datetime.datetime.now().strftime("%d %b %Y")

        cursor.execute("SELECT * FROM stock_sell")
        sold_mobiles = cursor.fetchall()
        cursor.execute("SELECT * FROM sell_new")
        new_mobiles = cursor.fetchall()
        cursor.execute("SELECT * FROM sell_used")
        used_mobiles = cursor.fetchall()
        data =[]
        total_profit = 0
        total_loss = 0
        for stock in sold_mobiles:
            date = stock[-1].split(',')
            if date[0] == today_date:
                data.append(list(stock))
        for used in used_mobiles:
            date = used[-1].split(',')
            if date[0]== today_date:
                data.append(list(used))
        for new in new_mobiles:
            date = new[-1].split(',')
            if date[0]== today_date:
                data.append(list(new))
        day_book_purchased = []
        for x in data:
            if x[10] == 'new' or x[10] =='used':
                profit_or_loss =int(x[7]) - int(x[6])
                no,name,model,manufacture,original_price,sell,ime1,imei2,condition,sell_date,profit_or_loss =x[0],x[1],x[2],x[4],x[6],x[7],x[8],x[9],x[10],x[12],profit_or_loss
                day_book_purchased.append([name,model,manufacture,original_price,sell,ime1,imei2,condition,sell_date,profit_or_loss])
            elif x[9] == 'stock':
                print(x)
                profit_or_loss =int(x[6]) - int(x[5])
                print(profit_or_loss)
                no,name,model,manufacture,original_price,sell,ime1,imei2,condition,sell_date,profit_or_loss =x[0],x[1],x[2],x[4],x[5],x[6],x[7],x[8],x[9],x[11],profit_or_loss
                day_book_purchased.append([name,model,manufacture,original_price,sell,ime1,imei2,condition,sell_date,profit_or_loss])
        os.system('clear')

        print("+=============================================================+")
        print("DAY BOOK - MOBILES Sell TODAY")
        print("+=============================================================+")
        print(tabulate(day_book_purchased, headers=["Name", "Model", "Manufacturer","Original Price", "Sell Price", "IMEI#1", "IMEI#2","Condition","Date","profit_loss"], tablefmt="fancy_grid"))
        print("+=============================================================+\n")
        overall_total_profit = sum(entry[-1] for entry in day_book_purchased if entry[-1] > 0)
        overall_total_loss = sum(entry[-1] for entry in day_book_purchased if entry[-1] < 0)
        print("+=============================================================+")

        print("Overall Total Profit:", overall_total_profit)
        print("Overall Total Loss:", overall_total_loss)

        print("+=============================================================+")



        today_date = datetime.datetime.now().strftime("%d %b %Y")

        cursor.execute("SELECT * FROM stock_buy")
        sold_mobiles = cursor.fetchall()
        cursor.execute("SELECT * FROM purchase_new")
        new_mobiles = cursor.fetchall()
        cursor.execute("SELECT * FROM purchase_used")
        used_mobiles = cursor.fetchall()
        data =[]
        total_profit = 0
        total_loss = 0
        for stock in sold_mobiles:
            date = stock[-1].split(',')
            if date[0] == today_date:
               data.append([stock[0],stock[1],stock[2],stock[3],stock[4],stock[5],stock[6],stock[7], "N/A", "stock"])
        for used in used_mobiles:
            date = used[-2].split(',')
            if date[0]==today_date:
                data.append(list(used))
        for new in new_mobiles:
            date = new[-2].split(',')
            if date[0]== today_date:
                data.append(list(new))
        day_book_purchased = []
        for x in data:
            if x[9] == 'new' or x[9] =='used':
               no,name,model,manufacture,original_price,sell,imei1,imei2,condition,sell_date =x[0],x[1],x[2],x[4],x[5],x[6],x[7],x[8],x[9],x[10]
               day_book_purchased.append([name,model,manufacture,original_price,sell,imei1,imei2,condition,sell_date])
            elif x[9] == 'stock':
                print(x)
                no,name,model,manufacture,original_price,imei1,imei2,condition,purchase_date=x[0],x[1],x[2],x[4],x[5],"N/A","N/A",x[9],x[7]
                day_book_purchased.append([name,model,manufacture,original_price,original_price,imei1,imei2,condition,purchase_date])
        print("+=============================================================+")
        print("DAY BOOK - MOBILES PURCHASE TODAY")
        print("+=============================================================+")
        print(tabulate(day_book_purchased, headers=["Name", "Model", "Manufacturer","Original Price", "Purchase Price", "IMEI#1", "IMEI#2","Condition","Date",], tablefmt="fancy_grid"))
        print("+=============================================================+\n")

    elif choice == 6:
         current_month = datetime.datetime.now().strftime("%b")
         current_year = datetime.datetime.now().strftime("%Y")
         cursor.execute("SELECT * FROM stock_buy")
         sold_mobiles = cursor.fetchall()
         cursor.execute("SELECT * FROM purchase_new")
         new_mobiles = cursor.fetchall()
         cursor.execute("SELECT * FROM purchase_used")
         used_mobiles = cursor.fetchall()
         data = []

         for stock in sold_mobiles:
             date = stock[-1].split(',')
             day, month, year = date[0].strip().split()
             if month == current_month and year == current_year:
                  data.append([stock[0],stock[1],stock[2],stock[3],stock[4],stock[5],stock[6],stock[7], "N/A", "stock"])


         for used in used_mobiles:
             date = used[-2].split(',')
             day, month, year = date[0].strip().split()
             if month == current_month and year == current_year:
                 data.append(list(used))

         for new in new_mobiles:
            date = new[-2].split(',')
            if month == current_month and year == current_year:
                data.append(list(new))
         day_book_purchase = []
         for x in data:
             if x[9] == 'new' or x[9] =='used':
                 no,name,model,manufacture,original_price,sell,imei1,imei2,condition,sell_date =x[0],x[1],x[2],x[4],x[5],x[6],x[7],x[8],x[9],x[10]
                 day_book_purchase.append([name,model,manufacture,original_price,sell,imei1,imei2,condition,sell_date])
             elif x[9] == 'stock':
                 no,name,model,manufacture,original_price,imei1,imei2,condition,purchase_date=x[0],x[1],x[2],x[4],x[5],"N/A","N/A",x[9],x[7]
                 day_book_purchase.append([name,model,manufacture,original_price,original_price,imei1,imei2,condition,purchase_date])
         os.system('clear')

         print("+=============================================================+")
         print("MONTHLY REPORT - MOBILES PURCHASED THIS MONTH")
         print("+=============================================================+")
         print(tabulate(day_book_purchase, headers=["Name", "Model", "Manufacturer","Original Price", "Purchase Price", "IMEI#1", "IMEI#2","Condition","Date",], tablefmt="fancy_grid"))
         print("+=============================================================+\n")

         cursor.execute("SELECT * FROM stock_sell")
         sold_mobiles = cursor.fetchall()
         cursor.execute("SELECT * FROM sell_new")
         new_mobiles = cursor.fetchall()
         cursor.execute("SELECT * FROM sell_used")
         used_mobiles = cursor.fetchall()
         data =[]
         total_profit = 0
         total_loss = 0
         for stock in sold_mobiles:
             date = stock[-1].split(',')
             day, month, year = date[0].strip().split()
             if month == current_month and year == current_year:
                 data.append(list(used))

         for used in used_mobiles:
            date = used[-2].split(',')
            day, month, year = date[0].strip().split()
            if month == current_month and year == current_year:
                data.append(list(used))
         for new in new_mobiles:
             date = new[-2].split(',')

             day, month, year = date[0].strip().split()
             if month == current_month and year == current_year:
                 data.append(list(new))
         day_book_purchased = []
         for x in data:
             if x[10] == 'new' or x[10] =='used':
                 profit_or_loss =int(x[7]) - int(x[6])
                 no,name,model,manufacture,original_price,sell,ime1,imei2,condition,sell_date,profit_or_loss =x[0],x[1],x[2],x[4],x[6],x[7],x[8],x[9],x[10],x[12],profit_or_loss
                 day_book_purchased.append([name,model,manufacture,original_price,sell,ime1,imei2,condition,sell_date,profit_or_loss])
             elif x[9] == 'stock':
                 print(x)
                 profit_or_loss =int(x[6]) - int(x[5])
                 print(profit_or_loss)
                 no,name,model,manufacture,original_price,sell,ime1,imei2,condition,sell_date,profit_or_loss =x[0],x[1],x[2],x[4],x[5],x[6],x[7],x[8],x[9],x[11],profit_or_loss
                 day_book_purchased.append([name,model,manufacture,original_price,sell,ime1,imei2,condition,sell_date,profit_or_loss])
        # os.system('clear')

         print("+=============================================================+")
         print("MONTHLY REPORT - MOBILES SOLD THIS MONTH")
         print("+=============================================================+")
         print(tabulate(day_book_purchased, headers=["Name", "Model", "Manufacturer","Original Price", "Sell Price", "IMEI#1", "IMEI#2","Condition","Date","profit_loss"], tablefmt="fancy_grid"))
         print("+=============================================================+\n")
         overall_total_profit = sum(entry[-1] for entry in day_book_purchased if entry[-1] > 0)
         overall_total_loss = sum(entry[-1] for entry in day_book_purchased if entry[-1] < 0)
         print("+=============================================================+")

         print("Overall Total Profit:", overall_total_profit)
         print("Overall Total Loss:", overall_total_loss)

         print("+=============================================================+")

    elif choice == 8:
        enetry = int(input("1:View Cash Book\n2:New Entry\nEnter your Choice: "))
        if enetry ==  2:
            os.system('clear')
            print("+=============================================================+")
            print("Cash Book Entry")
            print("+=============================================================+\n")
            title = input("Enter the title: ")
            inout = int(input("1:Cash In\n2:Cash Out\nEnter choice: "))
            amount = int(input("Enter the Amount: "))
            date = today
            if inout == 1:
                query= "INSERT INTO `cash`(`title`, `cash_in`, `cash_out`, `amount`, `date`) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(query, (title,'cash_in','N/A',amount,date))
                conn.commit()
                print("+=============================================================+")
                print("Cash Book Entry successful")
                print("+=============================================================+\n")
            elif inout == 2:
                query= "INSERT INTO `cash`(`title`, `cash_in`, `cash_out`, `amount`, `date`) VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(query, (title,'N/A','cash_out',amount,date))
                conn.commit()
                print("+=============================================================+")
                print("Cash Book Entry successful")
                print("+=============================================================+\n")

        elif enetry ==1:
            os.system('clear')
            print("+=============================================================+")
            print("                           Cash Book                          ")
            print("+=============================================================+\n")
            cursor.execute("SELECT * FROM cash")
            myresult = cursor.fetchall()
            data=[]
            for i in myresult:
                no,title,cash_in,cash_out,amount,date=i[0],i[1],i[2],i[3],i[4],i[5]
                data.append([no,title,cash_in,cash_out,amount,date])
            print(tabulate(data, headers=["#","Title","Cash In","Cash Out","Amount","Date"], tablefmt="fancy_grid"))
            print("+=============================================================+\n")
            cursor.execute("SELECT SUM(amount) FROM cash WHERE cash_in='cash_in'")
            sum_cash_in = cursor.fetchone()[0]
            print("profit:", sum_cash_in)
            cursor.execute("SELECT SUM(amount) FROM cash WHERE  cash_out='cash_out'")
            sum_cash_out= cursor.fetchone()[0]
            print("loss:", sum_cash_out)

    elif choice ==9:
        os.system('clear')
        entry = int(input("1:View Credit Book\n2:Credit Book Entry\nEnter your choice: "))
        if entry == 2:
            os.system('clear')

            print("+=============================================================+")
            print("|                       Credit Book Entry                     |      ")
            print("+=============================================================+\n")

            name = input("Enter a name: ")
            title = input("Enter a title: ")
            category = int(input("1:Receivable\n2:Payable\nEnter a choicce: "))
            amount = int(input("Enter the amount:"))
            issue_date = today1
            due_date =  input("Enter the Due Date(MM-DD-YYYY):")
            if category == 1:
                query=" INSERT INTO `credit`(`name`, `title`, `issue`, `due`, `receivable`,`remaning`) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, (name,title,issue_date,due_date,amount,amount))
                conn.commit()
                os.system('clear')
                print("+=============================================================+")
                print("|                 Credit Book Entry successful                |      ")
                print("+=============================================================+\n")
            elif category == 2:
                query=" INSERT INTO `credit`(`name`, `title_p`, `p_issue`, `p_due`, `payable`,`remaning_p`) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, (name,title,issue_date,due_date,amount,amount))
                conn.commit()
                os.system('clear')
                print("+=============================================================+")
                print("|                 Credit Book Entry successful                |      ")
                print("+=============================================================+\n")


        elif entry ==1:
            cursor.execute("SELECT * FROM credit")
            myresult = cursor.fetchall()
            data=[]
            total_r =0
            total_p =0
            total_dr =0
            total_dp =0
            all_r =0
            all_p =0
            for i in myresult:
                no,name,title,issue,due,receivable,payable,p_issue,p_due=i[0],i[1],i[2],i[3],i[4],i[10],i[11],i[14],i[14]

                if due == today1  :
                    today_r,today_p,def_r,def_p,totl_r,totl_p=receivable,payable,0,0,receivable,payable
                    data.append([no,name,today_r,today_p,def_r,def_p,totl_r,totl_p])
                    total_r +=today_r
                    total_p += today_p
                    total_dr += def_r
                    total_dp += def_p
                    all_r += totl_r
                    all_p +=totl_p

                elif due!=today1 and due > today1 :
                    today_r,today_p,def_r,def_p,totl_r,totl_p=0,0,0,0,receivable,payable
                    data.append([no,name,today_r,today_p,def_r,def_p,totl_r,totl_p])
                    total_r +=today_r
                    total_p += today_p
                    total_dr += def_r
                    total_dp += def_p
                    all_r += totl_r
                    all_p +=totl_p

                elif due!=today1 and due < today1 :
                    today_r,today_p,def_r,def_p,totl_r,totl_p=0,0,receivable,payable,receivable,payable
                    data.append([no,name,today_r,today_p,def_r,def_p,totl_r,totl_p])
                    total_r +=today_r
                    total_p += today_p
                    total_dr += def_r
                    total_dp += def_p
                    all_r += totl_r
                    all_p +=totl_p

            print(tabulate(data, headers=["#","Name","Today Receivable","Today Payable","Defaulted Receivable","Defaulted Payable","Overall Receivable","Overall Payable"], tablefmt="fancy_grid"))
            print("+=============================================================================================+")
            print("Today Receivable:",total_r,"\tDefaulted Receivable:",total_dr,"\tOverall Receivable:",all_r,)
            print("------------------------------------------------------------------------------------------------")
            print("Today Payable:",total_p,"\tDefaulted Payable:",total_dp,"\tOverall Payable:",all_p)
            print("+=============================================================================================+\n")
            edi = input("Do you want to edit any user(y/n):")
            os.system('clear')
            if edi == 'y':
                print(tabulate(data, headers=["#","Name","Today Receivable","Today Payable","Defaulted Receivable","Defaulted Payable","Overall Receivable","Overall Payable"], tablefmt="fancy_grid"))
                print("+=============================================================+\n")
                nu = int(input("Enter the no of the user:"))
                cursor.execute("SELECT * FROM credit")
                myresult = cursor.fetchall()
                for i in myresult:
                    if i[0] == nu:
                        os.system('clear')
                        # print("+===============================================================================================+")
                        print("Today Receivable:",total_r,"\tDefaulted Receivable:",total_dr,"\tOverall Receivable:",all_r,"\n")
                        print("Today Payable:",total_p,"\tDefaulted Payable:",total_dp,"\tOverall Payable:",all_p,"")
                        # print("+==================================================================================================+")
                        print("+=====================================================+")
                        print(f'|Receivable\t\t\t\t{i[5]}      |\n|{i[2]}|\n|Remaning:{i[10]}\t\t\t\t      |\n|-----------------------------------------------------|\n|Issue Date:{i[3]}\t\tDue Date:{i[4]}   |')
                        print("+=====================================================+\n")

                        if i[9]!= None:
                            print("\t\t\t\t\t\t\t+=====================================================+")
                            received = int(i[5]) -int(i[10])
                            print("\t\t\t\t\t\t\t"f'|Received\t\t\t\t{received}             |\n\t\t\t\t\t\t\t|{i[9]}|\n\t\t\t\t\t\t\t|-----------------------------------------------------|\n\t\t\t\t\t\t\t|Issue Date:{i[3]}\t\tDue Date:{i[4]}   |')
                        # print("\t\t\t\t\t\t\t+=====================================================+\n")
                        print("+=====================================================+")
                        print(f'|payable\t\t\t\t{i[6]}      |\n|{i[12]}|\n|Remaning:{i[11]}\t\t\t\t\t  |\n|-----------------------------------------------------|\n|Issue Date:{i[3]}\t\tDue Date:{i[4]}   |')
                        print("+=====================================================+\n")

                        if i[13]!= None:
                            print("\t\t\t\t\t\t\t+=====================================================+")
                            payed = int(i[6]) -int(i[11])
                            print("\t\t\t\t\t\t\t"f'|Payed\t\t\t\t{payed}             |\n\t\t\t\t\t\t\t|{i[13]}|\n\t\t\t\t\t\t\t|-----------------------------------------------------|\n\t\t\t\t\t\t\t|Issue Date:{i[3]}\t\tDue Date:{i[4]}   |')
                        choi = int(input("1:Receivable\n2:Payable\n3:Received\n4:Payed\n5:Cancel\nEnter your choice: "))
                        if choi ==1:
                            issue_date=today1

                            due_date =  input("Enter the Due Date(MM-DD-YYYY):")
                            amount = int(input("Enter the amount:"))
                            title = input("Enter the title:")
                            tota_amount = amount+i[10]
                            query = "UPDATE credit SET title=%s,issue=%s,due=%s,remaning=%s WHERE `#` =%s"
                            cursor.execute(query, ( f'{i[2]}|\n|{title}',issue_date,due_date,tota_amount, nu))
                            conn.commit()

                            print("+=============================================================+")
                            print("|                 Credit Book UPDATE successful                |      ")
                            print("+=============================================================+\n")


                        elif choi ==2:
                            issue_date=today1

                            due_date =  input("Enter the Due Date(MM-DD-YYYY):")
                            amount = int(input("Enter the amount:"))
                            title = input("Enter the title:")
                            tota_amount = amount+i[11]
                            query = "UPDATE credit SET title_p=%s,issue=%s,due=%s,remaning_p=%s WHERE `#` =%s"
                            cursor.execute(query, (f'{i[12]}\n{title}',issue_date,due_date,tota_amount, nu))
                            conn.commit()
                            os.system('clear')
                            print("+=============================================================+")
                            print("|                 Credit Book UPDATE successful                |      ")
                            print("+=============================================================+\n")
                            time.sleep(4)
                            os.system('clear')



                        elif choi ==3:
                            issue_date=i[3]

                            due_date =  i[4]
                            amount = int(input("Enter the amount:"))
                            title = input("Enter the title:")
                            tota_amount = i[10]-amount
                            query = "UPDATE credit SET title_r=%s,remaning=%s WHERE `#` =%s"
                            cursor.execute(query, (f'{i[9]}\n{title}',tota_amount, nu))
                            conn.commit()
                            os.system('clear')
                            print("+=============================================================+")
                            print("|                 Credit Book UPDATE successful                |      ")
                            print("+=============================================================+\n")
                            time.sleep(4)
                            os.system('clear')


                        elif choi ==4:
                            issue_date=i[3]

                            due_date =  i[4]
                            amount = int(input("Enter the amount:"))
                            title = input("Enter the title:")
                            tota_amount = i[11]-amount
                            query = "UPDATE credit SET title_pa=%s,remaning_p=%s WHERE `#` =%s"
                            cursor.execute(query, (f'{i[13]}\n{title}',tota_amount, nu))
                            conn.commit()
                            os.system('clear')
                            print("+=============================================================+")
                            print("|                 Credit Book UPDATE successful                |      ")
                            print("+=============================================================+\n")

    elif choice == 10:
        os.system('clear')
        ch = input("Enter your choice that you want to Edit((name,model,manufacturer,price):")
        cursor.execute("SELECT * FROM my_products")
        myresult = cursor.fetchall()
        data=[]
        for x in myresult:
            x=list(x)
            data.append(x)
        table = tabulate(data, headers=["#","Name","Model","Model ID","Manufacturer","Price","Qty","Date"], tablefmt="fancy_grid")
        os.system('clear')
        print(table)
        cho = int(input(f"Enter the model ID  of mobile whos {ch} you want to edit:"))
        cursor.execute("SELECT * FROM my_products")
        myresult = cursor.fetchall()
        data=[]
        find =  False
        for x in myresult:
            x=list(x)
            data.append(x)

            if cho ==x[3]:

                find = True
                os.system('clear')
                n_name = input(f"Enter the new {ch} of Your Product ")
                conform =  input(f"Are you sure to Edit {ch} from all Enteries where Model ID is {cho}(y/n)")
                if conform == 'y':
                    query=f" UPDATE `my_products` SET `{ch}`=%s WHERE model_id =%s"
                    cursor.execute(query, (n_name,cho))
                    conn.commit()

                    query=f"  UPDATE `purchase_new` SET `{ch}`=%s WHERE model_id =%s"
                    cursor.execute(query, (n_name,cho))
                    conn.commit()

                    query=f"UPDATE `purchase_used` SET `{ch}`=%s WHERE model_id =%s"
                    cursor.execute(query, (n_name,cho))
                    conn.commit()

                    query=f"UPDATE `sell_new` SET `{ch}`=%s WHERE model_id =%s"
                    cursor.execute(query, (n_name,cho))
                    conn.commit()

                    query=f"UPDATE `sell_used` SET `{ch}`=%s WHERE model_id =%s"
                    cursor.execute(query, (n_name,cho))
                    conn.commit()


                    query=f"UPDATE `stock_buy` SET `{ch}`=%s WHERE model_id =%s"
                    cursor.execute(query, (n_name,cho))
                    conn.commit()

                    query=f"  UPDATE `stock_sell` SET `{ch}`=%s WHERE model_id =%s"
                    cursor.execute(query, (n_name,cho))
                    conn.commit()
                    os.system("clear")
                    print("+=================================================+")
                    print(f"{ch} UPDATED successful from all Enteries")
                    print("+=================================================+")



        if not find:
            os.system('clear')
            print("+=================================================+")
            print(f"No ANY Mobile Avalible of this Model ID:{cho}")
            print("+================================================ =+")

    elif choice == 11:
        os.system('clear')
        cursor.execute("SELECT * FROM my_products")
        myresult = cursor.fetchall()
        data=[]
        for x in myresult:
            x=list(x)
            data.append(x)
        table = tabulate(data, headers=["#","Name","Model","Model ID","Manufacturer","Price","Qty","Date"], tablefmt="fancy_grid")
        os.system('clear')
        print(table)
        delete = int(input("Enter the Model ID of mobile that you want to delete from all Enteries:"))

        cursor.execute("SELECT * FROM my_products")
        myresult = cursor.fetchall()
        find =  False
        for x in myresult:
            x=list(x)

            if delete ==x[3]:
                find = True
                os.system('clear')
                print(f"The mobile that you want to delete\nName:{x[1]}\nModel:{x[2]}\nManufacturer:{x[4]}\nPrice:{x[5]}")
                confom = input("Are you sure to Delete this mobile from all Enteries(y/n):")
                if confom == 'y':
                   query = "DELETE FROM `my_products` WHERE model_id =%s"
                   cursor.execute(query, (x[3],))
                   conn.commit()

                   query = "DELETE FROM `purchase_new` WHERE model_id =%s"
                   cursor.execute(query, (x[3],))
                   conn.commit()

                   query = "DELETE FROM `purchase_used` WHERE model_id =%s"
                   cursor.execute(query, (x[3],))
                   conn.commit()

                   query = "DELETE FROM `sell_new` WHERE model_id =%s"
                   cursor.execute(query, (x[3],))
                   conn.commit()

                   query = "DELETE FROM `sell_used` WHERE model_id =%s"
                   cursor.execute(query, (x[3],))
                   conn.commit()

                   query = "DELETE FROM `stock_buy` WHERE model_id =%s"
                   cursor.execute(query, (x[3],))
                   conn.commit()

                   query = "DELETE FROM `stock_sell` WHERE model_id =%s"
                   cursor.execute(query, (x[3],))
                   conn.commit()
                   os.system('clear')
                   print("+=================================================+")
                   print("Product Deleted Successful")
                   print("+=================================================+")

        if not find:
            os.system("clear")
            print("+=================================================+")
            print(f"NO Any Mobile Avalible of this model id:{delete} ")
            print("+=================================================+")

    elif choice == 7:
        os.system('clear')
        print("+=============================================================+")
        print("OVERALL INFORMATION - MOBILES AVAILABLE")

        print("+=============================================================+\n")
        new = fetchall_myproduct('purchase_new')
        used = fetchall_myproduct('purchase_used')

        sell_new =  fetchall_myproduct('sell_new')

        sell_used = fetchall_myproduct('sell_used')

        price_new = 0
        price_used = 0
        sum_used =0
        sum_new = 0
        find = False
        for i in new:
            sum_new +=i[-1]
            if i[-1]>0:
                price_new +=i[6]
                find = True
        print("Total Number of Available New Mobiles:",sum_new)
        print("Total Price of Available New Mobiles:", price_new)
        if not find:
             print("No New Mobiles Available")

        print("+-------------------------------------------------------------+")

        found = False
        for j in used:
            sum_used +=j[-1]
            if j[-1]>0:
                found = True
                price_used +=j[6]

        print("Total Number of Available Used Mobiles:",sum_used)
        print("Total Price of Available New Mobiles:", price_used)

        if not find:
            print("No New Mobiles Available")

        print("+-------------------------------------------------------------+")
