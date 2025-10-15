# Simple pytest for replication monitor
import pytest
from scripts.replication_monitor import get_replication_lag, alert_on_lag
from unittest.mock import Mock, patch

@pytest.fixture
def mock_db():
    db = Mock()
    db.cursor.return_value.fetchone.return_value = (None,) * 32 + (3,)  # Mock lag=3s
    return db

def test_lag_below_threshold(mock_db):
    with patch('pymysql.connect') as mock_connect:
        mock_connect.return_value = mock_db
        lag = get_replication_lag(mock_db)
        assert lag == 3
        alert_on_lag(lag)  # No alert expected

def test_lag_above_threshold():
    alert_on_lag(10)  # Should print alert
