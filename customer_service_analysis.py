import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

class CustomerServiceAnalysis:
    def __init__(self, errands_path, orders_path):
        """Initialize the analysis with data paths."""
        self.errands_df = pd.read_parquet(errands_path)
        self.orders_df = pd.read_parquet(orders_path)
        self.merged_df = None
        self._preprocess_data()
        
        # Create figures directory if it doesn't exist
        os.makedirs('analysis/figures', exist_ok=True)
        
    def _preprocess_data(self):
        """Preprocess and merge the datasets."""
        # Convert order numbers
        self.errands_df['order_number'] = self.errands_df['order_number'].apply(lambda x: str(int(x, 36)))
        self.orders_df['order_id'] = self.orders_df['order_id'].astype(str)
        
        # Convert timestamps
        self.errands_df['errand_created_at'] = pd.to_datetime(self.errands_df['created'])
        self.orders_df['order_created_at'] = pd.to_datetime(self.orders_df['order_created_at'])
        # Add day of week
        self.errands_df['day_of_week'] = self.errands_df['errand_created_at'].dt.day_name()
        
        # Merge datasets
        self.merged_df = pd.merge(
            self.errands_df,
            self.orders_df,
            left_on='order_number',
            right_on='order_id',
            how='inner'
        )
            
        
    def analyze_contacts_per_order(self):
        """Analyze and plot contacts per order distribution."""
        contacts_per_order = self.merged_df.groupby('order_number').size()
        average_contacts = contacts_per_order.mean()
        distribution = contacts_per_order.value_counts().sort_index()
        percentages = (distribution / len(contacts_per_order) * 100)
        
        plt.figure(figsize=(10, 6))
        plt.bar(percentages[percentages.index <= 10].index,
                percentages[percentages.index <= 10].values,
                color='skyblue', edgecolor='black')
        plt.xlabel('Number of Contacts per Order')
        plt.ylabel('Percentage of Orders')
        plt.title('Distribution of Contacts per Order (Up to 10 Contacts)')
        plt.xticks(range(0, 11))
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig('analysis/figures/contacts_per_order.png')
        plt.close()
        
        return average_contacts

    def analyze_channel_distribution(self):
        """Analyze and plot contact channel distribution."""
        channel_distribution = self.merged_df['errand_channel'].value_counts()
        percentages = (channel_distribution / len(self.merged_df)) * 100
        
        plt.figure(figsize=(10, 6))
        percentages.plot(kind='bar', color='orange', edgecolor='black')
        plt.xlabel('Contact Channel')
        plt.ylabel('Percentage of Total Contacts')
        plt.title('Distribution of Contact Channels')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('analysis/figures/channel_distribution.png')
        plt.close()
        return percentages
    

    def analyze_errand_categories(self):
        """Analyze and plot errand categories, types, and actions distribution."""
        # Calculate category distribution
        category_distribution = self.merged_df['errand_category'].value_counts()
        category_percentage = (category_distribution / category_distribution.sum()) * 100

        # Calculate type distribution
        type_distribution = self.merged_df.groupby('errand_category')['errand_type'].value_counts()
        type_percentage = (type_distribution / type_distribution.sum()) * 100
        
        # Function to map actions
        def categorize_errand_action(action):
            if pd.isna(action):
                return None
            prefix = action.split(':')[0].split('.')[0]
            return prefix
        
        # Calculate action distribution
        self.merged_df['errand_action_category'] = self.merged_df['errand_action'].apply(categorize_errand_action)
        action_counts = self.merged_df['errand_action_category'].value_counts()
        action_percentages = (action_counts / len(self.merged_df) * 100).round(2)

        # Create figure with three subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 6))

        # Plot category distribution
        category_percentage.head(8).plot(kind='bar', color='blue', edgecolor='black', ax=ax1)
        ax1.set_xlabel('Errand Category')
        ax1.set_ylabel('Percentage of Contacts')
        ax1.set_title('Distribution of Top 8 Errand Categories')
        ax1.tick_params(axis='x', rotation=60)
        ax1.grid(axis='y', linestyle='--', alpha=0.7)

        # Plot type distribution
        type_percentage.head(8).plot(kind='bar', color='green', edgecolor='black', ax=ax2)
        ax2.set_xlabel('Errand Type by Category')
        ax2.set_ylabel('Percentage of Contacts')
        ax2.set_title('Distribution of Top 8 Errand Types')
        ax2.tick_params(axis='x', rotation=60)
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Plot action distribution
        action_percentages.head(8).plot(kind='bar', color='red', edgecolor='black', ax=ax3)
        ax3.set_xlabel('Errand Action Category')
        ax3.set_ylabel('Percentage of Contacts')
        ax3.set_title('Distribution of Top 8 Errand Actions')
        ax3.tick_params(axis='x', rotation=60)
        ax3.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.savefig('analysis/figures/errand_distribution.png')
        plt.close()

        return {
            'category_dist': category_percentage,
            'type_dist': type_percentage,
            'action_dist': action_percentages
        }
    def analyze_time_patterns(self):
        """Analyze and plot time-based patterns in customer service contacts."""
        # Daily time series analysis
        time_series = self.merged_df.resample('D', on='errand_created_at').size()
        daily_total = time_series.sum()
        daily_percentages = (time_series / daily_total * 100)
        
        # Get top 2 days with most contacts
        top_days = daily_percentages.sort_values(ascending=False).head(2)
        
        # Create daily trend plot
        plt.figure(figsize=(12, 6))
        daily_percentages.plot(color='green')
        plt.xlabel('Date')
        plt.ylabel('Percentage of Daily Contacts')
        plt.title('Customer Service Contacts Over Time (% of Daily Total)')
        plt.grid(axis='both', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('analysis/figures/daily_contacts_trend.png')
        plt.close()
        
        # Create a custom order for days of the week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Day of week analysis with ordered categories
        self.merged_df['day_of_week'] = pd.Categorical(
            self.merged_df['errand_created_at'].dt.day_name(),
            categories=day_order,
            ordered=True
        )
        
        # Hour of day analysis
        self.merged_df['hour_of_day'] = self.merged_df['errand_created_at'].dt.hour
        
        # Calculate day and hour distributions
        day_analysis = self.merged_df.groupby('day_of_week').size()
        day_percentages = (day_analysis / day_analysis.sum() * 100).round(2)
        
        hour_analysis = self.merged_df.groupby('hour_of_day').size()
        hour_percentages = (hour_analysis / hour_analysis.sum() * 100).round(2)
        
        # Create figure with two subplots side by side
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
        
        # Plot distribution by day
        day_percentages.plot(kind='bar', color='pink', edgecolor='black', ax=ax1)
        ax1.set_title('Distribution of Contacts by Day of Week')
        ax1.set_xlabel('Day of Week')
        ax1.set_ylabel('Percentage of Total Contacts')
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        ax1.tick_params(axis='x', rotation=45)
        
        # Plot distribution by hour
        hour_percentages.plot(kind='bar', color='red', edgecolor='black', ax=ax2)
        ax2.set_title('Distribution of Contacts by Hour of Day')
        ax2.set_xlabel('Hour of Day')
        ax2.set_ylabel('Percentage of Total Contacts')
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        ax2.tick_params(axis='x', rotation=45)
        
        # Adjust layout to prevent overlap
        plt.tight_layout()
        plt.savefig('analysis/figures/time_distribution.png')
        plt.close()
        
        # Get top values
        top_weekdays = day_percentages.sort_values(ascending=False).head(2)
        top_hours = hour_percentages.sort_values(ascending=False).head(5)
        
        return {
            'daily_trend': daily_percentages,
            'day_of_week': day_percentages,
            'hour_of_day': hour_percentages,
            'top_days': top_days,
            'top_weekdays': top_weekdays,
            'top_hours': top_hours
        }
    def analyze_travel_details(self):
        """Analyze travel routes, journey types, and booking sources."""
        # Analyze routes
        route_contacts = self.merged_df.groupby(['Origin_Country', 'Destination_Country']).size().reset_index(name='route_count')
        route_contacts['route_percentage'] = (route_contacts['route_count'] / route_contacts['route_count'].sum() * 100).round(2)
        route_contacts = route_contacts.sort_values(by='route_percentage', ascending=False)
        
        # Analyze journey types
        journey_contacts = self.merged_df['Journey_Type_ID'].value_counts()
        journey_percentage = (journey_contacts / journey_contacts.sum() * 100).round(2)
        
        # Create journey type plot
        plt.figure(figsize=(10, 6))
        journey_percentage.plot(kind='bar', color='cyan', edgecolor='black')
        plt.xlabel('Journey Type')
        plt.ylabel('Percentage of Contacts')
        plt.title('Contacts by Journey Type')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('analysis/figures/journey_type_distribution.png')
        plt.close()
        
        # Analyze booking sources
        booking_system_contacts = self.merged_df['booking_system_source_type'].value_counts()
        booking_system_percentage = (booking_system_contacts / booking_system_contacts.sum() * 100).round(2)
        
        # Create booking source plot
        plt.figure(figsize=(10, 6))
        booking_system_percentage.plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title('Booking Source Distribution')
        plt.xlabel('Booking System Source Type')
        plt.ylabel('Percentage of Total Bookings')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('analysis/figures/booking_source_distribution.png')
        plt.close()
        
        return {
            'top_routes': route_contacts.head(10),
            'journey_types': journey_percentage,
            'booking_sources': booking_system_percentage
        }

    def analyze_cancellations(self):
        """Analyze cancellation patterns."""
        # Update cancellation status
        self.merged_df.loc[
            (self.merged_df['Is_Canceled'] == 0) & 
            (self.merged_df['cancel_reason'] == "Schedule Change - refund"), 
            'Is_Canceled'
        ] = 1
        
        # Calculate percentages for cancellation reasons
        cancel_reasons = self.merged_df[self.merged_df['Is_Canceled'] == 1]['cancel_reason'].value_counts()
        cancel_percentages = (cancel_reasons / len(self.merged_df[self.merged_df['Is_Canceled'] == 1]) * 100).round(2)
        
        # Analyze cancellation patterns by route
        cancel_routes = self.merged_df[self.merged_df['Is_Canceled'] == 1].groupby(
            ['Origin_Country', 'Destination_Country']
        ).size()
        cancel_routes_percentages = (
            cancel_routes / len(self.merged_df[self.merged_df['Is_Canceled'] == 1]) * 100
        ).round(2).sort_values(ascending=False)
        
        # Analyze cancellation patterns by journey type
        cancel_journeytype = self.merged_df[self.merged_df['Is_Canceled'] == 1].groupby(
            ['Journey_Type_ID']
        ).size()
        cancel_journeytype_percentages = (
            cancel_journeytype / len(self.merged_df[self.merged_df['Is_Canceled'] == 1]) * 100
        ).round(2).sort_values(ascending=False)
        
        # Plot cancellation reasons
        plt.figure(figsize=(12, 6))
        cancel_percentages.head(8).plot(kind='bar')
        plt.title('Distribution of Cancellation Reasons')
        plt.xlabel('Cancellation Reason')
        plt.ylabel('Percentage of Cancelled Orders')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('analysis/figures/cancellation_distribution.png')
        plt.close()
        
        return {
            'reasons': cancel_percentages,
            'top_routes': cancel_routes_percentages.head(3),
            'top_journey_types': cancel_journeytype_percentages.head(2)
        }

    def analyze_changes(self):
        """Analyze change patterns."""
        # Update change status
        self.merged_df.loc[
            (self.merged_df['Is_Changed'] == 0) & 
            (self.merged_df['change_reason'].isin([
                "Schedule change: Primary Alternative", 
                "Cancel part of order"
            ])), 
            'Is_Changed'
        ] = 1
        
        # Calculate percentages for change reasons
        change_reasons = self.merged_df[self.merged_df['Is_Changed'] == 1]['change_reason'].value_counts()
        change_percentages = (change_reasons / len(self.merged_df[self.merged_df['Is_Changed'] == 1]) * 100).round(2)
        
        # Analyze change patterns by route
        change_routes = self.merged_df[self.merged_df['Is_Changed'] == 1].groupby(
            ['Origin_Country', 'Destination_Country']
        ).size()
        change_routes_percentages = (
            change_routes / len(self.merged_df[self.merged_df['Is_Changed'] == 1]) * 100
        ).round(2).sort_values(ascending=False)
        
        # Analyze change patterns by journey type
        change_journeytype = self.merged_df[self.merged_df['Is_Changed'] == 1].groupby(
            ['Journey_Type_ID']
        ).size()
        change_journeytype_percentages = (
            change_journeytype / len(self.merged_df[self.merged_df['Is_Changed'] == 1]) * 100
        ).round(2).sort_values(ascending=False)
        
        # Plot change reasons
        plt.figure(figsize=(12, 6))
        change_percentages.head(8).plot(kind='bar')
        plt.title('Distribution of Change Reasons')
        plt.xlabel('Change Reason')
        plt.ylabel('Percentage of Changed Orders')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('analysis/figures/change_distribution.png')
        plt.close()
        
        return {
            'reasons': change_percentages,
            'top_routes': change_routes_percentages.head(3),
            'top_journey_types': change_journeytype_percentages.head(2)
        }

    def analyze_financial_patterns(self):
        """Analyze financial patterns and customer groups."""
        # Analyze contacts by customer group
        customer_group_contacts = self.merged_df['Customer_Group_Type'].value_counts()
        customer_group_percentages = (
            customer_group_contacts / customer_group_contacts.sum() * 100
        ).sort_values(ascending=False)
        
        # Analyze revenue by customer group
        revenue_by_group = self.merged_df.groupby('Customer_Group_Type')['Revenue'].sum()
        revenue_percentages = (
            revenue_by_group / revenue_by_group.sum() * 100
        ).sort_values(ascending=False)
        
        # Create comparison plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot revenue and contact percentages
        revenue_percentages.plot(
            kind='bar', 
            color='skyblue', 
            edgecolor='black', 
            ax=ax, 
            label='Revenue %'
        )
        customer_group_percentages.plot(
            kind='line', 
            color='red', 
            marker='o', 
            ax=ax, 
            label='Contacts %'
        )
        
        # Customize plot
        ax.set_xlabel('Customer Group Type')
        ax.set_ylabel('Percentage')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.legend()
        
        plt.title('Distribution of Contacts and Revenue by Customer Group')
        plt.tight_layout()
        plt.savefig('analysis/figures/financial_distribution.png')
        plt.close()
        
        return {
            'revenue_dist': revenue_percentages,
            'contact_dist': customer_group_percentages
        }

    def generate_all_analyses(self):
        """Generate all analyses and save figures."""
        try:
            # Calculate basic metrics first
            analyses = {
                'avg_contacts': self.analyze_contacts_per_order(),
                'errand_dist': self.analyze_errand_categories(),
                'channel_dist': self.analyze_channel_distribution(),
                'time_patterns': self.analyze_time_patterns(),
                'travel_details': self.analyze_travel_details(),
                'cancellation_dist': self.analyze_cancellations(),
                'change_dist': self.analyze_changes(),
                'financial_patterns': self.analyze_financial_patterns()
            }
            
            # Validate results
            for key, value in analyses.items():
                if value is None:
                    print(f"Warning: {key} analysis returned None")
                    
            return analyses
            
        except Exception as e:
            print(f"Error generating analyses: {str(e)}")
            return None