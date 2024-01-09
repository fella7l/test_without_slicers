
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
    


data = pd.read_csv('sales7data.csv')

st.sidebar.title("Streamlit Sales App ")
st.sidebar.subheader('Dive into a world of insights with our dynamic Streamlit app!')

Df = data.dropna()


# your code goes here




selected_year_range = st.sidebar.slider("Year", min_value=min(Df['Year']), max_value=max(Df['Year']))
selected_month = st.sidebar.multiselect("Months", Df['Month'].unique())
selected_gender = st.sidebar.multiselect("Gender", Df['Customer_Gender'].unique())
selected_country = st.sidebar.multiselect("Country", Df['Country'].unique()) 


st.sidebar.markdown("""
Embark on a data exploration adventure with our dynamic Streamlit app! Featuring a robust DataFrame comprising 113,036 entries and 18 columns, this app is your gateway to uncovering intricate details about customer behavior, product categories, and financial metrics.
""")

  

Df['Day'] = Df['Day'].astype(str).str.zfill(2)
Df['Month'] = Df['Month'].astype(str)
Df['Year'] = Df['Year'].astype(str)

Df['Date'] = Df['Day'] + '-' + Df['Month'] + '-' + Df['Year']


# your code goes here
Df['Calculated_Date'] = pd.to_datetime(Df['Date'], format='%d-%B-%Y')

total_cost = Df['Cost'].sum()
total_revenue = Df['Revenue'].sum()
Mean_Customer_age = Df['Customer_Age'].mean().round(2)
Number_of_Customers = Df['Customer_Age'].count()
Mean_Order_Quantity= Df['Order_Quantity'].mean().round(2)
Total_Sales= Df['Order_Quantity'].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Cost", total_cost, "USD")

with col2:
    st.metric("Total Revenue", total_revenue, "USD")

with col3:
    st.metric("Total Sales", Total_Sales , "units")
    
with col4:
    st.metric("Average of Orders", Mean_Order_Quantity, "units")


st.subheader("Customer_Information")

col1, col2,  = st.columns(2)

with col1:
    st.metric("Number of Curomers", Number_of_Customers, "years")
with col2:
    st.metric("Average Age", Mean_Customer_age, "years")
    
    
# Plot 1: KDE Plot for Customer Age
col1, col2 = st.columns(2)

# Plot 1: KDE Plot for Customer Age
with col1:
    plt.figure(figsize=(16, 8))
    Df['Customer_Age'].plot(kind='kde', color='0.75')
    plt.axvline(Df['Customer_Age'].mean(), color='steelblue')  
    plt.xlabel('Customer Age')
    plt.title('Density of Customer Age')
    st.pyplot()

# Plot 2: Pie Chart for Gender Distribution
AVG_Age_per_Country = Df.pivot_table(index='Country', values='Customer_Age', aggfunc='mean')
sort_AVG_Age_per_Country = AVG_Age_per_Country.sort_values(by='Customer_Age', ascending=False)

with col2:
   # AVG_Age_per_Country = Df.pivot_table(index='Country', values='Customer_Age', aggfunc='mean')
   #sort_AVG_Age_per_Country = AVG_Age_per_Country.sort_values(by='Customer_Age', ascending=False)

   country_colors = {country: sns.color_palette('vlag')[i] for i, country in enumerate(Df['Country'].unique())}
   Df['Country_Color'] = Df['Country'].map(country_colors)   

   plt.figure(figsize=(16, 8))
   sns.boxplot(x='Country', y='Customer_Age', data=Df, palette=country_colors, order=sort_AVG_Age_per_Country.index)
   plt.title('Average Customer Age per Country')
   plt.xlabel('Customer Age')
   plt.ylabel('Country')
   st.pyplot()
# Table in the first column


col1, col2 = st.columns(2)

# Plot 1: Pie Chart for Gender Distribution
with col1:
    plt.figure(figsize=(4, 4))
    gender_of_customers = Df['Customer_Gender'].value_counts()
    plt.pie(gender_of_customers, labels=gender_of_customers.index, autopct='%1.1f%%', colors=['#3E727F', 'orchid'])
    plt.legend(title="Gender", loc="lower right")
    plt.title('Gender Distribution')
    st.pyplot()

# Plot 2: Pivot Table for Gender Distribution
with col2:
   
    AVG_Age_per_Country = Df.pivot_table(index='Country', values='Customer_Age', aggfunc='mean').sort_values(by='Customer_Age', ascending=False)
    st.table(AVG_Age_per_Country)
    gender_pivot_table = Df.pivot_table(index='Customer_Gender', values='Order_Quantity', aggfunc='sum').sort_values(by='Order_Quantity', ascending=False) 
    st.table(gender_pivot_table)
    



Gender_sale= Df.pivot_table(index='Customer_Gender', values= 'Order_Quantity')
Order_per_Sales = Gender_sale.sort_values(by='Order_Quantity', ascending=False)

st.subheader('Salse informations')
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# Graphique 1: Histogramme - Order Quantity
axes[0, 0].hist(Df['Order_Quantity'], color='#3E727F')
axes[0, 0].set_xlabel('Order Quantity')
axes[0, 0].set_title('Frequency of Order Quantity')

# Graphique 2: Boxplot - Order Quantity
axes[0, 1].boxplot(Df['Order_Quantity'], patch_artist=True, boxprops=dict(facecolor='0.75'), medianprops=dict(color='steelblue'))
axes[0, 1].set_title('Boxplot of Order Quantity')

# Graphique 3: Pie Chart - Sales per Year
sales_per_year = Df.groupby('Year')['Order_Quantity'].sum()
total_sales = Df['Order_Quantity'].sum()
percentage_of_sales_per_year = (sales_per_year / total_sales * 100).round(2)

axes[1, 0].pie(sales_per_year, labels=percentage_of_sales_per_year.index, autopct='%1.1f%%', colors=['#026A8F', '#057E86', '#597E76', '#3E727F', '#96AFB6', '#D1DEE4'])
axes[1, 0].set_title('Sales per Year')
axes[1, 0].legend(title="Year", loc="lower right")

# Ajouter des étiquettes aux axes x et y
axes[1, 0].set_xlabel('X-axis Label')
axes[1, 0].set_ylabel('Y-axis Label')

# Graphique 4: Bar Chart - Sales per Month
sales_per_month = Df.pivot_table(index='Month', values='Order_Quantity', aggfunc='sum')
sort_sales = sales_per_month.sort_values(by='Order_Quantity', ascending=False)

color = sns.color_palette('Blues')
axes[1, 1].bar(sort_sales.index, sort_sales['Order_Quantity'], color=color)
axes[1, 1].set_xlabel('Month')
axes[1, 1].set_ylabel('Sales')
axes[1, 1].set_title('Sales per Month')
plt.xticks(rotation=45, ha='right')

# Adjust space between subplots to avoid overlapping titles
plt.subplots_adjust(wspace=0.5, hspace=0.5)

# Afficher la figure dans Streamlit
st.pyplot(fig)

Df['Month'] = Df['Calculated_Date'].dt.month

# Créez une figure et des axes
fig, ax = plt.subplots(figsize=(16, 8))

# Utilisez seaborn pour créer un boxplot
sns.boxplot(x='Month', y='Profit', data=Df, palette='vlag', ax=ax)

# Ajoutez des étiquettes et un titre
ax.set_xlabel('Month')
ax.set_ylabel('Profit')
ax.set_title('Profit per Month')

# Affichez la figure dans Streamlit
st.pyplot(fig)


fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Graphique 1: Bar Plot - Sales per Country
country_colors = {country: sns.color_palette('vlag')[i] for i, country in enumerate(Df['Country'].unique())}
Df['Country_Color'] = Df['Country'].map(country_colors)    


sort_country = Df.pivot_table(index='Country', values='Order_Quantity', aggfunc='sum').sort_values(by='Order_Quantity', ascending=False)
bars=axes[0].bar(sort_country.index, sort_country['Order_Quantity'], color=Df['Country_Color'])
axes[0].set_xlabel('Country')
axes[0].set_ylabel('Sales')
axes[0].set_title('Sales per Country')
plt.xticks(rotation=45, ha='right')
for bar in bars:
        yval = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')
        
        

sns.boxplot(x='Country', y='Profit', data=Df, palette=country_colors, ax=axes[1])
axes[1].set_title('Profit per Country')
axes[1].set_xlabel('Profit')
axes[1].set_ylabel('Country')
# Graphique 2: Bar Plot - Top 10 Products

st.pyplot(fig)


Product_sold = Df.pivot_table(index='Product', values='Order_Quantity', aggfunc='sum').sort_values(by='Order_Quantity', ascending=False)
top_10 = Product_sold.head(10)

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Graphique 1: Bar Plot - Top 10 Product Orders
bars2 = sns.barplot(x=top_10.index, y=top_10['Order_Quantity'], ax=axes[0], palette='Blues')
axes[0].set_xlabel('Product')
axes[0].set_ylabel('Order_Quantity')
axes[0].set_title('Top 10 Product Orders')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, ha='right') 
for bar2 in bars2.patches:
    yval2 = bar2.get_height()
    axes[0].text(bar2.get_x() + bar2.get_width()/2, yval2, round(yval2, 2), ha='center', va='bottom')

# Partie 2
# Graphique 2: Line Plot - Total Sales Over Time
sales_per_date = Df.groupby('Calculated_Date')['Order_Quantity'].sum()
sns.lineplot(x=sales_per_date.index, y=sales_per_date.values, color= '0.75')
axes[1].set_xlabel('Calculated Date')
axes[1].set_ylabel('Total Sales')
axes[1].set_title('Total Sales Over Time')

# Ajuster l'espace entre les subplots
plt.tight_layout()
st.pyplot(fig)





Pofit_for_one= Df['Unit_Price']-Df['Unit_Cost']


# Assuming Df is your DataFrame

country_colors = {country: sns.color_palette('vlag')[i] for i, country in enumerate(Df['Country'].unique())}
Df['Country_Color'] = Df['Country'].map(country_colors)

fig, axes = plt.subplots(1, 2, figsize=(20, 8))

# Graphique 1: Scatter Plot - Unit_Cost vs Unit_Price
Df.plot(kind='scatter', x='Unit_Cost', y='Unit_Price', ax=axes[0], color='orchid')
axes[0].set_title('Relationship between Unit_Cost and Unit_Price')
axes[0].set_xlabel('Unit_Cost')
axes[0].set_ylabel('Unit_Price')

# Graphique 2: Scatter Plot - Order_Quantity vs Profit
Df.plot(kind='scatter', x='Order_Quantity', y='Profit', ax=axes[1], color='orchid')
axes[1].set_title('Relationship between Order_Quantity and Profit')
axes[1].set_xlabel('Order_Quantity')
axes[1].set_ylabel('Profit')


plt.tight_layout()
st.pyplot(fig)

# your code goes here


sales_per_category = Df.groupby('Product_Category')['Order_Quantity'].sum()

colors = ['darkmagenta', 'orchid', 'lavenderblush']

fig, axes = plt.subplots(1, 2, figsize=(20, 8))

# Partie 1: Graphique en secteurs (Pie Chart)
n = sales_per_category.plot(kind='pie', colors=colors, autopct='%1.1f%%', labels=None, ax=axes[0])
axes[0].legend(labels=sales_per_category.index, title="Sales_per_category", loc="lower right")
axes[0].set_title('Sales per Category')


orders_in_france_by_region = Df[Df['Country'] == 'France'].groupby('State')['Order_Quantity'].count()
sort_orders_in_france_by_region = orders_in_france_by_region.sort_values(ascending=False)

# Utiliser sns.barplot avec l'axe spécifié
sns.barplot(x=sort_orders_in_france_by_region.index, y=sort_orders_in_france_by_region.values, palette='vlag', ax=axes[1])

# Ajouter les étiquettes sur l'axe x avec rotation
axes[1].set_xlabel('France_State')
axes[1].set_ylabel('Number of Orders')
axes[1].set_title('Number of Orders in Each Region of France')
axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha='left')

# Ajuster l'espace entre les subplots
plt.tight_layout()

# Afficher la figure dans Streamlit
st.pyplot(fig)


accessories_orders = Df[Df['Product_Category'] == 'Accessories']
orders_per_subcategory = accessories_orders.groupby('Sub_Category')['Order_Quantity'].sum()
q = orders_per_subcategory.sort_values(ascending =False)

bike_racks_canada_count = len(Df[(Df['Country'] == 'Canada') & (Df['Sub_Category'] == 'Bike Racks')])


Bike_orders = Df[Df['Product_Category'] == 'Bikes']
orders_per_Bike_subcategory = Bike_orders.groupby('Sub_Category')['Order_Quantity'].sum()



fig, axes = plt.subplots(1, 2, figsize=(20, 8))

# Partie 1: Bar Plot pour les accessoires
color = sns.color_palette('Blues')
q.plot(kind='bar', color=color, ax=axes[0])
axes[0].set_xlabel('Accessories')
axes[0].set_ylabel('Orders')
axes[0].set_title('Orders per Accessory')
axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, ha='right')

# Partie 2: Pie Plot pour les vélos
colors = ['lightsteelblue', 'lightslategray']
orders_per_Bike_subcategory.plot(kind='pie', colors=colors, autopct='%1.1f%%', labels=None, ax=axes[1])
axes[1].legend(labels=orders_per_Bike_subcategory.index, title="Sales per Bikes", loc="lower right")
axes[1].set_title('Sales per Bike Subcategory')

# Afficher la figure dans Streamlit
st.pyplot(fig)




st.subheader('calculated informations')

# your code goes here# Assuming your DataFrame is named 'Df'
canada_france = Df[Df['Country'].isin(['Canada', 'France'])]


canada_france.pivot_table(index='Country', values='Order_Quantity', aggfunc='count')


bike_racks_canada_count = len(Df[(Df['Country'] == 'Canada') & (Df['Sub_Category'] == 'Bike Racks')])



# your code goes here
sales_by_men = Df[(Df['Customer_Gender'] == 'M') & (Df['Revenue'] > 500)]
num_sales_by_men = len(sales_by_men)



# your code goes here
t = Df.pivot_table(index= 'Order_Quantity', values=('Revenue'))
t.sort_values(by='Revenue' , ascending= False  ).head(5)

top_5_sales = Df[['Order_Quantity','Product', 'Revenue']].sort_values(by='Revenue', ascending=False).head(5)


# your code goes here
top_1_sales = Df[['Order_Quantity','Product', 'Revenue']].sort_values(by='Revenue', ascending=False).head(1)


# your code goes here
filtered_rows = Df[Df['Revenue'] > 10000]

mean_order_quantity = filtered_rows['Order_Quantity'].mean().round(0)


# your code goes here
filtered_rows2 = Df[Df['Revenue'] < 10000]

mean_order_quantity = filtered_rows2['Order_Quantity'].mean().round(0)



# your code goes here
may_2016_orders = Df[(Df['Calculated_Date'].dt.month == 5) & (Df['Calculated_Date'].dt.year == 2016)]
nb_may_2016_orders = len(may_2016_orders)





# your code goes here
may_to_july = Df[(Df['Calculated_Date'].dt.month >= 5) & (Df['Calculated_Date'].dt.month <= 7) & (Df['Calculated_Date'].dt.year == 2016)]
nb_may_to_july = len(may_to_july)



# your code goes here



# your code goes here
tax_rate = 0.072


Df['Total_Price'] = Df.apply(lambda row: row['Unit_Price'] * (1 + tax_rate) if row['Country'] == 'United States' else row['Unit_Price'], axis=1)


# ...

# Ajoutez une sous-entête pour regrouper les informations
st.subheader('More Informations')


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("Mean Order Quantity for High Revenue Sales (> 10000):")
    st.text("Mean Order Quantity: {}".format(mean_order_quantity))

# Calculated informations 8
with col2:
    st.write("Mean Order Quantity for Low Revenue Sales (< 10000):")
    st.text("Mean Order Quantity: {}".format(mean_order_quantity))

with col3:
    st.write("Number of Orders in May 2016:")
    st.text("Count: {}".format(nb_may_2016_orders))

# Calculated informations 10
with col4:
    st.write("Number of Orders from May to July 2016:")
    st.text("Count: {}".format(nb_may_to_july))
    
    
col1, col2,  = st.columns(2)
# Créez deux colonnes
with col1:

   st.write("Top 5 Sales:")
   st.write(top_5_sales)
    
with col2:
    st.write("Number of High Revenue Sales by Men:")
    st.text("Count: {}".format(num_sales_by_men))


    