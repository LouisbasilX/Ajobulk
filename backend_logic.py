import os
import shutil
from datetime import datetime

path = "database_folder"
files = {"organizations.csv": "org_id,name,created_date\n",
          "members.csv":"member_id,fullname,phone_number,date_registered\n",
          "stocks.csv":"stock_id,org_id,product_name,target_quantity,estimated_price,contributed_amount\n",
          "stock_contributions.csv": "contribution_id,stock_id,member_id,amount_paid,quantity_due,last_updated\n",
          "settings.csv": "id,biz_name,terms,backup_path,export_path\n"
}

#helper functions

# shortform path joiner
def p(filename):
    return os.path.join(path, filename) 

#shortform directory creator
def create_new_folder(path):
     os.makedirs(path, exist_ok=True)
     
#short form time
def time():
     return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

#initiate a non existent db file
def init_file(filename, content):
    filepath = p(filename)
    if not os.path.exists(filepath):
         with open(filepath, mode="w", encoding="utf-8") as file:
               file.write(content)
               print(f"file {filename} created successfully")
    else:
         print(f"file {filename} already exists")

#append to an existing db_file
def append_to_file(filename, content):
    filepath = p(filename)
    with open(filepath, mode="a", encoding="utf-8") as file:
               file.write(content)
               print(f"file {filename} updated")

def overwrite_file(filename, content):
    with open(p(filename), mode="w", encoding="utf-8") as file:
            file.write(content)
            print(f"file {filename} overwritten") 

#read a db_file
def read_file(filename):
     with open(p(filename), mode='r') as f:
          rows = f.read().splitlines()
     header = rows[0]
     records = rows[1:]

     return {"header": header, "records": records}     

# Fix a missing db file by backing up the current db and reseting it
def fix_missing_db_file(filename):
    filepath = p(filename)
    if not os.path.exists(path) or not os.path.exists(filepath): 
         back_up_database(False)
         init_database()
    else: return

# loop through an existing db_file and get the next usable id
def get_new_id(filename):
    fix_missing_db_file(filename)

    with open(p(filename), mode="r") as f:
         rows = f.read().splitlines()
    usable_rows = rows[1:]   
    if(len(usable_rows) == 0): return '1'  
    largest_id = usable_rows[-1].split(',')[0]

    return f"{int(largest_id) + 1}"    

def get_record(filename, id):
     fix_missing_db_file(filename)
     content = read_file(filename)
     header = content['header'].split(',')
     records = content['records']
     if len(records) == 0: return {}
     for record in records:
          record_list = record.split(',')
          record_id = record_list[0]
          if record_id == id:
               res = {}
               for i in range(len(header)):
                    res[header[i]] = record_list[i]
               return res 
     return {}       



def update_record(filename,id,new_value):
     fix_missing_db_file(filename)
     content = read_file(filename)
     header = content['header'].split(',')
     records = content['records']
     
     if len(header) != len(new_value.split(',')):
          print("Error Invalid row")
          return
   
     if len(records) == 0: return 

     for i in range(len(records)):
          record_list = records[i].split(',')
          record_id = record_list[0]
          if record_id == id:
              records[i] = new_value
              new_record = f"{content['header']}\n{'\n'.join(records)}\n"
              overwrite_file(filename, new_record)      

def delete_record(filename, id):
     content = read_file(filename)
     records = content['records']
     for record in records:
          record_list = record.split(',')
          record_id = record_list[0]
          if record_id == id:
              records.remove(record)
              new_record = f"{content['header']}\n{'\n'.join(records)}"
              overwrite_file(filename, new_record) 
              break

def add_record(filename, new_record):
     fix_missing_db_file(filename)
     content = read_file(filename)
     header = content['header'].split(',')
     if len(header) != len(new_record.split(',')):
          print("Error Invalid row")
          return
     append_to_file(filename, new_record)

def get_all_records(filename):
     fix_missing_db_file(filename)
     content = read_file(filename)
     res = []
     for record in content['records']:
          record_id = record.split(',')[0]
          res.append(get_record(filename, record_id))
     return res 


# Setup & Settings Zone
def init_database():
  create_new_folder("database_folder")
  for filename, header in files.items():
      init_file(filename, header)
  append_to_file(f"settings.csv", "1,untitled,no terms,backup_folder,export_folder\n")    


def reset_database():
    for filename in files:
        filepath = p(filename)
        if os.path.exists(filepath):
           os.remove(filepath)
           print(f"{filename} deleted successfully")
        else:
           print(f"{filename} is already deleted")
    init_database()

def back_up_database(state):
    settings = get_record('settings.csv', '1')
    back_up_folder = settings['backup_path']
    create_new_folder(back_up_folder)
    time_stamp = time()
    back_up_type = "Missing_File_Backups" if not state else "Normal_Backups"
    backup_path = os.path.join(back_up_folder, back_up_type, f"{back_up_type}_{time_stamp}")
    create_new_folder(backup_path)
    for file in files:
         if os.path.exists(p(file)):
              shutil.copy2(p(file), os.path.join(backup_path, file))
              print(f"Successfully backed up {file}")
         else: print(f"missing {file} file. Backup Failed")   


     
     
      
             







# Dashboard view functions

#add organization function
def add_organization(name):
     new_id = get_new_id("organizations.csv")
     date_created = time()
     orgs = get_all_records("organizations.csv")
     for org in orgs:
          if name == org['name']:
               return 'Error Organization already exists'
     
     add_record('organizations.csv', f"{new_id},{name},{date_created}\n")
     return 'Organization added successfully'


#get dashboard metrics function
def get_dashboard_metrics():
     org_length = len(read_file("organizations.csv")['records'])
     stock_length = len(read_file("stocks.csv")['records'])
     members_length = len(read_file("members.csv")['records'])

     return {"ORGANIZATIONS": org_length, "ACTIVE BULKS": stock_length, "MEMBERS": members_length}

def edit_org_name(org_id, new_name):
     current_record = get_record("organizations.csv", org_id)
     new_record = f"{org_id},{new_name},{current_record['created_date']}"
     update_record("organizations.csv", org_id, new_record)

#delete organization
def delete_organization(org_id):
     org_stocks = get_org_stocks(org_id)
     stock_ids = [stock['stock_id'] for stock in org_stocks]

     for stock_id in stock_ids:
          delete_stock(stock_id)
     delete_record("organizations.csv", org_id)     




# Organization View Functions
def add_stock(name, org_id,target_qunatity,estimated_price ):
     new_id = get_new_id("stocks.csv")
     stocks = get_all_records("stocks.csv")
     for stock in stocks:
          if org_id == stock['org_id'] and name == stock['product_name']:
               return 'Error Stock name already exists'
     
     add_record('stocks.csv', f'{new_id},{org_id},{name},{target_qunatity},{estimated_price},0\n')
     return 'Stock added successfully'

#Get Org Stocks
def get_org_stocks(org_id):
     res = []
     stocks = get_all_records('stocks.csv')
     for stock in stocks:
          if stock['org_id'] == org_id:
               res.append(stock)
     return res          

#Count Org members involved
def count_org_members(org_stocks):
     contributions = get_all_records('stock_contributions.csv')
     stock_id_set = set([stock['stock_id'] for stock in org_stocks])
     count = 0
     for contribution in contributions:
          if contribution['stock_id'] in stock_id_set:
               count+=1
     return count          


# Get Organization Metrics
def get_org_metrics(org_id):
     org = get_record("organizations.csv", org_id)
     if org == {}: return
     stocks = get_org_stocks(org_id)
     members_involved = count_org_members(stocks)
     org['STOCKS'] = len(stocks)
     org['MEMBERS_INVOLVED'] = members_involved
     return org

#Delete Stock Function
def delete_stock(stock_id):
    contributions = get_stock_contributions(stock_id)
    contribution_ids = [contribution['contribution_id'] for contribution in contributions]
    for contribution_id in contribution_ids:
         delete_contribution(contribution_id)
    delete_record("stocks.csv", stock_id)


#Stock View Functions

#get stock contributions
def get_stock_contributions(stock_id):
     res = []
     contributions = get_all_records('stock_contributions.csv')
     for contribution in contributions:
          if contribution['stock_id'] == stock_id:
               res.append(contribution)
     return res      

#edit stock
def edit_stock(stock_id, name,target_qunatity,estimated_price):
     current_stock_record = get_record("stocks.csv", stock_id)
     org_id = current_stock_record['org_id']
     new_record =  f"{stock_id},{org_id},{name},{target_qunatity},{estimated_price},{current_stock_record['contributed_amount']}"
     update_record('stocks.csv', stock_id, new_record)
     contributions = get_stock_contributions(stock_id)
     for contribution in contributions:
          edit_contribution(contribution['contribution_id'], contribution['amount_paid'])

# add contributions to stock function
def add_contributions(stock_id, member_ids):
     last_updated,quantity_due,amount_paid = time(),0,0
     for member_id in member_ids:
          contribution_id = get_new_id("stock_contributions.csv")
          add_record("stock_contributions.csv", f"{contribution_id},{stock_id},{member_id},{amount_paid},{quantity_due},{last_updated}\n")

back_up_database(False)

# edit contributions
def edit_contribution(contribution_id, new_amount):
     contribution = get_record("stock_contributions.csv", contribution_id)
     if contribution == {}: return
     stock = get_record("stocks.csv", contribution['stock_id'])
     
     prev_amount = int(contribution['amount_paid'])
     change = int(new_amount) - prev_amount

     new_contributed_amount = int(stock['contributed_amount']) + change
     new_quantity_due = (int(new_amount) / int(stock['estimated_price'])) * int(stock['target_quantity'] )
     
     last_updated = time()
     update_record("stocks.csv", stock['stock_id'], f"{stock['stock_id']},{stock['org_id']},{stock['product_name']},{stock['target_quantity']},{stock['estimated_price']},{new_contributed_amount}")
     update_record("stock_contributions.csv", contribution['contribution_id'],f"{contribution_id},{contribution['stock_id']},{contribution['member_id']},{new_amount},{new_quantity_due},{last_updated}")


#Delete Stock contribution
def delete_contribution(contribution_id):
     contribution = get_record("stock_contributions.csv", contribution_id)
     
     if contribution == {}: return
     stock =  get_record("stocks.csv", contribution['stock_id'])
     new_contributed_amount = int(stock['contributed_amount']) - int(contribution['amount_paid'])
     update_record("stocks.csv", contribution['stock_id'], f"{stock['stock_id']},{stock['org_id']},{stock['product_name']},{stock['target_quantity']},{stock['estimated_price']},{new_contributed_amount}")
     delete_record("stock_contributions.csv", contribution['contribution_id'])


#Members View

#create new member

def create_member(name, phone):
     member_id = get_new_id("members.csv")
     members = get_all_records("members.csv")
     member_names = set([member['fullname'] for member in members])
     member_phones = set([member['phone_number'] for member in members])
     if name in member_names:
          return "Error adding member: name already used"
     elif phone in member_phones:
          return "Error Adding member: Phone already used"
     else:
      new_member_record = f"{member_id},{name},{phone},{time()}\n"
      add_record("members.csv", new_member_record)
      return f"Member {name} Added Successfully"
     
def edit_member(member_id, new_name, new_phone):
     members = get_all_records("members.csv")
     current_member = get_record("members.csv", member_id)
     if current_member == {}: return

     #below the member is removed from the list for checks
     member_excluded_list = list(filter(lambda x: x['member_id'] != member_id, members))

     member_names = set([member['fullname'] for member in member_excluded_list])
     member_phones = set([member['phone_number'] for member in member_excluded_list])
     if new_name in member_names:
          return "Error adding member: name already used"
     elif new_phone in member_phones:
          return "Error Adding member: Phone already used"
     else:
          updated_member_record = f"{member_id},{new_name},{new_phone},{current_member['date_registered']}"
          update_record("members.csv", member_id, updated_member_record)

#delete member function
def delete_member(member_id):
     all_contributions = get_all_records("stock_contributions.csv")
     member_contributions = list(filter(lambda x: x['member_id'] == member_id, all_contributions))
     for contribution in member_contributions:
          delete_contribution(contribution['contribution_id'])
     delete_record("members.csv", member_id)

 
#Export Zone
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter



def export_stock_report(stock_id):

    # get stock
    stock = get_record("stocks.csv", stock_id)

    if stock == {}:
        print("Stock not found")
        return

    # get organization
    org = get_record("organizations.csv", stock['org_id'])

    # get settings
    settings = get_record("settings.csv", "1")

    # export folder
    export_folder = settings['export_path']

    create_new_folder(export_folder)

    # generate filename
    filename = f"{stock['product_name']}_{time()}.pdf"
    export_path = os.path.join(export_folder, filename)

    # create pdf document
    doc = SimpleDocTemplate(
        export_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    # title
    title = Paragraph(
        f"<b>{settings['biz_name']}</b>",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    # stock metadata
    metadata = [
        f"Organization: {org['name']}",
        f"Stock Name: {stock['product_name']}",
        f"Target Quantity: {stock['target_quantity']}",
        f"Estimated Price: {stock['estimated_price']}",
        f"Contributed Amount: {stock['contributed_amount']}",
        f"Generated At: {time()}"
    ]

    for item in metadata:
        elements.append(
            Paragraph(item, styles['BodyText'])
        )

    elements.append(Spacer(1, 20))

    # contribution table
    contributions = get_stock_contributions(stock_id)

    table_data = [[
        "Member Name",
        "Amount Paid",
        "Quantity Due",
        "Last Updated"
    ]]

    for contribution in contributions:

        member = get_record(
            "members.csv",
            contribution['member_id']
        )

        table_data.append([
            member['fullname'],
            contribution['amount_paid'],
            contribution['quantity_due'],
            contribution['last_updated']
        ])

    # create table
    table = Table(table_data)

    # style table
    table.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),

        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

        ('GRID', (0, 0), (-1, -1), 1, colors.black)

    ]))

    elements.append(table)

    # build pdf
    doc.build(elements)

    print(f"Stock report exported successfully")
    print(f"Saved to: {export_path}")
     







     




    

    

    
            

  