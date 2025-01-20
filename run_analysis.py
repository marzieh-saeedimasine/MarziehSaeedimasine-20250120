import argparse
from customer_service_analysis import CustomerServiceAnalysis

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Run customer service data analysis')
    parser.add_argument('--errands', 
                       default='Data/errands.parquet',
                       help='Path to errands parquet file')
    parser.add_argument('--orders', 
                       default='Data/orders.parquet',
                       help='Path to orders parquet file')
    parser.add_argument('--output', 
                       default='analysis/figures',
                       help='Output directory for figures')
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Initialize analysis
        analysis = CustomerServiceAnalysis(
            errands_path=args.errands,
            orders_path=args.orders
        )
        
        # Generate all analyses
        results = analysis.generate_all_analyses()
        
        # Print results
        print("\n=== Analysis Results ===")
        print(f"Average contacts per order: {results['avg_contacts']:.2f}")
        
        print("\nTop channels distribution:")
        print(results['channel_dist'].head())

        print("\nTop errand categories:")
        print(results['errand_dist']['category_dist'].head())
        
        print("\nTop errand types:")
        print(results['errand_dist']['type_dist'].head())
        
        print("\nTop errand actions:")
        print(results['errand_dist']['action_dist'].head())
        
        print("\nTop 2 busiest dates:")
        print(results['time_patterns']['top_days'])
        
        print("\nTop 2 busiest days of week:")
        print(results['time_patterns']['top_weekdays'])
        
        print("\nTop 5 busiest hours:")
        print(results['time_patterns']['top_hours'])
        
        print("\nTop 10 routes with most contacts:")
        print(results['travel_details']['top_routes'])
        
        print("\nJourney type distribution:")
        print(results['travel_details']['journey_types'])
        
        print("\nBooking source distribution:")
        print(results['travel_details']['booking_sources'])
        
        print("\nDaily contact trend statistics:")
        print(f"Mean daily contacts: {results['time_patterns']['daily_trend'].mean():.2f}%")
        print(f"Max daily contacts: {results['time_patterns']['daily_trend'].max():.2f}%")
        print(f"Min daily contacts: {results['time_patterns']['daily_trend'].min():.2f}%")
        
        print("\nTop cancellation reasons:")
        print(results['cancellation_dist']['reasons'].head())
        
        print("\nTop 3 routes with most cancellations:")
        print(results['cancellation_dist']['top_routes'])
        
        print("\nTop 2 journey types with most cancellations:")
        print(results['cancellation_dist']['top_journey_types'])
        
        print("\nTop change reasons:")
        print(results['change_dist']['reasons'].head())
        
        print("\nTop 3 routes with most changes:")
        print(results['change_dist']['top_routes'])
        
        print("\nTop 2 journey types with most changes:")
        print(results['change_dist']['top_journey_types'])
        
        print("\nRevenue distribution by customer group (%):")
        print((results['financial_patterns']['revenue_dist']).head())
        
        print("\nContact distribution by customer group (%):")
        print((results['financial_patterns']['contact_dist']).head())
        
        
        print(f"\nFigures have been saved to: {args.output}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 