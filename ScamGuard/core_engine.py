import pandas as pd
import networkx as nx
from sklearn.ensemble import RandomForestClassifier
import numpy as np

class ScamGuardEngine:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False

    def train_ai(self, df):
        """Trains the AI to recognize scam patterns."""
        X = df[['amount', 'time_gap_seconds']]
        y = df['is_scam']
        self.model.fit(X, y)
        self.is_trained = True

    def get_risk_score(self, amount, time_gap):
        """Returns a probability score (0 to 1) for a transaction."""
        if not self.is_trained: return 0.5
        return self.model.predict_proba([[amount, time_gap]])[0][1]

    def build_graph(self, df, threshold):
        """Builds a mathematical map of the money flow."""
        G = nx.DiGraph()
        for _, row in df.iterrows():
            risk = self.get_risk_score(row['amount'], row['time_gap_seconds'])
            G.add_edge(row['sender'], row['receiver'], 
                       weight=row['amount'], risk=risk, tx_id=row['tx_id'])
        return G

    def detect_laundering_cycles(self, G):
        """Finds circular routing (A -> B -> C -> A)."""
        return list(nx.simple_cycles(G))

    def trigger_alert_level(self, score):
        if score > 0.9: return "🔴 CRITICAL", "error"
        if score > 0.7: return "🟠 WARNING", "warning"
        return "🟢 CLEAR", "success"