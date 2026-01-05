"""
Market Analytics and Visualization
Generates plots and reports from simulation data.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

class MarketAnalytics:
    def __init__(self, logs_dir="logs"):
        self.logs_dir = Path(logs_dir)
        self.ledger_path = self.logs_dir / "transaction_ledger.csv"
        self.offers_path = self.logs_dir / "active_offers.json"
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)

    def generate_all_reports(self):
        """Generate all analytics and save to logs."""
        if not self.ledger_path.exists():
            print("⚠️ No transaction ledger found. Run simulation first.")
            return
        
        print("📊 Generating analytics...")
        
        try:
            self.plot_price_over_time()
            self.plot_trade_volume()
            self.plot_trader_activity()
            self.plot_market_concentration()
            self.generate_summary_report()
            
            print("✅ All reports generated in logs/ directory!")
        except Exception as e:
            print(f"❌ Error generating reports: {e}")
            import traceback
            traceback.print_exc()

    def plot_price_over_time(self):
        """Plot price evolution over time."""
        df = pd.read_csv(self.ledger_path)
        
        if df.empty:
            print("⚠️ No trades to plot")
            return
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['trade_number'] = range(1, len(df) + 1)
        
        plt.figure(figsize=(12, 6))
        plt.plot(df['trade_number'], df['price'], marker='o', linestyle='-', 
                alpha=0.7, linewidth=2, markersize=6)
        plt.title('Price Evolution Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Trade Number', fontsize=12)
        plt.ylabel('Price per Unit ($)', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Add average price line
        avg_price = df['price'].mean()
        plt.axhline(y=avg_price, color='r', linestyle='--', 
                   label=f'Average: ${avg_price:.2f}', alpha=0.7)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(self.logs_dir / 'price_evolution.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Price evolution chart saved")

    def plot_trade_volume(self):
        """Plot trading volume over time."""
        df = pd.read_csv(self.ledger_path)
        
        if df.empty:
            return
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['trade_number'] = range(1, len(df) + 1)
        df['total_value'] = df['price'] * df['quantity']
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Cumulative volume
        df['cumulative_volume'] = df['total_value'].cumsum()
        ax1.plot(df['trade_number'], df['cumulative_volume'], 
                linewidth=2, color='green', marker='o', markersize=4)
        ax1.set_title('Cumulative Trading Volume', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Trade Number', fontsize=11)
        ax1.set_ylabel('Cumulative Value ($)', fontsize=11)
        ax1.grid(True, alpha=0.3)
        
        # Individual trade values
        ax2.bar(df['trade_number'], df['total_value'], alpha=0.7, color='steelblue')
        ax2.set_title('Individual Trade Values', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Trade Number', fontsize=11)
        ax2.set_ylabel('Trade Value ($)', fontsize=11)
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(self.logs_dir / 'trade_volume.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Trade volume charts saved")

    def plot_trader_activity(self):
        """Plot most active traders (buyers and sellers)."""
        df = pd.read_csv(self.ledger_path)
        
        if df.empty:
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Top sellers
        seller_counts = df['seller'].value_counts().head(10)
        ax1.barh(range(len(seller_counts)), seller_counts.values, color='coral', alpha=0.7)
        ax1.set_yticks(range(len(seller_counts)))
        ax1.set_yticklabels(seller_counts.index)
        ax1.set_xlabel('Number of Sales', fontsize=11)
        ax1.set_title('Top 10 Sellers', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='x')
        ax1.invert_yaxis()
        
        # Top buyers
        buyer_counts = df['buyer'].value_counts().head(10)
        ax2.barh(range(len(buyer_counts)), buyer_counts.values, color='skyblue', alpha=0.7)
        ax2.set_yticks(range(len(buyer_counts)))
        ax2.set_yticklabels(buyer_counts.index)
        ax2.set_xlabel('Number of Purchases', fontsize=11)
        ax2.set_title('Top 10 Buyers', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        ax2.invert_yaxis()
        
        plt.tight_layout()
        plt.savefig(self.logs_dir / 'trader_activity.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Trader activity charts saved")

    def plot_market_concentration(self):
        """Plot market concentration and trading patterns."""
        df = pd.read_csv(self.ledger_path)
        
        if df.empty:
            return
        
        df['total_value'] = df['price'] * df['quantity']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Trading volume by seller
        seller_volume = df.groupby('seller')['total_value'].sum().sort_values(ascending=False).head(10)
        ax1.bar(range(len(seller_volume)), seller_volume.values, color='coral', alpha=0.7)
        ax1.set_xticks(range(len(seller_volume)))
        ax1.set_xticklabels(seller_volume.index, rotation=45, ha='right')
        ax1.set_ylabel('Total Sales Volume ($)', fontsize=11)
        ax1.set_title('Top 10 Sellers by Volume', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Trading volume by buyer
        buyer_volume = df.groupby('buyer')['total_value'].sum().sort_values(ascending=False).head(10)
        ax2.bar(range(len(buyer_volume)), buyer_volume.values, color='skyblue', alpha=0.7)
        ax2.set_xticks(range(len(buyer_volume)))
        ax2.set_xticklabels(buyer_volume.index, rotation=45, ha='right')
        ax2.set_ylabel('Total Purchase Volume ($)', fontsize=11)
        ax2.set_title('Top 10 Buyers by Volume', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(self.logs_dir / 'market_concentration.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  ✓ Market concentration charts saved")

    def generate_summary_report(self):
        """Generate a text summary report."""
        df = pd.read_csv(self.ledger_path)
        
        if df.empty:
            print("⚠️ No trades to analyze")
            return
        
        df['total_value'] = df['price'] * df['quantity']
        
        report = []
        report.append("=" * 70)
        report.append("MARKET SIMULATION SUMMARY REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Market Statistics
        report.append("📊 MARKET STATISTICS")
        report.append("-" * 70)
        report.append(f"Total Trades Executed: {len(df)}")
        report.append(f"Total Trading Volume: ${df['total_value'].sum():.2f}")
        report.append(f"Average Trade Value: ${df['total_value'].mean():.2f}")
        report.append(f"Average Price per Unit: ${df['price'].mean():.2f}")
        report.append(f"Price Range: ${df['price'].min():.2f} - ${df['price'].max():.2f}")
        report.append(f"Price Volatility (Std Dev): ${df['price'].std():.2f}")
        report.append(f"Total Wood Traded: {df['quantity'].sum():.0f} units")
        report.append("")
        
        # Trader Statistics
        report.append("👥 TRADER STATISTICS")
        report.append("-" * 70)
        unique_sellers = df['seller'].nunique()
        unique_buyers = df['buyer'].nunique()
        unique_traders = len(set(df['seller'].tolist() + df['buyer'].tolist()))
        
        report.append(f"Unique Sellers: {unique_sellers}")
        report.append(f"Unique Buyers: {unique_buyers}")
        report.append(f"Total Active Traders: {unique_traders}")
        report.append("")
        
        # Top Performers
        report.append("🏆 TOP PERFORMERS")
        report.append("-" * 70)
        
        report.append("\nTop 5 Sellers (by number of sales):")
        top_sellers = df['seller'].value_counts().head(5)
        for i, (name, count) in enumerate(top_sellers.items(), 1):
            report.append(f"  {i}. {name}: {count} sales")
        
        report.append("\nTop 5 Buyers (by number of purchases):")
        top_buyers = df['buyer'].value_counts().head(5)
        for i, (name, count) in enumerate(top_buyers.items(), 1):
            report.append(f"  {i}. {name}: {count} purchases")
        
        report.append("\nTop 5 Sellers (by volume):")
        seller_volume = df.groupby('seller')['total_value'].sum().sort_values(ascending=False).head(5)
        for i, (name, volume) in enumerate(seller_volume.items(), 1):
            report.append(f"  {i}. {name}: ${volume:.2f}")
        
        report.append("")
        
        # Save report
        report_text = "\n".join(report)
        with open(self.logs_dir / "summary_report.txt", "w", encoding='utf-8') as f:
            f.write(report_text)
        
        print("  ✓ Summary report saved")
        print("\n" + report_text)


if __name__ == "__main__":
    analytics = MarketAnalytics()
    analytics.generate_all_reports()