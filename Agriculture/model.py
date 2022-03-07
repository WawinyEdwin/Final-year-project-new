from decimal import Decimal
from sqlalchemy import *

engine = create_engine('mysql://root:@localhost/food_securitydb')

metadata_obj = MetaData()
role = Table('role', metadata_obj,
             Column('id', Integer, primary_key=True),
             Column('title', String(100), nullable=False),
             Column('description', String(100), nullable=False),
             
             Column('slug', String(100), unique=True, nullable=False),
             Column('status', Integer, default=0, nullable=False),
             Column('created_at', DateTime, nullable=False),
             Column('updated_at', DateTime, nullable=True),
             
             )
permission = Table('permission', metadata_obj,
                   Column('id', Integer, primary_key=True),
                   Column('title', Integer, nullable=False),
                   Column('description', String(100), nullable=False),
                   Column('slug', String(100), unique=True, nullable=False),
                   Column('status', Integer, default=0, nullable=False),
                   Column('created_at', DateTime, nullable=False),
                   Column('updated_at', DateTime, nullable=True),
                   Column('farm', Integer, ForeignKey(
                       "farm.id"), nullable=False)
                   )
role_permission = Table('role_permission', metadata_obj,
                        Column('id', Integer, primary_key=True),
                        Column('role_id', Integer, ForeignKey("role.id")),
                        Column('created_at', DateTime, nullable=False),
                        Column('updated_at', DateTime, nullable=True),

                        )

user = Table('user', metadata_obj,

             Column('id', Integer, primary_key=True),
             Column('role_id', Integer, ForeignKey("role.id")),
             Column('fname', String(60), nullable=False),
             Column('lname', String(60), nullable=False),
             Column('mname', String(60), nullable=False),
             Column('username', String(60), unique=True, nullable=False),
             Column('email', String(60), key='email',
                    unique=True, nullable=False),
             Column('mobile', String(60), unique=True, nullable=True),
             Column('password_hash', String(60), nullable=False),
             Column('registered_at', DateTime, nullable=False),
             Column('intro', String(60), nullable=True),
             Column('last_login', DateTime, nullable=True),
)
employee = Table('employee', metadata_obj,
                 Column('id', Integer, primary_key=True),
                 Column('user_id', Integer, ForeignKey("user.id")),
                 Column('role_id', Integer, ForeignKey("role.id")),
                 Column('updated_by', Integer, ForeignKey("user.id")),
                 Column('status', Integer, default=0, nullable=False),
                 Column('code', String(100), unique=True),
                 Column('start_at', DateTime, nullable=False),
                 Column('ends_at', DateTime, nullable=True),
                 Column('created_at', DateTime, nullable=False),
                 Column('updated_at', DateTime, nullable=True),
                 Column('salary', Integer, nullable=False),
                 Column('branch', Integer, ForeignKey(
                     "farm_type.id"), nullable=False),
                 Column('farm', Integer, ForeignKey("farm.id"), nullable=False)

                 )
# New, Approved, Active, or Blocked.
farm = Table('farm', metadata_obj,
             Column('id', Integer, primary_key=True),
             Column('company_name', String(100)),
             Column('slug', String(100), unique=True, nullable=False),
             Column('created_by', Integer, ForeignKey("user.id")),
             Column('status', Integer, default=0, nullable=False),
             Column('updated_by', Integer, ForeignKey("user.id")),
             Column('created_at', DateTime, nullable=False),
             Column('updated_at', DateTime, nullable=True),
             Column('content', String(100)),
             Column('owner', Integer, ForeignKey(
                 "user.id"), nullable=False)

             )
farm_type = Table('farm_type', metadata_obj,
                  Column('id', Integer, primary_key=True),
                  Column('type_name', String(100)),
                  Column('company', Integer, ForeignKey(
                      "farm.id"), nullable=False),


                  )
customer = Table("customer", metadata_obj,
                 Column('id', Integer, primary_key=True),
                 Column('customer_name', String(60),  nullable=False),
                 Column('customer_email', String(60),
                        key='email', unique=True, nullable=False),
                 Column('customer_contact', String(
                     60), unique=True, nullable=True),
                 Column('sex', String(60), nullable=True),
                 Column('farm', Integer, ForeignKey("farm.id"), nullable=False)
                 )
# Dairy Farming
cow_type = Table('cow_type', metadata_obj,
                 Column('id', Integer, primary_key=True),
                 Column('name', String(100), unique=True),
                 Column('description', String(100)),
                 Column('farm', Integer, ForeignKey("farm.id"), nullable=False)
                 )
cow_info = Table('cow_info', metadata_obj,
                 Column('id', Integer, primary_key=True),

                 Column('gender', String(100)),
                 Column('image', String(100)),
                 Column('status', Integer, default=0, nullable=False),
                 Column('DOB', String(100)),
                 Column('type', Integer, ForeignKey(
                     "cow_type.id"), nullable=False),
                 Column('user_id', Integer, ForeignKey(
                     "employee.id"), nullable=False),
                 Column('farm', Integer, ForeignKey("farm.id"), nullable=False)
                 )
cow_sale = Table('cow_sale', metadata_obj,
                 Column('id', Integer, primary_key=True),
                 Column('invoice_number', Integer,
                        unique=True, nullable=False),

                 Column('date_recorded', DateTime, nullable=False),
                 Column('amount', Float, nullable=False),
                 Column('customer', Integer, ForeignKey(
                     "customer.id"), nullable=False),
                 Column('employee', Integer, ForeignKey(
                     "employee.id"), nullable=False),
                 Column('company', Integer, ForeignKey(
                     "farm.id"), nullable=False),
                 Column('cow_no', Integer, ForeignKey(
                     "cow_info.id"), nullable=False),
                 Column('remarks', String(200), nullable=True),


                 )
cow_vacc = Table('cow_vacc', metadata_obj,
                 Column('date', DateTime),
                 Column('cow_no', Integer),
                 Column('remarks', String(100)),
                 Column('cow_id', Integer, ForeignKey(
                     "cow_info.id"), nullable=False),
                 Column('company', Integer, ForeignKey(
                     "farm.id"), nullable=False),
                 Column('employee', Integer, ForeignKey(
                     "employee.id"), nullable=False)


                 )
cow_feed = Table('cow_feed', metadata_obj,
                 Column('id', Integer, primary_key=True),
                 Column('date', DateTime),
                 Column('cow_no', Integer, ForeignKey(
                     "cow_info.id"), nullable=False),
                 Column('food_item', String(200), nullable=False),
                 Column('quantity', Float, nullable=False),
                 Column('feed_time', DateTime, nullable=False),
                 Column('remarks', String(100)),
                 Column('employee', Integer, ForeignKey(
                     "employee.id"), nullable=False),
                 Column('company', Integer, ForeignKey(
                     "farm.id"), nullable=False),
                 )
cow_milk = Table('cow_milk', metadata_obj,
                 Column('id', Integer, primary_key=True),
                 Column('cow_no', Integer, ForeignKey("cow_info.id")),
                 Column('date', DateTime, nullable=False),
                 Column('liter', Float, nullable=False),
                 Column('price', Float, nullable=False),
                 Column('total', Float, nullable=False),
                 Column('employee', Integer, ForeignKey(
                     "employee.id"), nullable=False),
                 Column('company', Integer, ForeignKey(
                     "farm.id"), nullable=False),
                 )
milk_sale = Table('milk_sale', metadata_obj,
                  Column('id', Integer, primary_key=True),
                  Column('date', DateTime, nullable=False),
                  Column('liter', Float, nullable=False),
                  Column('price', Float, nullable=False),
                  Column('total', Float, nullable=False),
                  Column('customer', Integer, ForeignKey(
                      "customer.id"), nullable=False),
                  Column('employee', Integer, ForeignKey(
                      "employee.id"), nullable=False),
                  Column('company', Integer, ForeignKey(
                      "farm.id"), nullable=False),
                  )

cow_vaccine = Table('cow_vaccine', metadata_obj,
                    Column('id', Integer, primary_key=True),
                    Column('cow_id', Integer, ForeignKey(
                        "cow_info.id"), nullable=False),
                    Column('remarks', String(100), nullable=True),
                    Column('employee', Integer, ForeignKey(
                        "employee.id"), nullable=False),
                    Column('company', Integer, ForeignKey(
                        "farm.id"), nullable=False),

                    )
feed = Table('feed', metadata_obj,
             Column('id', Integer, primary_key=True),

             Column('name', String(100), nullable=True),
             Column('manufactured_date', DateTime, nullable=False),
             Column('manufacturing_code', Integer, nullable=True),
             Column('validation_period', DateTime, nullable=False),
             Column('producer', String(100), nullable=True),
             Column('quantity_bought', Integer, nullable=False),
             Column('quantity_remain', Integer, nullable=False),
             Column('price', Integer, nullable=False),
             Column('company', Integer, ForeignKey("farm.id"), nullable=False),
             Column('employee', Integer, ForeignKey(
                 "employee.id"), nullable=False)
             )

# Poultry Tables
batch_flock = Table('batch_flock', metadata_obj,
                    Column('id', Integer, primary_key=True),
                    Column('breed_type', Integer, ForeignKey(
                        "breed_type.id"), nullable=False),
                    Column('date', DateTime, nullable=True),
                    Column('expired', Integer, nullable=True),
                    Column('total', Integer, nullable=True),
                    Column('laying', Integer, nullable=True),
                    Column('batch_no', String(20), nullable=True),
                    Column('company', Integer, ForeignKey(
                        "farm.id"), nullable=False),
                    )

batch_no = Table('batch_no', metadata_obj,
                 Column('id', Integer, primary_key=True),
                 Column('breed_type', Integer, ForeignKey(
                        "breed_type.id"), nullable=False),
                 Column('batch_no', String(20), nullable=True),
                 Column('company', Integer, ForeignKey(
                     "farm.id"), nullable=False)

                 )
breed_type = Table('breed_type', metadata_obj,
                   Column('id', Integer, primary_key=True),

                   Column('name', String(40), nullable=True),
                   Column('company', Integer, ForeignKey(
                       "farm.id"), nullable=False),

                   )
calendar = Table('calendar', metadata_obj,
                 Column('id', Integer, primary_key=True),

                 Column('title', String(120), nullable=True),
                 Column('description', Text, nullable=False),
                 Column('start', DateTime, nullable=False),
                 Column('end', DateTime, nullable=False),
                 Column('allDay', String(200), nullable=False),
                 Column('color', String(200), nullable=False),
                 Column('url', String(200), nullable=False),
                 Column('category', String(200), nullable=False),
                 Column('repeat_type', String(200), nullable=False),
                 Column('user_id', Integer, nullable=False),
                 Column('repeat_id', Integer, nullable=False),
                 Column('company', Integer, ForeignKey(
                     "farm.id"), nullable=False),

                 )
document = Table('document', metadata_obj,
                 Column('id', Integer, primary_key=True),
                 Column('title', String(200), nullable=False),
                 Column('detail', String(200), nullable=False),
                 Column('image', String(200), nullable=False),
                 Column('company', Integer, ForeignKey(
                     "farm.id"), nullable=False),

                 )

egg_production = Table('egg_production', metadata_obj,
                       Column('id', Integer, primary_key=True),
                       Column('batch_flock', Integer, ForeignKey(
                           "batch_flock.id"), nullable=False),
                       Column('total', Integer, nullable=True),
                       Column('cracked', Integer, nullable=True),
                       Column('double_york', Integer, nullable=True),
                       Column('dirty', Integer, nullable=True),
                       Column('other', Integer, nullable=True),

                       Column('worker', Integer, ForeignKey(
                           "employee.id"), nullable=False),
                       Column('date', DateTime, nullable=True),
                       Column('company', Integer, ForeignKey(
                           "farm.id"), nullable=False),


                       )
expcat = Table('expcat', metadata_obj,
               Column('id', Integer, primary_key=True),
               Column('title', String(50), nullable=False),
               Column('company', Integer, ForeignKey(
                   "farm.id"), nullable=False),
               )
expenses = Table('expenses', metadata_obj,
                 Column('id', Integer, primary_key=True),
                 Column('category', Integer, ForeignKey(
                     "expcat.id"), nullable=False),
                 Column('description', String(100), nullable=True),
                 Column('date', DateTime, nullable=False),
                 Column('amount', Float, nullable=True),
                 Column('company', Integer, ForeignKey(
                     "farm.id"), nullable=False),
                 )
incat = Table('incat', metadata_obj,
              Column('id', Integer, primary_key=True),
              Column('title', String(50), nullable=False),
              Column('company', Integer, ForeignKey(
                  "farm.id"), nullable=False),
              )
income = Table('income', metadata_obj,
               Column('id', Integer, primary_key=True),
               Column('category', Integer, ForeignKey(
                   "incat.id"), nullable=False),
               Column('description', String(100), nullable=True),
               Column('date', DateTime, nullable=False),
               Column('amount', Float, nullable=True),
               Column('company', Integer, ForeignKey(
                   "farm.id"), nullable=False),
               )
feed_type = Table('feed_type', metadata_obj,
                  Column('id', Integer, primary_key=True),
                  Column('title', String(50), nullable=False),
                  Column('company', Integer, ForeignKey(
                      "farm.id"), nullable=False),
                  )
general_setting = Table('general_setting', metadata_obj,
                        Column('id', Integer, primary_key=True),
                        Column('sitename', String(350), nullable=False),
                        Column('email', String(350), nullable=False),
                        Column('mobile', String(350), nullable=False),
                        Column('radiocode', String(350), nullable=False),
                        Column('tvcode', String(350), nullable=False),
                        Column('currency', String(350), nullable=False),
                        Column('sms', String(350), nullable=False),
                        Column('company', Integer, ForeignKey(
                            "farm.id"), nullable=False),


                        )
hatched = Table('hatched', metadata_obj,
                Column('id', Integer, primary_key=True),
                Column('batch_flock', Integer, ForeignKey(
                    "batch_flock.id"), nullable=False),
                Column('name', String(60), nullable=True),
                Column('received', Integer, ForeignKey(
                    "employee.id"), nullable=True),
                Column('received_by', Integer, ForeignKey(
                    "employee.id"), nullable=False),
                Column('integerroduction_date', Date, nullable=True),
                Column('idate_total', Integer, nullable=True),

                Column('hatched', Integer, nullable=True),
                Column('survived', Integer, nullable=True),
                Column('company', Integer, ForeignKey(
                    "farm.id"), nullable=False),

                )

inventory = Table('inventory', metadata_obj,
                  Column('id', Integer, primary_key=True),
                  Column('feed_type', Integer, ForeignKey(
                      "feed_type.id"), nullable=False),


                  Column('amount', Float, nullable=True),
                  Column('receipt_no', Integer, nullable=True),
                  Column('date_issued', DateTime, nullable=False),
                  Column('company', Integer, ForeignKey(
                      "farm.id"), nullable=False),

                  )

order = Table('order', metadata_obj,
              Column('id', Integer, primary_key=True),
              Column('customer', Integer, nullable=False),
              Column('description', String(350), nullable=False),
              Column('amount', Float, nullable=False),
              Column('paid', Float, nullable=False),
              Column('balnce', Float, nullable=False),
              Column('received_by', Integer, ForeignKey(
                  "employee.id"),  nullable=False),
              Column('date_received', DateTime, nullable=False),
              Column('date_completed', DateTime, nullable=False),
              Column('date_collected', DateTime, nullable=False),
              Column('company', Integer, ForeignKey(
                  "farm.id"), nullable=False),


              )

sales = Table('sales', metadata_obj,
              Column('id', Integer, primary_key=True),
              Column('type', Integer, nullable=False),
              Column('booking_receipt_no', Integer, nullable=False),
              Column('booking_amount', Float, nullable=False),
              Column('final_receipt_no', Integer, nullable=False),
              Column('final_payment', Float, nullable=False),
              Column('quantity', Integer, nullable=False),
              Column('unit_price', Float, nullable=False),
              Column('total', Float, nullable=False),
              Column('worker_id', Integer, nullable=False),
              Column('customer_id', Integer, nullable=False),
              Column('approved_by', Integer, nullable=False),
              Column('date', DateTime, nullable=False),
              Column('company', Integer, ForeignKey(
                  "farm.id"), nullable=False),


              )

sms = Table('sms', metadata_obj,
            Column('id', Integer, primary_key=True),

            Column('customer', String(100), nullable=True),
            Column('message', Text, nullable=False),
            Column('date', DateTime, nullable=True),
            Column('company', Integer, ForeignKey(
                "farm.id"), nullable=False),
            )

template = Table('template', metadata_obj,
                 Column('id', Integer, primary_key=True),
                 Column('title', String(100), nullable=True),
                 Column('message', Text, nullable=False),
                 Column('company', Integer, ForeignKey(
                     "farm.id"), nullable=False),
                 )

vaccine = Table('vaccine', metadata_obj,
                Column('id', Integer, primary_key=True),
                Column('name', Integer, nullable=False),
                Column('vaccine_id', Integer, nullable=False),
                Column('administered_by', Integer, nullable=False),
                Column('due_date', DateTime, nullable=False),
                Column('relative_date', DateTime, nullable=False),
                Column('date_given', DateTime, nullable=False),
                Column('expiry_date', DateTime, nullable=False),
                Column('reaction', String(350), nullable=False),
                Column('other_details', String(350), nullable=False),
                Column('batch_flock', Integer, nullable=False),
                Column('company', Integer, ForeignKey(
                    "farm.id"), nullable=False),



                )
vaccine_medication = Table('vaccine_medication', metadata_obj,
                           Column('id', Integer, primary_key=True),
                           Column('strain', String(100), nullable=True),
                           Column('route', String(100), nullable=True),
                           Column('name', String(100), nullable=True),
                           Column('dose', String(100), nullable=True),
                           Column('age', String(100), nullable=True),
                           Column('company', Integer, ForeignKey(
                               "farm.id"), nullable=False),


                           )

# Crop Farming Tables

crop = Table('crop', metadata_obj,
             Column('id', Integer, primary_key=True),
             Column('name', String(100), nullable=True),
             Column('category', String(100), nullable=True),
             Column('description', Text, nullable=False),
             Column('planted', Integer, nullable=True),
             Column('date_planted', DateTime, nullable=False),
             Column('date', DateTime, nullable=False),
             Column('price', Integer, nullable=False),
             Column('company', Integer, ForeignKey(
                 "farm.id"), nullable=False),

             )
supply = Table('supply', metadata_obj,
               Column('id', Integer, primary_key=True),
               Column('name', String(100), nullable=True),
               Column('address', String(100), nullable=True),
               Column('email', String(100), nullable=False),
               Column('company', Integer, ForeignKey(
                   "farm.id"), nullable=False),

               )
pesticide = Table('pesticide', metadata_obj,
                  Column('id', Integer, primary_key=True),
                  Column('name', String(100), nullable=True),
                  Column('category', String(100), nullable=True),
                  Column('description', String(100), nullable=False),
                  Column('rate', Integer, nullable=True),
                  Column('crop', Integer, nullable=False),
                  Column('accre', Integer, nullable=False),
                  Column('total', Float, nullable=False),
                  Column('company', Integer, ForeignKey(
                      "farm.id"), nullable=False),

                  )
fertilizer = Table('fertilizer', metadata_obj,
                   Column('id', Integer, primary_key=True),
                   Column('name', String(100), nullable=True),
                   Column('category', String(100), nullable=True),
                   Column('description', String(100), nullable=False),
                   Column('company', Integer, ForeignKey(
                       "farm.id"), nullable=False),

                   )
harvest = Table('harvest', metadata_obj,
                Column('id', Integer, primary_key=True),
                Column('date', DateTime, nullable=True),
                Column('category', String(100), nullable=True),
                Column('description', String(100), nullable=False),
                Column('units', String(100), nullable=False),
                Column('total', Float, nullable=False),
                Column('consumed', Float, nullable=False),
                Column('friends', Integer, nullable=False),
                Column('damage', Integer, nullable=False),
                Column('sold', Integer, nullable=False),
                Column('employee', Integer, ForeignKey(
                    "employee.id"), nullable=False),
                Column('company', Integer, ForeignKey(
                    "farm.id"), nullable=False),

                )

soil_test = Table('soil_test', metadata_obj,
                  Column('id', Integer, primary_key=True),
                  Column('name_lab', String(100), nullable=True),
                  Column('date', DateTime, nullable=True),
                  Column('ph', Integer, nullable=True),
                  Column('p', Integer, nullable=False),
                  Column('k', Integer, nullable=True),
                  Column('ca', Integer, nullable=False),
                  Column('mg', Integer, nullable=False),
                  Column('company', Integer, ForeignKey(
                      "farm.id"), nullable=False),

                  )
creditors = Table('creditors', metadata_obj,
                  Column('id', Integer, primary_key=True),
                  Column('lender', String(100), nullable=True),
                  Column('lender_address', String(100), nullable=True),
                  Column('date', DateTime, nullable=True),
                  Column('particulars', String(500), nullable=True),
                  Column('debt', Float, nullable=False),
                  Column('paid', Float, nullable=True),
                  Column('balance', Integer, nullable=False),
                  Column('witness', Text, nullable=False),
                  Column('company', Integer, ForeignKey(
                      "farm.id"), nullable=False),

                  )
debtors = Table('debtors', metadata_obj,
                Column('id', Integer, primary_key=True),
                Column('lender', String(100), nullable=True),
                Column('lender_address', String(100), nullable=True),
                Column('date', DateTime, nullable=True),
                Column('particulars', String(500), nullable=True),
                Column('debt', Float, nullable=False),
                Column('paid', Float, nullable=True),
                Column('balance', Integer, nullable=False),
                Column('witness', Text, nullable=False),
                Column('company', Integer, ForeignKey(
                    "farm.id"), nullable=False),

                )
metadata_obj.create_all(engine)
