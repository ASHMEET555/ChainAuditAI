"""
Test Data Generator for FraudProof Ledger

Generates synthetic test data for all 4 fraud detection models:
- Vehicle Insurance Fraud
- Bank Account Fraud  
- E-commerce Fraud
- Ethereum Blockchain Fraud

Features:
- Samples both fraud and non-fraud records
- Applies randomization and transformations to create new synthetic samples
- Handles numeric ranges, categorical features
- Preserves all original columns and data types
- Generates ~50 rows per category
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid
import os

# Set random seed for reproducibility
np.random.seed(42)

# Output directory
OUTPUT_DIR = 'data/test_data'
os.makedirs(OUTPUT_DIR, exist_ok=True)


class VehicleDataGenerator:
    """Generate synthetic vehicle insurance fraud test data."""
    
    def __init__(self, csv_path='data/vehicle_insurance_fraud.csv'):
        """Load and analyze vehicle insurance dataset."""
        self.df = pd.read_csv(csv_path)
        self.fraud_col = 'FraudFound_P'  # Fraud column
        self.categorical_cols = self.df.select_dtypes(include='object').columns.tolist()
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        print(f"Vehicle Dataset: {len(self.df)} rows, {len(self.df.columns)} columns")
        print(f"Fraud samples: {(self.df[self.fraud_col]==1).sum()}")
        print(f"Non-fraud samples: {(self.df[self.fraud_col]==0).sum()}")
    
    def generate_synthetic_data(self, n_fraud=25, n_non_fraud=25):
        """
        Generate synthetic vehicle data by sampling and perturbing real data.
        
        Args:
            n_fraud: Number of fraud samples to generate
            n_non_fraud: Number of non-fraud samples to generate
        
        Returns:
            DataFrame with synthetic data
        """
        fraud_data = self.df[self.df[self.fraud_col] == 1]
        non_fraud_data = self.df[self.df[self.fraud_col] == 0]
        
        synthetic_records = []
        
        # Sample and perturb fraud records
        for _ in range(n_fraud):
            record = fraud_data.sample(1).iloc[0].copy()
            record = self._perturb_record(record)
            record[self.fraud_col] = 1
            synthetic_records.append(record)
        
        # Sample and perturb non-fraud records
        for _ in range(n_non_fraud):
            record = non_fraud_data.sample(1).iloc[0].copy()
            record = self._perturb_record(record)
            record[self.fraud_col] = 0
            synthetic_records.append(record)
        
        return pd.DataFrame(synthetic_records)
    
    def _perturb_record(self, record):
        """Apply randomization to numeric and categorical features."""
        # Perturb numeric columns by ±10-30%
        for col in self.numeric_cols:
            if col != self.fraud_col:
                try:
                    if pd.notna(record[col]) and record[col] != 0:
                        perturbation = np.random.uniform(-0.3, 0.3)
                        record[col] = record[col] * (1 + perturbation)
                except:
                    pass
        
        return record
    
    def save(self, df):
        """Save to CSV with all columns preserved."""
        output_path = os.path.join(OUTPUT_DIR, 'vehicle_test_data.csv')
        df.to_csv(output_path, index=False)
        print(f"✓ Saved Vehicle: {output_path} ({len(df)} rows, {len(df.columns)} columns)")
        return output_path


class BankDataGenerator:
    """Generate synthetic bank account fraud test data."""
    
    def __init__(self, csv_path='data/bank_fraud.csv'):
        """Load and analyze bank fraud dataset."""
        self.df = pd.read_csv(csv_path, nrows=50000)  # Load subset for speed
        self.fraud_col = 'fraud_bool'
        self.categorical_cols = self.df.select_dtypes(include='object').columns.tolist()
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        print(f"\nBank Dataset: {len(self.df)} rows, {len(self.df.columns)} columns")
        print(f"Fraud samples: {(self.df[self.fraud_col]==1).sum()}")
        print(f"Non-fraud samples: {(self.df[self.fraud_col]==0).sum()}")
    
    def generate_synthetic_data(self, n_fraud=25, n_non_fraud=25):
        """Generate synthetic bank data with perturbations."""
        fraud_data = self.df[self.df[self.fraud_col] == 1]
        non_fraud_data = self.df[self.df[self.fraud_col] == 0]
        
        synthetic_records = []
        
        # Sample and perturb fraud records
        for _ in range(min(n_fraud, len(fraud_data))):
            record = fraud_data.sample(1).iloc[0].copy()
            record = self._perturb_record(record)
            record[self.fraud_col] = 1
            synthetic_records.append(record)
        
        # Sample and perturb non-fraud records
        for _ in range(min(n_non_fraud, len(non_fraud_data))):
            record = non_fraud_data.sample(1).iloc[0].copy()
            record = self._perturb_record(record)
            record[self.fraud_col] = 0
            synthetic_records.append(record)
        
        return pd.DataFrame(synthetic_records)
    
    def _perturb_record(self, record):
        """Apply randomization to numeric and categorical features."""
        # Perturb numeric columns by ±20-40%
        for col in self.numeric_cols:
            if col != self.fraud_col:
                try:
                    if pd.notna(record[col]):
                        if record[col] == 0:
                            record[col] = np.random.uniform(0, 100)
                        else:
                            perturbation = np.random.uniform(-0.4, 0.4)
                            record[col] = record[col] * (1 + perturbation)
                except:
                    pass
        
        # Randomly select categorical values from dataset
        for col in self.categorical_cols:
            if np.random.random() < 0.3:  # 30% chance to change
                unique_vals = self.df[col].dropna().unique()
                if len(unique_vals) > 0:
                    record[col] = np.random.choice(unique_vals)
        
        return record
    
    def save(self, df):
        """Save to CSV with all columns preserved."""
        output_path = os.path.join(OUTPUT_DIR, 'bank_test_data.csv')
        df.to_csv(output_path, index=False)
        print(f"✓ Saved Bank: {output_path} ({len(df)} rows, {len(df.columns)} columns)")
        return output_path


class EcommerceDataGenerator:
    """Generate synthetic e-commerce fraud test data."""
    
    def __init__(self, csv_path='data/ecommerce_fraud_lite.csv'):
        """Load and analyze e-commerce dataset."""
        self.df = pd.read_csv(csv_path)
        self.fraud_col = 'Is Fraudulent'
        self.categorical_cols = self.df.select_dtypes(include='object').columns.tolist()
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        print(f"\nE-commerce Dataset: {len(self.df)} rows, {len(self.df.columns)} columns")
        print(f"Fraud samples: {(self.df[self.fraud_col]==1).sum()}")
        print(f"Non-fraud samples: {(self.df[self.fraud_col]==0).sum()}")
    
    def generate_synthetic_data(self, n_fraud=25, n_non_fraud=25):
        """Generate synthetic e-commerce data with perturbations."""
        fraud_data = self.df[self.df[self.fraud_col] == 1]
        non_fraud_data = self.df[self.df[self.fraud_col] == 0]
        
        synthetic_records = []
        
        # Sample and perturb fraud records
        for _ in range(min(n_fraud, len(fraud_data))):
            record = fraud_data.sample(1).iloc[0].copy()
            record = self._perturb_record(record, is_fraud=True)
            record[self.fraud_col] = 1
            synthetic_records.append(record)
        
        # Sample and perturb non-fraud records
        for _ in range(min(n_non_fraud, len(non_fraud_data))):
            record = non_fraud_data.sample(1).iloc[0].copy()
            record = self._perturb_record(record, is_fraud=False)
            record[self.fraud_col] = 0
            synthetic_records.append(record)
        
        return pd.DataFrame(synthetic_records)
    
    def _perturb_record(self, record, is_fraud=False):
        """Apply randomization with fraud-aware transformations."""
        # Perturb numeric columns
        for col in self.numeric_cols:
            if col != self.fraud_col:
                try:
                    if pd.notna(record[col]) and record[col] > 0:
                        if is_fraud:
                            # Frauds tend to have higher amounts or odd patterns
                            perturbation = np.random.uniform(0.5, 1.5)
                        else:
                            perturbation = np.random.uniform(-0.3, 0.3)
                        record[col] = record[col] * (1 + perturbation)
                except:
                    pass
        
        # Regenerate IDs for uniqueness
        if 'Transaction ID' in record.index:
            record['Transaction ID'] = str(uuid.uuid4())
        if 'Customer ID' in record.index:
            record['Customer ID'] = str(uuid.uuid4())
        
        # Randomly modify categorical fields
        for col in self.categorical_cols:
            if col not in ['Transaction ID', 'Customer ID'] and np.random.random() < 0.2:
                unique_vals = self.df[col].dropna().unique()
                if len(unique_vals) > 0:
                    record[col] = np.random.choice(unique_vals)
        
        return record
    
    def save(self, df):
        """Save to CSV with all columns preserved."""
        output_path = os.path.join(OUTPUT_DIR, 'ecommerce_test_data.csv')
        df.to_csv(output_path, index=False)
        print(f"✓ Saved E-commerce: {output_path} ({len(df)} rows, {len(df.columns)} columns)")
        return output_path


class EthereumDataGenerator:
    """Generate synthetic Ethereum fraud test data."""
    
    def __init__(self, txt_path='data/eth_fraud.txt'):
        """Load and analyze Ethereum fraud dataset."""
        try:
            self.df = pd.read_csv(txt_path, sep='\t', nrows=10000)
        except:
            # Fallback if format differs
            print("Warning: Could not parse Ethereum data with tab separator")
            self.df = pd.read_csv(txt_path, nrows=10000)
        
        self.fraud_col = 'flagged'  # Common fraud column name
        
        # If fraud column doesn't exist, create it based on available data
        if self.fraud_col not in self.df.columns:
            # Try common alternatives
            for col in ['fraud', 'is_fraud', 'is_fraudulent', 'Fraud']:
                if col in self.df.columns:
                    self.fraud_col = col
                    break
            else:
                # Default: assume last numeric column or create random
                self.fraud_col = 'is_fraud'
                self.df[self.fraud_col] = np.random.randint(0, 2, len(self.df))
        
        self.categorical_cols = self.df.select_dtypes(include='object').columns.tolist()
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        print(f"\nEthereum Dataset: {len(self.df)} rows, {len(self.df.columns)} columns")
        print(f"Fraud column: {self.fraud_col}")
        if self.fraud_col in self.df.columns:
            print(f"Fraud samples: {(self.df[self.fraud_col]==1).sum()}")
            print(f"Non-fraud samples: {(self.df[self.fraud_col]==0).sum()}")
    
    def generate_synthetic_data(self, n_fraud=25, n_non_fraud=25):
        """Generate synthetic Ethereum data with perturbations."""
        if self.df.empty:
            print("Warning: Ethereum dataset is empty, creating minimal synthetic data")
            return self._create_minimal_eth_data(n_fraud, n_non_fraud)
        
        if self.fraud_col not in self.df.columns:
            self.df[self.fraud_col] = 0
        
        fraud_data = self.df[self.df[self.fraud_col] == 1]
        non_fraud_data = self.df[self.df[self.fraud_col] == 0]
        
        synthetic_records = []
        
        # If no fraud data, use non-fraud data instead
        if len(fraud_data) == 0:
            fraud_data = non_fraud_data.sample(min(n_fraud, len(non_fraud_data)))
        
        # Sample and perturb fraud records
        n_fraud_available = min(n_fraud, len(fraud_data))
        for _ in range(n_fraud_available):
            record = fraud_data.sample(1).iloc[0].copy()
            record = self._perturb_record(record)
            record[self.fraud_col] = 1
            synthetic_records.append(record.to_dict())
        
        # Sample and perturb non-fraud records
        n_non_fraud_available = min(n_non_fraud, len(non_fraud_data))
        for _ in range(n_non_fraud_available):
            record = non_fraud_data.sample(1).iloc[0].copy()
            record = self._perturb_record(record)
            record[self.fraud_col] = 0
            synthetic_records.append(record.to_dict())
        
        # Fill remaining with synthetic data if needed
        while len(synthetic_records) < (n_fraud + n_non_fraud):
            record = self._create_synthetic_ethereum_record()
            synthetic_records.append(record)
        
        return pd.DataFrame(synthetic_records)
    
    def _perturb_record(self, record):
        """Apply randomization to numeric and categorical features."""
        # Perturb numeric columns by ±15-40%
        for col in self.numeric_cols:
            try:
                if pd.notna(record[col]):
                    val = float(record[col])
                    if val != 0:
                        perturbation = np.random.uniform(-0.4, 0.4)
                        record[col] = val * (1 + perturbation)
                    else:
                        record[col] = np.random.uniform(0, 100)
            except:
                pass
        
        return record
    
    def _create_synthetic_ethereum_record(self):
        """Create a synthetic Ethereum record."""
        record = {
            'blockNumber': np.random.randint(16000000, 18000000),
            'confirmations': np.random.randint(1, 1000),
            'Month': np.random.randint(1, 13),
            'Day': np.random.randint(1, 32),
            'Hour': np.random.randint(0, 24),
            'mean_value_received': np.random.exponential(0.5),
            'variance_value_received': np.random.exponential(0.1),
            'total_received_time_diff': np.random.exponential(1),
            'total_tx_sent': np.random.randint(1, 1000),
            self.fraud_col: np.random.randint(0, 2)
        }
        return record
    
    def _create_minimal_eth_data(self, n_fraud, n_non_fraud):
        """Create minimal Ethereum data structure."""
        records = []
        for i in range(n_fraud):
            records.append({
                'blockNumber': 16000000 + i,
                'confirmations': np.random.randint(1, 1000),
                'Month': np.random.randint(1, 13),
                'Day': np.random.randint(1, 32),
                'Hour': np.random.randint(0, 24),
                'mean_value_received': np.random.exponential(0.5),
                'variance_value_received': np.random.exponential(0.1),
                'total_received_time_diff': np.random.exponential(1),
                'total_tx_sent': np.random.randint(1, 1000),
                self.fraud_col: 1
            })
        for i in range(n_non_fraud):
            records.append({
                'blockNumber': 16000000 + n_fraud + i,
                'confirmations': np.random.randint(1, 1000),
                'Month': np.random.randint(1, 13),
                'Day': np.random.randint(1, 32),
                'Hour': np.random.randint(0, 24),
                'mean_value_received': np.random.exponential(0.5),
                'variance_value_received': np.random.exponential(0.1),
                'total_received_time_diff': np.random.exponential(1),
                'total_tx_sent': np.random.randint(1, 1000),
                self.fraud_col: 0
            })
        return pd.DataFrame(records)
    
    def save(self, df):
        """Save to CSV with all columns preserved."""
        output_path = os.path.join(OUTPUT_DIR, 'ethereum_test_data.csv')
        df.to_csv(output_path, index=False)
        print(f"✓ Saved Ethereum: {output_path} ({len(df)} rows, {len(df.columns)} columns)")
        return output_path


def main():
    """Generate test data for all 4 fraud detection models."""
    print("\n" + "="*80)
    print("FRAUDPROOF LEDGER - TEST DATA GENERATOR")
    print("="*80)
    
    # Vehicle Insurance
    print("\n[1/4] Generating Vehicle Insurance Test Data...")
    vehicle_gen = VehicleDataGenerator()
    vehicle_df = vehicle_gen.generate_synthetic_data(n_fraud=25, n_non_fraud=25)
    vehicle_path = vehicle_gen.save(vehicle_df)
    print(f"   Columns: {list(vehicle_df.columns)[:5]}... (total: {len(vehicle_df.columns)})")
    print(f"   Sample fraud_score range: {vehicle_df['FraudFound_P'].min()}-{vehicle_df['FraudFound_P'].max()}")
    
    # Bank Account
    print("\n[2/4] Generating Bank Account Test Data...")
    bank_gen = BankDataGenerator()
    bank_df = bank_gen.generate_synthetic_data(n_fraud=25, n_non_fraud=25)
    bank_path = bank_gen.save(bank_df)
    print(f"   Columns: {list(bank_df.columns)[:5]}... (total: {len(bank_df.columns)})")
    print(f"   Sample fraud_score range: {bank_df['fraud_bool'].min()}-{bank_df['fraud_bool'].max()}")
    
    # E-commerce
    print("\n[3/4] Generating E-commerce Test Data...")
    ecom_gen = EcommerceDataGenerator()
    ecom_df = ecom_gen.generate_synthetic_data(n_fraud=25, n_non_fraud=25)
    ecom_path = ecom_gen.save(ecom_df)
    print(f"   Columns: {list(ecom_df.columns)[:5]}... (total: {len(ecom_df.columns)})")
    print(f"   Sample fraud_score range: {ecom_df['Is Fraudulent'].min()}-{ecom_df['Is Fraudulent'].max()}")
    
    # Ethereum
    print("\n[4/4] Generating Ethereum Test Data...")
    eth_gen = EthereumDataGenerator()
    eth_df = eth_gen.generate_synthetic_data(n_fraud=25, n_non_fraud=25)
    eth_path = eth_gen.save(eth_df)
    print(f"   Columns: {list(eth_df.columns)[:5]}... (total: {len(eth_df.columns)})")
    print(f"   Sample fraud_score range: {eth_df[eth_gen.fraud_col].min()}-{eth_df[eth_gen.fraud_col].max()}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"✓ Vehicle: {len(vehicle_df)} rows × {len(vehicle_df.columns)} columns")
    print(f"✓ Bank: {len(bank_df)} rows × {len(bank_df.columns)} columns")
    print(f"✓ E-commerce: {len(ecom_df)} rows × {len(ecom_df.columns)} columns")
    print(f"✓ Ethereum: {len(eth_df)} rows × {len(eth_df.columns)} columns")
    print(f"\nAll test data saved to: {OUTPUT_DIR}/")
    print("="*80)
    
    # Validation: Print sample from each
    print("\nVALIDATION - Sample Records with All Columns:\n")
    
    print("VEHICLE (first row):")
    print(vehicle_df.iloc[0])
    print(f"\nVehicle dtypes:\n{vehicle_df.dtypes}\n")
    
    print("BANK (first row):")
    print(bank_df.iloc[0])
    print(f"\nBank dtypes:\n{bank_df.dtypes}\n")
    
    print("ECOMMERCE (first row):")
    print(ecom_df.iloc[0])
    print(f"\nEcommerce dtypes:\n{ecom_df.dtypes}\n")
    
    print("ETHEREUM (first row):")
    print(eth_df.iloc[0])
    print(f"\nEthereum dtypes:\n{eth_df.dtypes}\n")


if __name__ == '__main__':
    main()
