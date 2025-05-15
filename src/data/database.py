from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os

Base = declarative_base()

class HistoricalPrice(Base):
    __tablename__ = 'historical_prices'
    
    ticker = Column(String, primary_key=True)
    date = Column(DateTime, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

class FinancialDatabase:
    def __init__(self, db_path='data/database/finance.db'):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def store_historical_data(self, ticker, df):
        session = self.Session()
        
        # Convert DataFrame to list of HistoricalPrice objects
        records = []
        for date, row in df.iterrows():
            records.append(HistoricalPrice(
                ticker=ticker,
                date=date.to_pydatetime(),
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            ))
        
        # Add to session and commit
        session.add_all(records)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_historical_data(self, ticker):
        session = self.Session()
        try:
            query = session.query(HistoricalPrice).filter(HistoricalPrice.ticker == ticker)
            df = pd.read_sql(query.statement, session.bind, index_col='date')
            return df
        finally:
            session.close()