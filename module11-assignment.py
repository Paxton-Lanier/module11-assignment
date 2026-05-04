# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
np.random.seed(42)

quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022',
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:
                seasonal_factor = 1.3
            elif quarter.quarter == 1:
                seasonal_factor = 0.8

            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]

            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]

            growth_factor = (1 + 0.05/4) ** quarter_idx

            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)

            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)

            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

customer_data = []
total_customers = 2000

age_params = {
    'Tampa': (45, 15),
    'Miami': (35, 12),
    'Orlando': (38, 14),
    'Jacksonville': (42, 13)
}

for location in locations:
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])

    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)

    for age in ages:
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])

        base_amount = np.random.gamma(shape=5, scale=20)

        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'],
                                     p=[0.3, 0.5, 0.2])

        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]

        purchase_amount = base_amount * tier_factor

        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    quarterly_sales = sales_df.groupby('QuarterLabel')['Sales'].sum()

    fig, ax = plt.subplots()
    ax.plot(quarterly_sales.index, quarterly_sales.values, marker='o')
    ax.set_title("Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Total Sales")
    ax.grid(True, alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    loc_sales = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack()

    fig, ax = plt.subplots()
    for loc in loc_sales.columns:
        ax.plot(loc_sales.index, loc_sales[loc], marker='o', label=loc)

    ax.set_title("Quarterly Sales by Location")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales")
    ax.legend()
    ax.grid(True, alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    latest_quarter = sales_df['Quarter'].max()
    recent = sales_df[sales_df['Quarter'] == latest_quarter]

    grouped = recent.pivot_table(values='Sales', index='Category', columns='Location', aggfunc='sum')

    fig, ax = plt.subplots()
    grouped.plot(kind='bar', ax=ax)

    ax.set_title("Category Performance by Location (Latest Quarter)")
    ax.set_xlabel("Category")
    ax.set_ylabel("Sales")
    plt.xticks(rotation=30)
    plt.tight_layout()
    return fig


def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    grouped = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    grouped_pct = grouped.div(grouped.sum(axis=1), axis=0) * 100

    fig, ax = plt.subplots()
    grouped_pct.plot(kind='bar', stacked=True, ax=ax)

    ax.set_title("Sales Composition by Location")
    ax.set_xlabel("Location")
    ax.set_ylabel("Percent of Sales")
    plt.xticks(rotation=0)
    plt.tight_layout()
    return fig


def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots()

    x = sales_df['AdSpend']
    y = sales_df['Sales']

    ax.scatter(x, y, alpha=0.7)

    m, b = np.polyfit(x, y, 1)
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = m * x_line + b
    ax.plot(x_line, y_line, linestyle='--')

    high_sales_row = sales_df.loc[sales_df['Sales'].idxmax()]
    ax.annotate(
        "Outlier",
        (high_sales_row['AdSpend'], high_sales_row['Sales']),
        xytext=(8, 8),
        textcoords='offset points'
    )

    ax.set_title("Ad Spend vs Sales")
    ax.set_xlabel("Ad Spend")
    ax.set_ylabel("Sales")
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    return fig


def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    efficiency = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()

    fig, ax = plt.subplots()
    ax.plot(efficiency.index, efficiency.values, marker='o')

    best_q = efficiency.idxmax()
    best_val = efficiency.max()
    ax.annotate(f"Highest: {best_val:.1f}", (best_q, best_val),
                xytext=(0, 10), textcoords='offset points', ha='center')

    ax.set_title("Advertising Efficiency Over Time")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales Per Ad Dollar")
    ax.grid(True, alpha=0.5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    fig, axes = plt.subplots(3, 2, figsize=(11, 10))
    axes = axes.flatten()

    all_ages = customer_df['Age']
    axes[0].hist(all_ages, bins=15, edgecolor='black')
    axes[0].axvline(all_ages.mean(), linestyle='--', label='Mean')
    axes[0].axvline(all_ages.median(), linestyle=':', label='Median')
    axes[0].set_title("Overall Age Distribution")
    axes[0].legend()

    for i, loc in enumerate(locations, start=1):
        loc_ages = customer_df[customer_df['Location'] == loc]['Age']
        axes[i].hist(loc_ages, bins=15, edgecolor='black')
        axes[i].axvline(loc_ages.mean(), linestyle='--', label='Mean')
        axes[i].axvline(loc_ages.median(), linestyle=':', label='Median')
        axes[i].set_title(loc + " Age Distribution")
        axes[i].legend()

    axes[5].axis('off')

    fig.suptitle("Customer Age Distribution")
    plt.tight_layout()
    return fig


def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    temp_df = customer_df.copy()
    bins = [18, 30, 45, 60, 100]
    labels = ['18-30', '31-45', '46-60', '61+']
    temp_df['AgeGroup'] = pd.cut(temp_df['Age'], bins=bins, labels=labels)

    fig, ax = plt.subplots()
    temp_df.boxplot(column='PurchaseAmount', by='AgeGroup', ax=ax)

    ax.set_title("Purchase Amount by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Purchase Amount")
    plt.suptitle("")
    plt.tight_layout()
    return fig


def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    fig, ax = plt.subplots()
    ax.hist(customer_df['PurchaseAmount'], bins=20, edgecolor='black')

    ax.set_title("Purchase Amount Distribution")
    ax.set_xlabel("Purchase Amount")
    ax.set_ylabel("Frequency")
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    return fig


def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    tier_sales = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()

    explode = [0, 0, 0]
    biggest = np.argmax(tier_sales.values)
    explode[biggest] = 0.1

    fig, ax = plt.subplots()
    ax.pie(tier_sales.values, labels=tier_sales.index, autopct='%1.1f%%', explode=explode, startangle=90)
    ax.set_title("Sales by Price Tier")
    return fig


def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    cat_sales = sales_df.groupby('Category')['Sales'].sum()

    explode = [0] * len(cat_sales)
    biggest = np.argmax(cat_sales.values)
    explode[biggest] = 0.1

    fig, ax = plt.subplots()
    ax.pie(cat_sales.values, labels=cat_sales.index, autopct='%1.1f%%', explode=explode, startangle=90)
    ax.set_title("Category Market Share")
    return fig


def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    loc_sales = sales_df.groupby('Location')['Sales'].sum()

    fig, ax = plt.subplots()
    ax.pie(loc_sales.values, labels=loc_sales.index, autopct='%1.1f%%', startangle=90)
    ax.set_title("Sales Distribution by Location")
    return fig


def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    quarter_sales = sales_df.groupby('QuarterLabel')['Sales'].sum()
    axes[0, 0].plot(quarter_sales.index, quarter_sales.values, marker='o')
    axes[0, 0].set_title("Overall Sales Trend")
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, alpha=0.4)

    loc_sales = sales_df.groupby('Location')['Sales'].sum()
    axes[0, 1].bar(loc_sales.index, loc_sales.values)
    axes[0, 1].set_title("Sales by Location")
    axes[0, 1].tick_params(axis='x', rotation=20)

    axes[1, 0].scatter(sales_df['AdSpend'], sales_df['Sales'], alpha=0.7)
    axes[1, 0].set_title("Ad Spend vs Sales")
    axes[1, 0].set_xlabel("Ad Spend")
    axes[1, 0].set_ylabel("Sales")

    cat_sales = sales_df.groupby('Category')['Sales'].sum()
    axes[1, 1].pie(cat_sales.values, labels=cat_sales.index, autopct='%1.1f%%', startangle=90)
    axes[1, 1].set_title("Category Market Share")

    fig.suptitle("SunCoast Retail Dashboard")
    plt.tight_layout()
    return fig


def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()

    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()

    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()

    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()

    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()

    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()

    fig13 = create_business_dashboard()

    print("\nKEY BUSINESS INSIGHTS:")
    print("- Sales generally increased over the time period, especially in Q4.")
    print("- Miami had the strongest total sales compared to the other locations.")
    print("- Electronics looked like the strongest category overall.")
    print("- There is a positive relationship between ad spending and sales.")
    print("- Customer age patterns are a little different depending on location.")
    print("- Mid-range and premium purchases make up a large share of spending.")
    print("- The company should focus more on strong categories and strong locations.")

    plt.show()


if __name__ == "__main__":
    main()